from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AttachmentItem:
    path: Path
    name: str | None = None
    source: str = "local"

    @property
    def display_name(self) -> str:
        return self.name or self.path.name


@dataclass(slots=True)
class DeliveryRequest:
    comment_text: str
    attachments: list[AttachmentItem] = field(default_factory=list)
    requested_chat_id: str | None = None


@dataclass(slots=True)
class FileOutcome:
    name: str
    path: str
    status: str
    reason: str | None = None


@dataclass(slots=True)
class DeliveryRunResult:
    ok: bool
    trigger_matched: bool
    target_chat_id: str | None
    sent: list[FileOutcome] = field(default_factory=list)
    skipped: list[FileOutcome] = field(default_factory=list)
    failed: list[FileOutcome] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "trigger_matched": self.trigger_matched,
            "target_chat_id": self.target_chat_id,
            "sent": [vars(x) for x in self.sent],
            "skipped": [vars(x) for x in self.skipped],
            "failed": [vars(x) for x in self.failed],
            "notes": self.notes,
        }
