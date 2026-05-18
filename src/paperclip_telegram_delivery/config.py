from __future__ import annotations

import os
from dataclasses import dataclass

from .dotenv_loader import load_dotenv_if_present


DEFAULT_ALLOWED_EXTENSIONS = ".md,.txt,.pdf,.docx,.pptx,.xlsx,.png,.jpg,.jpeg"


@dataclass(slots=True)
class TelegramConfig:
    """Runtime configuration loaded from environment variables."""

    bot_token: str
    default_chat_id: str
    allowed_chat_ids: set[str]
    allowed_extensions: set[str]
    max_file_bytes: int
    timeout_seconds: int

    @classmethod
    def from_env(cls) -> "TelegramConfig":
        load_dotenv_if_present()
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        default_chat_id = os.environ.get("TELEGRAM_DEFAULT_CHAT_ID", "").strip()
        allowed_chat_ids_raw = os.environ.get("TELEGRAM_ALLOWED_CHAT_IDS", "").strip()
        allowed_extensions_raw = os.environ.get(
            "TELEGRAM_ALLOWED_EXTENSIONS",
            DEFAULT_ALLOWED_EXTENSIONS,
        ).strip()
        max_file_bytes = int(os.environ.get("TELEGRAM_MAX_FILE_BYTES", "50000000"))
        timeout_seconds = int(os.environ.get("TELEGRAM_TIMEOUT_SECONDS", "30"))

        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not default_chat_id:
            raise ValueError("TELEGRAM_DEFAULT_CHAT_ID is required")
        if max_file_bytes <= 0:
            raise ValueError("TELEGRAM_MAX_FILE_BYTES must be > 0")
        if timeout_seconds <= 0:
            raise ValueError("TELEGRAM_TIMEOUT_SECONDS must be > 0")

        allowed_chat_ids = {
            item.strip() for item in allowed_chat_ids_raw.split(",") if item.strip()
        }
        allowed_extensions = {
            (item if item.startswith(".") else f".{item}").strip().lower()
            for item in allowed_extensions_raw.split(",")
            if item.strip()
        }

        return cls(
            bot_token=bot_token,
            default_chat_id=default_chat_id,
            allowed_chat_ids=allowed_chat_ids,
            allowed_extensions=allowed_extensions,
            max_file_bytes=max_file_bytes,
            timeout_seconds=timeout_seconds,
        )
