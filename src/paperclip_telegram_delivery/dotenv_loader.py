from __future__ import annotations

import os
from pathlib import Path


CANDIDATE_FILES = (
    ".env",
    ".env.telegram",
    ".env.paperclip",
)


def load_dotenv_if_present(start_dir: str | Path | None = None) -> str | None:
    root = Path(start_dir or Path.cwd()).resolve()
    search_dirs = [root, *root.parents]

    for directory in search_dirs:
        for filename in CANDIDATE_FILES:
            candidate = directory / filename
            if candidate.exists() and candidate.is_file():
                _load_file(candidate)
                return str(candidate)
    return None


def _load_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
