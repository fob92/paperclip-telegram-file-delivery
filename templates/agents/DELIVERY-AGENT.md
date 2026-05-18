# Delivery Agent Addendum — Telegram Delivery

Use the `telegram-file-delivery` skill only after an explicit request.

## Trigger

```text
/telegram-send attachments
/telegram-send attachments to -1001234567890
```

## Execution

Prefer the workflow runner:

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow \
  --comment-file /tmp/trigger-comment.txt \
  --attachments-manifest /tmp/attachments.json \
  --emit-comment
```

## Required behavior

- send only safe attachments
- honor chat allowlist restrictions
- return one summary comment
- if nothing safe is available, comment clearly and do not send anything
