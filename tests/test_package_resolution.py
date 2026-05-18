import tempfile
import unittest
from pathlib import Path

PACKAGE_COMMENT = """Closed after independent Round 3 approval on [PRO-64](/issues/201ad06f-a41e-4c61-a509-9ab4642cae6c). The approving review is comment eef143dc-e5b5-400b-905a-3f900215d69f.\n\nDelivered package\n- cto/PRO-65-final-teaching-script.md\n- cto/PRO-65-self-study-slides.md\n- cto/PRO-65-final-package-manifest.md\n\nApproval outcome\n- ok\n"""

from importlib.util import module_from_spec, spec_from_file_location

MODULE_PATH = Path(__file__).resolve().parents[1] / "skills/telegram-file-delivery/scripts/telegram_delivery.py"
spec = spec_from_file_location("telegram_delivery", MODULE_PATH)
telegram_delivery = module_from_spec(spec)
spec.loader.exec_module(telegram_delivery)


class PackageResolutionTests(unittest.TestCase):
    def test_extract_delivered_package_paths(self) -> None:
        paths = telegram_delivery.extract_delivered_package_paths(PACKAGE_COMMENT)
        self.assertEqual(paths, [
            "cto/PRO-65-final-teaching-script.md",
            "cto/PRO-65-self-study-slides.md",
            "cto/PRO-65-final-package-manifest.md",
        ])

    def test_parse_trigger_latest_files(self) -> None:
        matched, chat, mode = telegram_delivery.parse_trigger("telegram-send latest-files")
        self.assertTrue(matched)
        self.assertIsNone(chat)
        self.assertEqual(mode, "latest-files")


if __name__ == "__main__":
    unittest.main()
