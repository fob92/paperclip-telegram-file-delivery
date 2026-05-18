#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_ROOT/../.." && pwd)"
cd "$REPO_ROOT"

PYTHONPATH="$SKILL_ROOT/src" python3 -m py_compile "$SKILL_ROOT"/src/paperclip_telegram_delivery/*.py "$SKILL_ROOT"/bin/paperclip_telegram_send.py "$SKILL_ROOT"/scripts/telegram_delivery.py
PYTHONPATH="$SKILL_ROOT/src" python3 -m unittest discover -s tests -v

echo "telegram-file-delivery validation passed"
