# Paperclip UI Install Checklist

## Before install

- [ ] Repo/subtree is reachable from the Paperclip UI import source
- [ ] `skills/telegram-file-delivery/SKILL.md` exists and renders correctly
- [ ] `skills/telegram-file-delivery/_meta.json` exists
- [ ] `skills/telegram-file-delivery/README.md` explains rollout, guardrails, and workflow usage
- [ ] `skills/telegram-file-delivery/SECURITY.md` exists
- [ ] `skills/telegram-file-delivery/import-contract.json` exists
- [ ] No secrets, tokens, local operator data, or compiled artifacts are committed
- [ ] Validation passes: `bash scripts/validate.sh`

## Paperclip UI install

- [ ] Open Paperclip UI
- [ ] Go to Skills
- [ ] Choose install from GitHub
- [ ] Paste the repo URL containing this skill subtree
- [ ] Confirm Paperclip detects `skills/telegram-file-delivery/SKILL.md`
- [ ] Install the skill

## Post-install verification

- [ ] Attach the skill to the target company or agents
- [ ] Open installed skill preview and verify the trigger contract is visible
- [ ] Confirm the runtime can access sibling `scripts/`, `references/`, and `assets/`
- [ ] Confirm the agent instructions mention explicit comment-triggered delivery

## Runtime verification

- [ ] Set the required Telegram env values
- [ ] Run the smoke test message command
- [ ] Run the workflow example with `references/examples/comment.txt` and `references/examples/attachments.json`
- [ ] Confirm the JSON result includes sent/skipped/failed sections
- [ ] Confirm the emitted markdown comment is ready to paste back into the issue

## Production readiness checks

- [ ] The destination chat allowlist is configured narrowly
- [ ] The file extension allowlist is approved
- [ ] Operators know how blocked/missing-config cases are surfaced
- [ ] Reviewer or delivery owner understands the trigger grammar
- [ ] Rollback path is documented
