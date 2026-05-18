# Paperclip Agent Instructions — Telegram Delivery

Use Telegram delivery only after an explicit user request.

Required trigger:

```text
/telegram-send attachments
```

Prefer the workflow runner:

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow --comment-text '/telegram-send attachments' --attachments-manifest /absolute/path/to/attachments.json --emit-comment
```

Then post one summary comment with sent, skipped, and failed files.
