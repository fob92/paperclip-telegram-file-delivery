from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DeliveryResult:
    ok: bool
    action: str
    target_chat_id: str
    message: str
    payload: dict[str, Any] | None = None
