# Agent Instructions — Telegram Delivery

Use this skill only after an explicit user request to send issue files to Telegram.

## Trigger

Act only on commands like:

```text
/telegram-send attachments
/telegram-send attachments to -1001234567890
```

## Required behavior

1. Read the triggering comment first.
2. Prefer wake delta/new comments over replaying the full thread.
3. Confirm the request explicitly asks for Telegram delivery.
4. Retrieve issue attachments or explicit current-issue deliverables.
5. Filter files using the local safety policy.
6. Prefer the end-to-end workflow command:

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow \
  --comment-text '/telegram-send attachments' \
  --attachments-manifest /absolute/path/to/attachments.json \
  --emit-comment
```

7. Post a single summary comment containing:
   - destination used
   - files sent
   - files skipped
   - any errors
   - whether operator action is needed

## Safety rules

Never send:
- environment files
- private keys
- credential files
- archives unless explicitly approved
- unsupported file types

If no safe files are available, do not send anything. Comment why.
