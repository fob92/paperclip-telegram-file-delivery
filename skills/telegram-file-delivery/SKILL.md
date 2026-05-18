---
name: telegram-file-delivery
version: "1.0.1"
description: >
  Deliver explicitly requested issue files or generated deliverables to Telegram
  from Paperclip/OpenClaw using a safe env-configured helper. Optimized for
  UI import, explicit comment triggers, attachment-first delivery, and one
  summary comment back into the issue.
author: openclaw-community
license: MIT
tags:
  - telegram
  - paperclip
  - delivery
  - attachments
  - bot
  - latest

requires:
  env:
    - name: TELEGRAM_BOT_TOKEN
      description: Telegram Bot API token from BotFather
    - name: TELEGRAM_DEFAULT_CHAT_ID
      description: Default destination chat id for deliveries
  optional_env:
    - name: TELEGRAM_ALLOWED_CHAT_IDS
      description: Comma-separated allowlist of permitted destination chat ids
    - name: TELEGRAM_ALLOWED_EXTENSIONS
      description: Comma-separated allowlist of permitted file extensions
    - name: TELEGRAM_MAX_FILE_BYTES
      description: Maximum file size allowed for automatic delivery
    - name: TELEGRAM_TIMEOUT_SECONDS
      description: HTTP timeout in seconds for Telegram API calls
  python_packages: []

security:
  scope: owner-operated
  note: >
    Sends files only to Telegram chats you configure. Uses conservative file and
    chat allowlists and avoids third-party services beyond Telegram Bot API.
  credential_handling: user-supplied-only
  network_access: telegram-bot-api-only
---

# Telegram File Delivery

Use this skill when a Paperclip user explicitly requests that issue files or
final deliverables be sent to Telegram.

This package is designed to be **UI-importable** and **productive by default**:
- no pip install required
- no repo patching after import
- only `.env` configuration should be needed
- direct Python stdlib Telegram Bot API client included in `scripts/telegram_delivery.py`
- end-to-end workflow runner included for trigger parsing, attachment intake, delivery, and summary generation
- layout aligned to the working Paperclip pattern: `skills/<skill>/SKILL.md` plus sibling `scripts/`, `references/`, and `assets/`

## Production-safe trigger

Preferred triggers:

```text
/telegram-send attachments
/telegram-send latest-package
/telegram-send final-package
```

Optional explicit destination override:

```text
/telegram-send attachments to -1001234567890
/telegram-send latest-package to -1001234567890
```

Keep V1 narrow. Do not act on vague requests like "send this somewhere".

## Paperclip best-practice workflow

On comment-driven wakes:

1. Read the exact triggering comment first.
2. Confirm it explicitly requests Telegram delivery.
3. Prefer the comment wake payload / latest comment delta over replaying the full thread.
4. Prefer issue attachments or explicit deliverable files from the current issue.
5. For `latest-package` / `final-package`, resolve files from the latest prior comment that contains a `Delivered package` bullet list.
6. Filter files through the local safety policy.
7. Send only allowed files.
7. Post **one** summary comment back into the issue.
8. If configuration is missing or no safe files exist, comment clearly and set the issue to `blocked` only when operator action is actually required.

## V1 operating scope

For the first production rollout, keep behavior constrained:

- explicit command only
- default destination chat unless an allowlisted override is requested
- attachments-first source selection, with latest-package fallback from prior delivered-package comments
- safe allowlisted file types only
- one final summary comment

## Included local helper

For Paperclip-installed use, prefer the self-contained helper in `scripts/`:

```bash
python scripts/telegram_delivery.py message --text "Telegram delivery is configured."
python scripts/telegram_delivery.py document --path /absolute/path/to/file
python scripts/telegram_delivery.py workflow \
  --comment-text '/telegram-send attachments' \
  --attachments-manifest references/examples/attachments.json \
  --emit-comment
python scripts/telegram_delivery.py workflow \
  --comment-text '/telegram-send latest-package' \
  --package-comment-file references/examples/package-comment.txt \
  --emit-comment
```

For repo-local development, the richer library-backed helper also exists, but installed Paperclip workflows should rely on the self-contained `scripts/telegram_delivery.py` path.

## Supported file types by default

- `.md`
- `.txt`
- `.pdf`
- `.docx`
- `.pptx`
- `.xlsx`
- `.png`
- `.jpg`
- `.jpeg`

## Never auto-send

- `.env`
- private keys
- credential files
- archives unless explicitly approved
- database dumps
- unsupported binaries

## Setup

### 1. Configure env

Add to your runtime env / `.env`:

```dotenv
TELEGRAM_BOT_TOKEN=1234567890:replace-me
TELEGRAM_DEFAULT_CHAT_ID=-1001234567890
TELEGRAM_ALLOWED_CHAT_IDS=-1001234567890
TELEGRAM_ALLOWED_EXTENSIONS=.md,.txt,.pdf,.docx,.pptx,.xlsx,.png,.jpg,.jpeg
TELEGRAM_MAX_FILE_BYTES=50000000
TELEGRAM_TIMEOUT_SECONDS=30
```

The helper auto-loads `.env`, `.env.telegram`, or `.env.paperclip` if present, so the easiest path is usually to add these values to the deployment `.env` already used by Paperclip/OpenClaw.

### 2. Smoke test

```bash
python scripts/telegram_delivery.py message --text "Telegram delivery is configured."
```

## Delivery summary contract

The workflow runner emits machine-readable JSON and can also emit a ready-to-post markdown comment.

After execution, comment back with:

- destination used
- files sent
- files skipped
- any errors
- whether follow-up operator action is needed

## UI import contract

This skill is production-ready only when the full `skills/telegram-file-delivery/` tree is imported and available to the runtime. A UI that imports only the markdown header without the helper files is insufficient.

## Packaged skill files

Primary installed assets live in the sibling directories Paperclip is most likely to preserve:

- `scripts/telegram_delivery.py`
- `assets/TELEGRAM-DELIVERY-OPERATING-MODEL.md`
- `references/docs/install-checklist.md`
- `references/docs/paperclip-ui-install.md`
- `references/docs/guardrails.md`
- `references/docs/rollout.md`
- `references/docs/env-setup.md`
- `references/docs/company-agent-pack.md`
- `references/docs/production-pack.md`
- `references/templates/company/AGENTS.md`
- `references/templates/company/HEARTBEAT.md`
- `references/templates/agents/DELIVERY-AGENT.md`
- `references/templates/agents/REVIEWER.md`
- `references/examples/comment.txt`
- `references/examples/attachments.json`
- `references/examples/package-comment.txt`

## References

- `references/paperclip-integration.md`
- `references/operations.md`
- `references/implementation-plan.md`
- `references/agent-instructions.md`
