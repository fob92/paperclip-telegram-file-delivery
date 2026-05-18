import tempfile
import unittest
from pathlib import Path

from paperclip_telegram_delivery.models import AttachmentItem, DeliveryRequest
from paperclip_telegram_delivery.summary import render_issue_comment
from paperclip_telegram_delivery.workflow import DeliveryWorkflow


class FakeSender:
    class Config:
        default_chat_id = "default-chat"

    def __init__(self) -> None:
        self.config = self.Config()
        self.sent = []

    def send_document(self, path, chat_id=None):
        p = Path(path)
        self.sent.append((str(p), chat_id))
        return {"ok": True}


class FakeSafetySender(FakeSender):
    def send_document(self, path, chat_id=None):
        p = Path(path)
        if p.suffix == ".json":
            from paperclip_telegram_delivery.filters import FileSafetyError

            raise FileSafetyError("Extension .json is not allowed")
        return super().send_document(path, chat_id)


class WorkflowTests(unittest.TestCase):
    def test_workflow_sends_safe_files_and_skips_unsafe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "report.md"
            md.write_text("ok")
            js = Path(tmp) / "secrets.json"
            js.write_text("{}")
            workflow = DeliveryWorkflow(sender=FakeSafetySender())
            result = workflow.run(
                DeliveryRequest(
                    comment_text="/telegram-send attachments to -1001",
                    attachments=[AttachmentItem(path=md), AttachmentItem(path=js)],
                )
            )
            self.assertTrue(result.ok)
            self.assertEqual(result.target_chat_id, "-1001")
            self.assertEqual([x.name for x in result.sent], ["report.md"])
            self.assertEqual([x.name for x in result.skipped], ["secrets.json"])

    def test_workflow_returns_not_triggered_when_comment_missing(self) -> None:
        workflow = DeliveryWorkflow(sender=FakeSender())
        result = workflow.run(DeliveryRequest(comment_text="please send maybe later"))
        self.assertFalse(result.ok)
        self.assertFalse(result.trigger_matched)

    def test_render_issue_comment_contains_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "report.md"
            md.write_text("ok")
            workflow = DeliveryWorkflow(sender=FakeSender())
            result = workflow.run(
                DeliveryRequest(
                    comment_text="/telegram-send attachments",
                    attachments=[AttachmentItem(path=md)],
                )
            )
            comment = render_issue_comment(result)
            self.assertIn("Telegram delivery completed.", comment)
            self.assertIn("Sent files:", comment)
            self.assertIn("report.md", comment)


if __name__ == "__main__":
    unittest.main()
