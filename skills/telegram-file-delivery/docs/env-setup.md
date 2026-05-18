# Env Setup

## Easiest operator path

For the simplest installation, put the Telegram values into the runtime `.env` file already used by your Paperclip/OpenClaw deployment.

Example:

```dotenv
TELEGRAM_BOT_TOKEN=1234567890:replace-me
TELEGRAM_DEFAULT_CHAT_ID=-1001234567890
TELEGRAM_ALLOWED_CHAT_IDS=-1001234567890
TELEGRAM_ALLOWED_EXTENSIONS=.md,.txt,.pdf,.docx,.pptx,.xlsx,.png,.jpg,.jpeg
TELEGRAM_MAX_FILE_BYTES=50000000
TELEGRAM_TIMEOUT_SECONDS=30
```

## Automatic loading behavior

This skill now auto-loads env values from the first matching file found while walking upward from the current working directory:

- `.env`
- `.env.telegram`
- `.env.paperclip`

That means you can often install through the UI and then only add the env values to your existing deployment `.env` file without any extra shell install steps.

## Important note

Existing real environment variables win over values loaded from `.env` files.
