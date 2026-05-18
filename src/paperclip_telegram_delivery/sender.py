from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from urllib import error, parse, request

from .config import TelegramConfig
from .filters import validate_chat_id, validate_file_path
from .result import DeliveryResult


class TelegramSender:
    """Thin Telegram Bot API wrapper using Python stdlib only."""

    def __init__(self, config: TelegramConfig | None = None) -> None:
        self.config = config or TelegramConfig.from_env()
        self.base_url = f"https://api.telegram.org/bot{self.config.bot_token}"

    def send_message(self, text: str, chat_id: str | None = None) -> DeliveryResult:
        target_chat_id = validate_chat_id(chat_id or self.config.default_chat_id, self.config)
        payload = self._post_form(
            endpoint="sendMessage",
            fields={"chat_id": target_chat_id, "text": text},
        )
        return DeliveryResult(
            ok=True,
            action="send_message",
            target_chat_id=target_chat_id,
            message="Message sent successfully.",
            payload=payload,
        )

    def send_document(
        self,
        path: str | Path,
        chat_id: str | None = None,
        caption: str | None = None,
    ) -> DeliveryResult:
        target_chat_id = validate_chat_id(chat_id or self.config.default_chat_id, self.config)
        file_path = validate_file_path(path, self.config)
        payload = self._post_multipart(
            endpoint="sendDocument",
            fields={"chat_id": target_chat_id, "caption": caption or ""},
            file_field="document",
            file_path=file_path,
        )
        return DeliveryResult(
            ok=True,
            action="send_document",
            target_chat_id=target_chat_id,
            message=f"Document sent successfully: {file_path.name}",
            payload=payload,
        )

    def _post_form(self, endpoint: str, fields: dict[str, str]) -> dict:
        data = parse.urlencode(fields).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/{endpoint}",
            data=data,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._execute(req)

    def _post_multipart(
        self,
        endpoint: str,
        fields: dict[str, str],
        file_field: str,
        file_path: Path,
    ) -> dict:
        boundary = "----OpenClawTelegramBoundary7MA4YWxkTrZu0gW"
        body = bytearray()

        for key, value in fields.items():
            body.extend(f"--{boundary}\r\n".encode())
            body.extend(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode())
            body.extend(str(value).encode())
            body.extend(b"\r\n")

        mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        with file_path.open("rb") as handle:
            content = handle.read()

        body.extend(f"--{boundary}\r\n".encode())
        body.extend(
            (
                f'Content-Disposition: form-data; name="{file_field}"; '
                f'filename="{file_path.name}"\r\n'
            ).encode()
        )
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode())
        body.extend(content)
        body.extend(b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode())

        req = request.Request(
            url=f"{self.base_url}/{endpoint}",
            data=bytes(body),
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        return self._execute(req)

    def _execute(self, req: request.Request) -> dict:
        try:
            with request.urlopen(req, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:  # pragma: no cover - network boundary
            raw = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Telegram API HTTP {exc.code}: {raw}") from exc
        except error.URLError as exc:  # pragma: no cover - network boundary
            raise RuntimeError(f"Telegram API connection failed: {exc.reason}") from exc

        if not payload.get("ok"):
            raise RuntimeError(f"Telegram API returned failure: {payload}")
        return payload
