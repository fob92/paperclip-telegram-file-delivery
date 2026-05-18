# telegram-file-delivery

Production-grade Telegram delivery helper for Paperclip/OpenClaw workflows.

## Goals

- easy UI import
- only `.env` changes required
- no extra package install step
- explicit and safe Telegram delivery
- Paperclip best-practice alignment for comment wakes and issue updates

## Contents

- `SKILL.md` — importable skill instructions
- `bin/paperclip_telegram_send.py` — zero-install CLI entrypoint
- `src/paperclip_telegram_delivery/` — Telegram helper library + workflow engine
- `references/` — Paperclip workflow guidance
- `docs/` — install, rollout, release, and guardrail docs
- `examples/` — smoke-test inputs
- `templates/` — reusable instruction fragments
- `tests/` — safety and workflow coverage
- `scripts/validate.sh` — production validation entrypoint

## Zero-install usage

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py message --text "Telegram delivery is configured."
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py document --path /absolute/path/to/file
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow --comment-text '/telegram-send attachments' --attachments-dir /path/to/files --emit-comment
```

## Required env

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_DEFAULT_CHAT_ID`

The helper auto-loads values from `.env`, `.env.telegram`, or `.env.paperclip` if present.

## Optional env

- `TELEGRAM_ALLOWED_CHAT_IDS`
- `TELEGRAM_ALLOWED_EXTENSIONS`
- `TELEGRAM_MAX_FILE_BYTES`
- `TELEGRAM_TIMEOUT_SECONDS`

## UI install contract

For this to be production-ready through the UI, the skill import must preserve the full repository subtree for this skill, not only the top-level `SKILL.md`. This package is self-contained under `skills/telegram-file-delivery/` and requires no additional shell install step.

See `import-contract.json` for the required file set.

## Validation

```bash
bash skills/telegram-file-delivery/scripts/validate.sh
```

## Operational packs

- company guidance: `templates/company/`
- agent guidance: `templates/agents/`
- env handoff: `docs/env-setup.md`
