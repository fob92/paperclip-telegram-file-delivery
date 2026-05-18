import tempfile
import unittest
from pathlib import Path

from paperclip_telegram_delivery.config import TelegramConfig
from paperclip_telegram_delivery.filters import FileSafetyError, validate_file_path


class FilterTests(unittest.TestCase):
    def test_validate_file_path_allows_safe_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "note.md"
            file_path.write_text("hello")
            config = TelegramConfig(
                bot_token="token",
                default_chat_id="1",
                allowed_chat_ids=set(),
                allowed_extensions={".md"},
                max_file_bytes=1024,
                timeout_seconds=30,
            )
            validated = validate_file_path(file_path, config)
            self.assertEqual(validated, file_path.resolve())

    def test_validate_file_path_rejects_unsupported_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "secrets.json"
            file_path.write_text("{}")
            config = TelegramConfig(
                bot_token="token",
                default_chat_id="1",
                allowed_chat_ids=set(),
                allowed_extensions={".md"},
                max_file_bytes=1024,
                timeout_seconds=30,
            )
            with self.assertRaises(FileSafetyError):
                validate_file_path(file_path, config)


if __name__ == "__main__":
    unittest.main()
