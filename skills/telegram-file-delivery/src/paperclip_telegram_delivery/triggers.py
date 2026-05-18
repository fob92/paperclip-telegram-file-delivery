from __future__ import annotations

import re
from dataclasses import dataclass

_TRIGGER_RE = re.compile(
    r"(?:^|\n)\s*(?:telegram-send|send\s+to\s+telegram)\s+(?P<mode>attachments|latest-files|latest-package|final-package)(?:\s+to\s+(?P<chat>-?\d+))?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


@dataclass(slots=True)
class TriggerMatch:
    matched: bool
    requested_chat_id: str | None = None
    mode: str | None = None


def parse_trigger(comment_text: str) -> TriggerMatch:
    match = _TRIGGER_RE.search(comment_text or "")
    if not match:
        return TriggerMatch(matched=False)
    return TriggerMatch(matched=True, requested_chat_id=match.group("chat"), mode=match.group("mode").lower())
