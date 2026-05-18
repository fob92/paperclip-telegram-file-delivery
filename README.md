# paperclip-telegram-file-delivery

Production-ready Telegram delivery skill for Paperclip/OpenClaw.

## Paperclip-compatible layout

This repository is intentionally structured like the working `paperclip-self-improvement` repo:

```text
skills/
  telegram-file-delivery/
    SKILL.md
    scripts/
    references/
    assets/
```

That layout is important because Paperclip UI skill import appears to preserve the skill markdown and its expected sibling skill directories more reliably than arbitrary repo-root helper trees.

## Install in Paperclip

Use the Paperclip UI with:

`https://github.com/fob92/paperclip-telegram-file-delivery`

Paperclip should discover the skill at:

`skills/telegram-file-delivery/SKILL.md`

and include sibling files from that same skill directory.

## Runtime path to use after install

For the installed skill, prefer the self-contained helper:

```bash
python scripts/telegram_delivery.py workflow --comment-file references/examples/comment.txt --attachments-manifest references/examples/attachments.json --emit-comment
```

## Why this repo was reworked

A previous root-level layout resulted in UI installation that surfaced only the skill markdown. This repo now follows the stronger Paperclip pattern used by the other install-oriented repositories.
