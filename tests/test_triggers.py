import unittest

from paperclip_telegram_delivery.triggers import parse_trigger


class TriggerTests(unittest.TestCase):
    def test_parse_trigger_basic(self) -> None:
        match = parse_trigger("/telegram-send attachments")
        self.assertTrue(match.matched)
        self.assertIsNone(match.requested_chat_id)

    def test_parse_trigger_with_chat_override(self) -> None:
        match = parse_trigger("please do this\n/telegram-send attachments to -100123\nthanks")
        self.assertTrue(match.matched)
        self.assertEqual(match.requested_chat_id, "-100123")

    def test_parse_trigger_ignores_non_explicit_text(self) -> None:
        match = parse_trigger("can you telegram-send attachments maybe?")
        self.assertFalse(match.matched)


if __name__ == "__main__":
    unittest.main()
