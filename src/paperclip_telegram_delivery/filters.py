from __future__ import annotations

from pathlib import Path

from .config import TelegramConfig


class FileSafetyError(ValueError):
    """Raised when a file is not eligible for automatic Telegram delivery."""


def validate_chat_id(chat_id: str, config: TelegramConfig) -> str:
    normalized = str(chat_id).strip()
    if not normalized:
        raise FileSafetyError("Target chat id is empty")
    if config.allowed_chat_ids and normalized not in config.allowed_chat_ids:
        raise FileSafetyError(f"Chat id {normalized} is not in TELEGRAM_ALLOWED_CHAT_IDS")
    return normalized


def validate_file_path(path: str | Path, config: TelegramConfig) -> Path:
    file_path = Path(path).expanduser().resolve()
    if not file_path.exists():
        raise FileSafetyError(f"File does not exist: {file_path}")
    if not file_path.is_file():
        raise FileSafetyError(f"Path is not a file: {file_path}")

    extension = file_path.suffix.lower()
    if extension not in config.allowed_extensions:
        raise FileSafetyError(
            f"Extension {extension or '<none>'} is not allowed. "
            f"Allowed: {sorted(config.allowed_extensions)}"
        )

    size = file_path.stat().st_size
    if size > config.max_file_bytes:
        raise FileSafetyError(
            f"File too large: {size} bytes exceeds TELEGRAM_MAX_FILE_BYTES={config.max_file_bytes}"
        )

    return file_path
