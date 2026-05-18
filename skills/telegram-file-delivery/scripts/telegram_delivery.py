#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from urllib import error, parse, request

DEFAULT_ALLOWED_EXTENSIONS = ".md,.txt,.pdf,.docx,.pptx,.xlsx,.png,.jpg,.jpeg"
TRIGGER_RE = re.compile(
    r"(?:^|\n)\s*/telegram-send\s+attachments(?:\s+to\s+(?P<chat>-?\d+))?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
DOTENV_FILES = (".env", ".env.telegram", ".env.paperclip")


def load_dotenv_if_present(start_dir: str | Path | None = None) -> str | None:
    root = Path(start_dir or Path.cwd()).resolve()
    for directory in [root, *root.parents]:
        for filename in DOTENV_FILES:
            candidate = directory / filename
            if candidate.exists() and candidate.is_file():
                for raw_line in candidate.read_text(encoding="utf-8").splitlines():
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
                return str(candidate)
    return None


def config() -> dict:
    load_dotenv_if_present()
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    default_chat_id = os.environ.get("TELEGRAM_DEFAULT_CHAT_ID", "").strip()
    allowed_chat_ids_raw = os.environ.get("TELEGRAM_ALLOWED_CHAT_IDS", "").strip()
    allowed_extensions_raw = os.environ.get("TELEGRAM_ALLOWED_EXTENSIONS", DEFAULT_ALLOWED_EXTENSIONS).strip()
    max_file_bytes = int(os.environ.get("TELEGRAM_MAX_FILE_BYTES", "50000000"))
    timeout_seconds = int(os.environ.get("TELEGRAM_TIMEOUT_SECONDS", "30"))
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required")
    if not default_chat_id:
        raise ValueError("TELEGRAM_DEFAULT_CHAT_ID is required")
    return {
        "bot_token": bot_token,
        "default_chat_id": default_chat_id,
        "allowed_chat_ids": {x.strip() for x in allowed_chat_ids_raw.split(",") if x.strip()},
        "allowed_extensions": {(x if x.startswith(".") else f'.{x}').strip().lower() for x in allowed_extensions_raw.split(",") if x.strip()},
        "max_file_bytes": max_file_bytes,
        "timeout_seconds": timeout_seconds,
    }


def validate_chat_id(chat_id: str, cfg: dict) -> str:
    normalized = str(chat_id).strip()
    if not normalized:
        raise ValueError("Target chat id is empty")
    if cfg["allowed_chat_ids"] and normalized not in cfg["allowed_chat_ids"]:
        raise ValueError(f"Chat id {normalized} is not in TELEGRAM_ALLOWED_CHAT_IDS")
    return normalized


def validate_file_path(path: str | Path, cfg: dict) -> Path:
    file_path = Path(path).expanduser().resolve()
    if not file_path.exists() or not file_path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")
    extension = file_path.suffix.lower()
    if extension not in cfg["allowed_extensions"]:
        raise ValueError(f"Extension {extension or '<none>'} is not allowed")
    if file_path.stat().st_size > cfg["max_file_bytes"]:
        raise ValueError("File too large")
    return file_path


def parse_trigger(comment_text: str) -> tuple[bool, str | None]:
    match = TRIGGER_RE.search(comment_text or "")
    if not match:
        return False, None
    return True, match.group("chat")


def post_form(base_url: str, endpoint: str, fields: dict[str, str], timeout: int) -> dict:
    data = parse.urlencode(fields).encode("utf-8")
    req = request.Request(f"{base_url}/{endpoint}", data=data, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
    return execute(req, timeout)


def post_multipart(base_url: str, endpoint: str, fields: dict[str, str], file_path: Path, timeout: int) -> dict:
    boundary = "----PaperclipTelegramDeliveryBoundary"
    body = bytearray()
    for key, value in fields.items():
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
        body.extend(str(value).encode())
        body.extend(b"\r\n")
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    content = file_path.read_bytes()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="document"; filename="{file_path.name}"\r\n'.encode())
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode())
    body.extend(content)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())
    req = request.Request(f"{base_url}/{endpoint}", data=bytes(body), method="POST", headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return execute(req, timeout)


def execute(req: request.Request, timeout: int) -> dict:
    try:
        with request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise RuntimeError(f"Telegram API HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Telegram API connection failed: {exc.reason}") from exc
    if not payload.get("ok"):
        raise RuntimeError(f"Telegram API returned failure: {payload}")
    return payload


def attachments_from_args(args) -> list[dict]:
    items = []
    for p in args.attachment or []:
        items.append({"path": str(Path(p).expanduser().resolve()), "name": None})
    if args.attachments_dir:
        root = Path(args.attachments_dir).expanduser().resolve()
        for p in sorted(root.iterdir()):
            if p.is_file():
                items.append({"path": str(p.resolve()), "name": None})
    if args.attachments_manifest:
        payload = json.loads(Path(args.attachments_manifest).expanduser().resolve().read_text())
        rows = payload.get("attachments", payload)
        for row in rows:
            if isinstance(row, str):
                items.append({"path": str(Path(row).expanduser().resolve()), "name": None})
            else:
                items.append({"path": str(Path(row["path"]).expanduser().resolve()), "name": row.get("name")})
    return items


def render_comment(result: dict) -> str:
    def bullets(items):
        if not items:
            return ["- none"]
        out = []
        for item in items:
            suffix = f" ({item['reason']})" if item.get("reason") else ""
            out.append(f"- {item['name']}{suffix}")
        return out
    lines = ["Telegram delivery completed." if result["ok"] else ("Telegram delivery not triggered." if not result["trigger_matched"] else "Telegram delivery could not complete cleanly.")]
    if result.get("target_chat_id"):
        lines += ["", f"Destination: {result['target_chat_id']}"]
    lines += ["", "Sent files:", *bullets(result["sent"]), "", "Skipped files:", *bullets(result["skipped"]), "", "Failed files:", *bullets(result["failed"])]
    if result.get("notes"):
        lines += ["", "Notes:", *[f"- {n}" for n in result["notes"]]]
    return "\n".join(lines)


def run_workflow(args) -> tuple[int, dict]:
    cfg = config()
    comment_text = args.comment_text or ""
    if args.comment_file:
        comment_text = Path(args.comment_file).read_text(encoding="utf-8")
    matched, trigger_chat_id = parse_trigger(comment_text)
    target_chat_id = args.chat_id or trigger_chat_id or cfg["default_chat_id"]
    result = {"ok": True, "trigger_matched": matched, "target_chat_id": target_chat_id, "sent": [], "skipped": [], "failed": [], "notes": []}
    if not matched:
        result["ok"] = False
        result["notes"].append("No explicit /telegram-send attachments trigger found.")
        return 1, result
    attachments = attachments_from_args(args)
    if not attachments:
        result["ok"] = False
        result["notes"].append("No attachments or deliverable files were provided to the workflow.")
        return 1, result
    base_url = f"https://api.telegram.org/bot{cfg['bot_token']}"
    for item in attachments:
        try:
            validate_chat_id(target_chat_id, cfg)
            file_path = validate_file_path(item["path"], cfg)
            post_multipart(base_url, "sendDocument", {"chat_id": target_chat_id, "caption": ""}, file_path, cfg["timeout_seconds"])
        except ValueError as exc:
            result["skipped"].append({"name": item.get("name") or Path(item["path"]).name, "path": item["path"], "status": "skipped", "reason": str(exc)})
        except Exception as exc:
            result["ok"] = False
            result["failed"].append({"name": item.get("name") or Path(item["path"]).name, "path": item["path"], "status": "failed", "reason": str(exc)})
        else:
            result["sent"].append({"name": item.get("name") or Path(item["path"]).name, "path": str(file_path), "status": "sent"})
    if not result["sent"]:
        result["ok"] = False
    return (0 if result["ok"] else 1), result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="telegram-delivery", description="Self-contained Telegram delivery workflow for Paperclip skill installs.")
    sub = parser.add_subparsers(dest="command", required=True)
    p1 = sub.add_parser("message")
    p1.add_argument("--text", required=True)
    p1.add_argument("--chat-id")
    p2 = sub.add_parser("document")
    p2.add_argument("--path", required=True)
    p2.add_argument("--chat-id")
    p3 = sub.add_parser("workflow")
    p3.add_argument("--comment-text")
    p3.add_argument("--comment-file")
    p3.add_argument("--attachment", action="append", default=[])
    p3.add_argument("--attachments-dir")
    p3.add_argument("--attachments-manifest")
    p3.add_argument("--chat-id")
    p3.add_argument("--emit-comment", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        cfg = config()
        base_url = f"https://api.telegram.org/bot{cfg['bot_token']}"
        if args.command == "message":
            chat_id = validate_chat_id(args.chat_id or cfg["default_chat_id"], cfg)
            payload = post_form(base_url, "sendMessage", {"chat_id": chat_id, "text": args.text}, cfg["timeout_seconds"])
            print(json.dumps({"ok": True, "action": "send_message", "target_chat_id": chat_id, "message": "Message sent successfully.", "payload": payload}))
            return 0
        if args.command == "document":
            chat_id = validate_chat_id(args.chat_id or cfg["default_chat_id"], cfg)
            file_path = validate_file_path(args.path, cfg)
            payload = post_multipart(base_url, "sendDocument", {"chat_id": chat_id, "caption": ""}, file_path, cfg["timeout_seconds"])
            print(json.dumps({"ok": True, "action": "send_document", "target_chat_id": chat_id, "message": f"Document sent successfully: {file_path.name}", "payload": payload}))
            return 0
        code, result = run_workflow(args)
        if args.emit_comment:
            result["comment"] = render_comment(result)
        print(json.dumps(result))
        return code
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc), "kind": "runtime"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
