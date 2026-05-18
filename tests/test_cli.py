import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def _env(self) -> dict[str, str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path("skills/telegram-file-delivery/src").resolve())
        env["TELEGRAM_BOT_TOKEN"] = "token"
        env["TELEGRAM_DEFAULT_CHAT_ID"] = "1"
        return env

    def test_cli_workflow_not_triggered(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as tmp:
            comment = Path(tmp) / "comment.txt"
            comment.write_text("hello")
            proc = subprocess.run(
                [
                    sys.executable,
                    "skills/telegram-file-delivery/bin/paperclip_telegram_send.py",
                    "workflow",
                    "--comment-file",
                    str(comment),
                ],
                cwd=repo_root,
                env=self._env(),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["trigger_matched"])


if __name__ == "__main__":
    unittest.main()
