# Security

## Supported scope

This skill is intended for owner-operated Paperclip/OpenClaw deployments.

## Guardrails

- explicit trigger only: `/telegram-send attachments`
- allowlisted destination chats
- allowlisted file extensions
- size cap for automatic sends
- no secrets or credential files should ever be sent
- one summary comment back into the issue

## Operator responsibilities

- protect `TELEGRAM_BOT_TOKEN`
- restrict bot membership to intended chats
- keep `TELEGRAM_ALLOWED_CHAT_IDS` narrow in production
- review any extension allowlist expansion carefully

## Reporting

If you find a vulnerability in the delivery flow, do not post secrets publicly. Share a sanitized report with impact, reproduction steps, and recommended mitigation.
