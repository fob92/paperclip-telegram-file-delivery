from __future__ import annotations

import json
from pathlib import Path

from .models import AttachmentItem


def attachments_from_paths(paths: list[str]) -> list[AttachmentItem]:
    return [AttachmentItem(path=Path(p).expanduser().resolve()) for p in paths]


def attachments_from_directory(directory: str) -> list[AttachmentItem]:
    root = Path(directory).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Attachment directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Attachment directory is not a directory: {root}")
    return [AttachmentItem(path=p.resolve()) for p in sorted(root.iterdir()) if p.is_file()]


def attachments_from_manifest(manifest_path: str) -> list[AttachmentItem]:
    path = Path(manifest_path).expanduser().resolve()
    payload = json.loads(path.read_text())
    items = payload.get("attachments", payload)
    output: list[AttachmentItem] = []
    for item in items:
        if isinstance(item, str):
            output.append(AttachmentItem(path=Path(item).expanduser().resolve()))
            continue
        output.append(
            AttachmentItem(
                path=Path(item["path"]).expanduser().resolve(),
                name=item.get("name"),
                source=item.get("source", "manifest"),
            )
        )
    return output
