# Paperclip UI Install Checklist

## Before install

- [ ] Repo/subtree is reachable from the Paperclip UI import source
- [ ] `SKILL.md` exists and renders correctly
- [ ] `_meta.json` exists
- [ ] `README.md` explains rollout, guardrails, and workflow usage
- [ ] `SECURITY.md` exists
- [ ] `import-contract.json` exists
- [ ] No secrets, tokens, local operator data, or compiled artifacts are committed
- [ ] Validation passes: `bash scripts/validate.sh`

## Paperclip UI install

- [ ] Open Paperclip UI
- [ ] Go to Skills
- [ ] Choose install from GitHub
- [ ] Paste the repo URL containing this skill as its import root
- [ ] Confirm Paperclip detects `SKILL.md`
- [ ] Install the skill

## Post-install verification

- [ ] Attach the skill to the target company or agents
- [ ] Open installed skill preview and verify the trigger contract is visible
- [ ] Confirm the runtime can access the full skill tree, not only `SKILL.md`
- [ ] Confirm the agent instructions mention explicit comment-triggered delivery

## Runtime verification

- [ ] Set the required Telegram env values
- [ ] Run the smoke test message command
- [ ] Run the workflow example with `examples/comment.txt` and `examples/attachments.json`
- [ ] Confirm the JSON result includes sent/skipped/failed sections
- [ ] Confirm the emitted markdown comment is ready to paste back into the issue

## Production readiness checks

- [ ] The destination chat allowlist is configured narrowly
- [ ] The file extension allowlist is approved
- [ ] Operators know how blocked/missing-config cases are surfaced
- [ ] Reviewer or delivery owner understands the trigger grammar
- [ ] Rollback path is documented
