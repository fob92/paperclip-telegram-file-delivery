import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE_COMMENT = """Closed after independent Round 3 approval on [PRO-64](/issues/201ad06f-a41e-4c61-a509-9ab4642cae6c). The approving review is comment eef143dc-e5b5-400b-905a-3f900215d69f.\n\nDelivered package\n- cto/PRO-65-final-teaching-script.md\n- cto/PRO-65-self-study-slides.md\n- cto/PRO-65-final-package-manifest.md\n\nApproval outcome\n- ok\n"""


class PackagedScriptTests(unittest.TestCase):
    def _env(self) -> dict[str, str]:
        env = os.environ.copy()
        env["TELEGRAM_BOT_TOKEN"] = "token"
        env["TELEGRAM_DEFAULT_CHAT_ID"] = "1"
        return env

    def test_packaged_script_workflow_not_triggered(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            comment = Path(tmp) / "comment.txt"
            comment.write_text("hello")
            proc = subprocess.run(
                [
                    sys.executable,
                    "skills/telegram-file-delivery/scripts/telegram_delivery.py",
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

    def test_packaged_script_resolves_latest_package_without_explicit_attachments(self) -> None:
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cto = root / "cto"
            cto.mkdir()
            for name in [
                "PRO-65-final-teaching-script.md",
                "PRO-65-self-study-slides.md",
                "PRO-65-final-package-manifest.md",
            ]:
                (cto / name).write_text("x")
            trigger = root / "trigger.txt"
            trigger.write_text("telegram-send latest-files")
            package = root / "package.txt"
            package.write_text(PACKAGE_COMMENT)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(repo_root / "skills/telegram-file-delivery/scripts/telegram_delivery.py"),
                    "workflow",
                    "--comment-file",
                    str(trigger),
                    "--package-comment-file",
                    str(package),
                    "--emit-comment",
                ],
                cwd=root,
                env=self._env(),
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(proc.returncode, 1)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["trigger_matched"])
        self.assertEqual(payload["mode"], "latest-files")
        self.assertIn("Resolved files from the latest delivered package comment.", payload["notes"])
        self.assertEqual(len(payload["failed"]), 3)


if __name__ == "__main__":
    unittest.main()
