from __future__ import annotations

import argparse
import json
import sys

from .attachments import attachments_from_directory, attachments_from_manifest, attachments_from_paths
from .filters import FileSafetyError
from .models import DeliveryRequest
from .sender import TelegramSender
from .summary import render_issue_comment
from .workflow import DeliveryWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="paperclip-telegram-send",
        description="Send messages or documents to Telegram using env-based configuration.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    message_parser = subparsers.add_parser("message", help="Send a text message")
    message_parser.add_argument("--text", required=True, help="Message text to send")
    message_parser.add_argument("--chat-id", help="Override TELEGRAM_DEFAULT_CHAT_ID")

    document_parser = subparsers.add_parser("document", help="Send a document/file")
    document_parser.add_argument("--path", required=True, help="Path to the file to send")
    document_parser.add_argument("--chat-id", help="Override TELEGRAM_DEFAULT_CHAT_ID")
    document_parser.add_argument("--caption", help="Optional Telegram caption")

    workflow_parser = subparsers.add_parser(
        "workflow",
        help="Run the end-to-end Telegram delivery workflow for a comment trigger",
    )
    workflow_parser.add_argument("--comment-text", help="Exact triggering comment text")
    workflow_parser.add_argument("--comment-file", help="Path to a file containing the triggering comment")
    workflow_parser.add_argument("--attachment", action="append", default=[], help="Attachment path (repeatable)")
    workflow_parser.add_argument("--attachments-dir", help="Directory containing attachments to consider")
    workflow_parser.add_argument("--attachments-manifest", help="JSON file listing attachments")
    workflow_parser.add_argument("--chat-id", help="Optional explicit destination override")
    workflow_parser.add_argument("--emit-comment", action="store_true", help="Also emit a ready-to-post markdown summary comment")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        sender = TelegramSender()
        if args.command == "message":
            result = sender.send_message(text=args.text, chat_id=args.chat_id)
        elif args.command == "document":
            result = sender.send_document(
                path=args.path,
                chat_id=args.chat_id,
                caption=args.caption,
            )
        elif args.command == "workflow":
            comment_text = args.comment_text or ""
            if args.comment_file:
                with open(args.comment_file, "r", encoding="utf-8") as handle:
                    comment_text = handle.read()
            attachments = []
            attachments.extend(attachments_from_paths(args.attachment))
            if args.attachments_dir:
                attachments.extend(attachments_from_directory(args.attachments_dir))
            if args.attachments_manifest:
                attachments.extend(attachments_from_manifest(args.attachments_manifest))
            workflow = DeliveryWorkflow(sender=sender)
            workflow_result = workflow.run(
                DeliveryRequest(
                    comment_text=comment_text,
                    attachments=attachments,
                    requested_chat_id=args.chat_id,
                )
            )
            payload = workflow_result.to_dict()
            if args.emit_comment:
                payload["comment"] = render_issue_comment(workflow_result)
            print(json.dumps(payload))
            return 0 if workflow_result.ok else 1
        else:  # pragma: no cover - argparse guards this
            parser.error(f"Unsupported command: {args.command}")
            return 2
    except FileSafetyError as exc:
        print(json.dumps({"ok": False, "error": str(exc), "kind": "safety"}))
        return 10
    except Exception as exc:  # pragma: no cover - CLI boundary
        print(json.dumps({"ok": False, "error": str(exc), "kind": "runtime"}))
        return 1

    print(
        json.dumps(
            {
                "ok": result.ok,
                "action": result.action,
                "target_chat_id": result.target_chat_id,
                "message": result.message,
            }
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
