# Paperclip UI Install

## Goal

Install the Telegram delivery skill through the Paperclip UI with only env configuration outside the UI.

## Import source requirements

Paperclip must import the full skill tree, including:
- `SKILL.md`
- `bin/`
- `src/`
- `references/`
- `examples/`
- `docs/`

If the UI only imports markdown metadata and not the helper files, installation is incomplete.

## Install steps

1. Open Paperclip UI.
2. Navigate to Skills.
3. Choose **Install from GitHub**.
4. Select the repository or subtree that exposes this skill root.
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
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py message --text "Telegram delivery is configured."
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow --comment-file skills/telegram-file-delivery/examples/comment.txt --attachments-manifest skills/telegram-file-delivery/examples/attachments.json --emit-comment
```
