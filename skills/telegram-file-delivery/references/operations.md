# Operations Guide

## Setup

1. Create a Telegram bot with @BotFather.
2. Invite the bot to the target group or message it directly.
3. Record the destination `chat_id`.
4. Add env values.
5. Smoke-test with the included helper.

## Env values

```dotenv
TELEGRAM_BOT_TOKEN=...
TELEGRAM_DEFAULT_CHAT_ID=...
TELEGRAM_ALLOWED_CHAT_IDS=...
TELEGRAM_ALLOWED_EXTENSIONS=.md,.txt,.pdf,.docx,.pptx,.xlsx,.png,.jpg,.jpeg
TELEGRAM_MAX_FILE_BYTES=50000000
TELEGRAM_TIMEOUT_SECONDS=30
```

## Smoke tests

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py message --text "Telegram delivery is configured."
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py document --path skills/telegram-file-delivery/README.md
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow --comment-text '/telegram-send attachments' --attachment skills/telegram-file-delivery/README.md --emit-comment
```

## Common failures

### TELEGRAM_BOT_TOKEN missing
Add the token to the runtime env and restart the worker/runtime if required.

### 400 chat not found / bot blocked
Confirm the bot is a member of the target chat and the `chat_id` is correct.

### chat id not allowed
Add the destination to `TELEGRAM_ALLOWED_CHAT_IDS` or remove the allowlist if intentionally unrestricted.

### unsupported extension
Add the file extension to `TELEGRAM_ALLOWED_EXTENSIONS` only if it is safe.

### file too large
Increase `TELEGRAM_MAX_FILE_BYTES` deliberately or send a smaller artifact.
