# Paperclip Integration Guide

## Goal

Deliver issue-related files to Telegram with minimal operator work and strong Paperclip hygiene.

## Recommended model

Use this skill as a reusable company skill or imported repo skill. Do not create a dedicated Telegram specialist agent for V1 unless delivery volume justifies it.

## Comment-wake procedure

When a comment wake arrives:

1. Read the exact triggering comment first.
2. If wake payload or comment delta is available, use that before replaying the full thread.
3. Continue only if the comment explicitly requests Telegram delivery.
4. Checkout the issue before substantive work if you are the acting assignee.
5. Prefer issue attachments or explicit deliverable paths from the current issue.
6. Download or materialize the files locally if your environment requires it.
7. Run the workflow helper with the exact comment and attachment inputs.
8. Post one summary comment back into the issue.
9. Set `blocked` only when missing env/config/operator action truly prevents delivery.

## Preferred trigger grammar

### V1

```text
/telegram-send attachments
```

### Optional V1 destination override

```text
/telegram-send attachments to -1001234567890
```

## Suggested success comment

```md
Telegram delivery completed.

Destination: -1001234567890
Sent files:
- concept-outline.md
- lecture-plan.pdf

Skipped files:
- secrets.json (unsupported extension)
```

## Suggested failure comment

```md
Telegram delivery could not proceed.

Reason:
- TELEGRAM_BOT_TOKEN is not configured in the runtime env

Next action:
- operator must add the env value and rerun the request
```

## CLI invocation

Single-file send:

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py document --path /path/to/file
```

End-to-end workflow:

```bash
python skills/telegram-file-delivery/bin/paperclip_telegram_send.py workflow \
  --comment-text '/telegram-send attachments' \
  --attachments-manifest /path/to/attachments.json \
  --emit-comment
```
