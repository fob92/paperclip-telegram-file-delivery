from __future__ import annotations

from .filters import FileSafetyError
from .models import DeliveryRequest, DeliveryRunResult, FileOutcome
from .sender import TelegramSender
from .summary import render_issue_comment
from .triggers import parse_trigger


class DeliveryWorkflow:
    def __init__(self, sender: TelegramSender | None = None) -> None:
        self.sender = sender or TelegramSender()

    def run(self, request: DeliveryRequest) -> DeliveryRunResult:
        trigger = parse_trigger(request.comment_text)
        target_chat_id = request.requested_chat_id or trigger.requested_chat_id
        if not trigger.matched:
            return DeliveryRunResult(
                ok=False,
                trigger_matched=False,
                target_chat_id=target_chat_id,
                notes=["No explicit /telegram-send attachments trigger found."],
            )

        result = DeliveryRunResult(
            ok=True,
            trigger_matched=True,
            target_chat_id=target_chat_id or self.sender.config.default_chat_id,
        )

        if not request.attachments:
            result.ok = False
            result.notes.append("No attachments or deliverable files were provided to the workflow.")
            return result

        for attachment in request.attachments:
            try:
                self.sender.send_document(path=attachment.path, chat_id=target_chat_id)
            except FileSafetyError as exc:
                result.skipped.append(
                    FileOutcome(
                        name=attachment.display_name,
                        path=str(attachment.path),
                        status="skipped",
                        reason=str(exc),
                    )
                )
            except Exception as exc:
                result.ok = False
                result.failed.append(
                    FileOutcome(
                        name=attachment.display_name,
                        path=str(attachment.path),
                        status="failed",
                        reason=str(exc),
                    )
                )
            else:
                result.sent.append(
                    FileOutcome(
                        name=attachment.display_name,
                        path=str(attachment.path),
                        status="sent",
                    )
                )

        if not result.sent:
            result.ok = False
        return result

    @staticmethod
    def render_comment(result: DeliveryRunResult) -> str:
        return render_issue_comment(result)
