# Guardrails

## Explicit trigger only

This skill must not act on vague phrasing. It should only execute on explicit commands such as:

```text
/telegram-send attachments
/telegram-send attachments to -1001234567890
```

## Attachment-first scope

For V1 production use:
- prefer current-issue attachments or explicit deliverable files
- do not scrape arbitrary workspace files
- do not auto-expand scope beyond the active request

## Safety controls

- allowlist destination chats
- allowlist file extensions
- enforce max file size
- reject missing or empty chat ids
- return structured success/failure output

## Paperclip operations guidance

- read the exact triggering comment first
- prefer wake delta or wake payload over replaying full history
- if acting as assignee, checkout before substantive work
- post one summary comment back into the issue
- use `blocked` only when operator action is truly required
