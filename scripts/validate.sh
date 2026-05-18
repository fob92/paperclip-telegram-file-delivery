#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHONPATH=src python3 -m py_compile src/paperclip_telegram_delivery/*.py bin/paperclip_telegram_send.py
PYTHONPATH=src python3 -m unittest discover -s tests -v

echo "telegram-file-delivery validation passed"
