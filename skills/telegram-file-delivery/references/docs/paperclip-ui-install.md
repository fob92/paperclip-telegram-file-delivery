# Paperclip UI Install

## Goal

Install the Telegram delivery skill through the Paperclip UI with only env configuration outside the UI.

## Import source requirements

Paperclip should import the skill subtree rooted at:
- `skills/telegram-file-delivery/SKILL.md`

Operationally required sibling directories are:
- `scripts/`
- `references/`
- `assets/`

This layout mirrors the working `paperclip-self-improvement` packaging pattern.

## Install steps

1. Open Paperclip UI.
2. Navigate to Skills.
3. Choose **Install from GitHub**.
4. Select the repository that exposes this skill subtree.
5. Verify the preview shows the `telegram-file-delivery` skill metadata.
6. Install the skill.
7. Attach the skill to the target company or agent set.

## Required env after install

```dotenv
TELEGRAM_BOT_TOKEN=...
TELEGRAM_DEFAULT_CHAT_ID=...
TELEGRAM_ALLOWED_CHAT_IDS=...
```

## Smoke tests

```bash
python scripts/telegram_delivery.py message --text "Telegram delivery is configured."
python scripts/telegram_delivery.py workflow --comment-file references/examples/comment.txt --attachments-manifest references/examples/attachments.json --emit-comment
```
