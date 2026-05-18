---
name: telegram-file-delivery
description: Deliver explicitly requested issue files to Telegram using a configured bot and a safe local helper.
---

# Telegram File Delivery

Trigger on explicit commands only:

```text
/telegram-send attachments
```

Workflow:
1. read the triggering comment
2. confirm delivery was explicitly requested
3. retrieve attachments
4. filter for safe files
5. send each safe file with the local helper
6. comment one summary back into the issue
