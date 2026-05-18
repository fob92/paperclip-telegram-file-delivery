import unittest

from paperclip_telegram_delivery.config import TelegramConfig
from paperclip_telegram_delivery.filters import FileSafetyError, validate_chat_id


class ConfigTests(unittest.TestCase):
    def test_config_normalizes_extensions(self) -> None:
        import os

        old = dict(os.environ)
        try:
            os.environ["TELEGRAM_BOT_TOKEN"] = "token"
            os.environ["TELEGRAM_DEFAULT_CHAT_ID"] = "1"
            os.environ["TELEGRAM_ALLOWED_EXTENSIONS"] = "md,.pdf"
            cfg = TelegramConfig.from_env()
            self.assertIn(".md", cfg.allowed_extensions)
            self.assertIn(".pdf", cfg.allowed_extensions)
        finally:
            os.environ.clear()
            os.environ.update(old)

    def test_validate_chat_id_enforces_allowlist(self) -> None:
        cfg = TelegramConfig(
            bot_token="token",
            default_chat_id="1",
            allowed_chat_ids={"2"},
            allowed_extensions={".md"},
            max_file_bytes=100,
            timeout_seconds=30,
        )
        with self.assertRaises(FileSafetyError):
            validate_chat_id("1", cfg)


if __name__ == "__main__":
    unittest.main()
