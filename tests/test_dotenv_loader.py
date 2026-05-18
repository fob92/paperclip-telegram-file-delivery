import os
import tempfile
import unittest
from pathlib import Path

from paperclip_telegram_delivery.dotenv_loader import load_dotenv_if_present


class DotenvTests(unittest.TestCase):
    def test_loads_env_file_when_present(self) -> None:
        old = dict(os.environ)
        try:
            with tempfile.TemporaryDirectory() as tmp:
                env_path = Path(tmp) / ".env"
                env_path.write_text("TELEGRAM_BOT_TOKEN=abc\nTELEGRAM_DEFAULT_CHAT_ID=123\n")
                os.environ.pop("TELEGRAM_BOT_TOKEN", None)
                os.environ.pop("TELEGRAM_DEFAULT_CHAT_ID", None)
                found = load_dotenv_if_present(tmp)
                self.assertEqual(found, str(env_path))
                self.assertEqual(os.environ["TELEGRAM_BOT_TOKEN"], "abc")
                self.assertEqual(os.environ["TELEGRAM_DEFAULT_CHAT_ID"], "123")
        finally:
            os.environ.clear()
            os.environ.update(old)


if __name__ == "__main__":
    unittest.main()
