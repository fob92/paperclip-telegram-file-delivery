# telegram-file-delivery

Production-grade Telegram delivery helper for Paperclip/OpenClaw workflows.

## Paperclip-compatible layout

This skill is intentionally packaged like the working `paperclip-self-improvement` repository pattern:

```text
skills/
  telegram-file-delivery/
    SKILL.md
    scripts/
    references/
    assets/
```

The reason is practical: a previous root-level layout resulted in a UI installation that surfaced `SKILL.md` but not the helper files. This revised layout keeps operationally relevant files inside the expected skill subtree.

Version: `1.0.1`

## Installed runtime path

After Paperclip UI installation, prefer the self-contained helper:

```bash
python scripts/telegram_delivery.py workflow --comment-file references/examples/comment.txt --attachments-manifest references/examples/attachments.json --emit-comment
python scripts/telegram_delivery.py workflow --comment-text 'telegram-send latest-files' --package-comment-file references/examples/package-comment.txt --emit-comment
```

## Companion workflow: TweetClaw reports

OpenClaw agents can collect X/Twitter context with
[TweetClaw](https://github.com/Xquik-dev/tweetclaw), then use this skill to
deliver only reviewed files:

```bash
openclaw plugins install @xquik/tweetclaw
```

Use TweetClaw to search tweets, search tweet replies, export followers, look up
users, monitor tweets, route webhooks, or prepare giveaway draw results. Save the
reviewed summary, CSV, PDF, image, or report as an issue attachment, then run
Telegram delivery only after an explicit `telegram-send attachments` or
`telegram-send latest-files` comment. Keep post tweets, post tweet replies,
direct messages, media upload, and media download behind operator review before
any Telegram delivery.

## What is inside

- `SKILL.md` — importable skill instructions
- `scripts/telegram_delivery.py` — self-contained installed runtime
- `references/docs/` — install, rollout, guardrail, and env docs
- `references/templates/` — company and agent integration templates
- `references/examples/` — smoke-test files
- `assets/TELEGRAM-DELIVERY-OPERATING-MODEL.md` — compact operating model

## Development-only extras

For local development and testing, this repo also includes:
- `src/` and `bin/` richer helper implementation
- root `tests/`
- GitHub validation workflow

These are for repo quality and local validation. Installed Paperclip usage should rely on the packaged `scripts/` and `references/` paths above.
