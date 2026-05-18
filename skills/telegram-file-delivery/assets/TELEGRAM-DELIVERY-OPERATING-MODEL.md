# Telegram Delivery Operating Model

Use explicit issue-comment triggers only:

- `/telegram-send attachments`
- `/telegram-send attachments to -1001234567890`

Execution principles:
- prefer current-issue attachments or explicitly named deliverables
- never send arbitrary workspace files
- send only allowlisted file types
- return exactly one summary comment into the issue
- mark blocked only when operator action is required
