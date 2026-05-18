# Company AGENTS.md — Telegram Delivery Pack

This company may use the `telegram-file-delivery` skill to send current-issue attachments or generated deliverables to Telegram.

## Allowed usage

Telegram delivery is allowed only when explicitly requested in an issue comment:

```text
/telegram-send attachments
/telegram-send attachments to -1001234567890
```

## Company-wide rules

- only explicit trigger comments may cause delivery
- prefer current-issue attachments or explicitly named deliverables
- do not send arbitrary workspace files
- do not send secrets, credentials, keys, archives, or unsupported types
- post exactly one delivery summary comment back into the issue
- set `blocked` only when operator action is required, such as missing env configuration

## Workflow expectation

1. read the exact triggering comment first
2. prefer wake delta / wake payload over replaying the full thread
3. if acting as assignee, checkout before substantive work
4. run the Telegram workflow helper
5. return one summary comment with sent/skipped/failed files
