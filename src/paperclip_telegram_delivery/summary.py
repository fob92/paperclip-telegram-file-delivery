from __future__ import annotations

from .models import DeliveryRunResult, FileOutcome


def _bullet_lines(items: list[FileOutcome]) -> list[str]:
    if not items:
        return ["- none"]
    lines = []
    for item in items:
        suffix = f" ({item.reason})" if item.reason else ""
        lines.append(f"- {item.name}{suffix}")
    return lines


def render_issue_comment(result: DeliveryRunResult) -> str:
    lines = []
    if result.ok:
        lines.append("Telegram delivery completed.")
    elif not result.trigger_matched:
        lines.append("Telegram delivery not triggered.")
    else:
        lines.append("Telegram delivery could not complete cleanly.")

    if result.target_chat_id:
        lines.extend(["", f"Destination: {result.target_chat_id}"])

    lines.extend(["", "Sent files:"])
    lines.extend(_bullet_lines(result.sent))
    lines.extend(["", "Skipped files:"])
    lines.extend(_bullet_lines(result.skipped))
    lines.extend(["", "Failed files:"])
    lines.extend(_bullet_lines(result.failed))

    if result.notes:
        lines.extend(["", "Notes:"])
        lines.extend(f"- {note}" for note in result.notes)

    return "\n".join(lines)
