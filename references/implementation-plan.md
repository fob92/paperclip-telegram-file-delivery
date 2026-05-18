# Implementation Plan

## Objective

Provide a UI-importable Telegram delivery skill that works with only env configuration and follows Paperclip best practices.

## Design choices

- explicit comment trigger instead of vague natural-language inference
- zero-install Python stdlib helper instead of pip-dependent transport
- attachment-first V1 behavior
- conservative file and chat allowlists
- one summary comment per delivery action
- operator intervention required only for env setup or true permission issues

## Why stdlib-only

UI-importable skills should not require shell package installation. Using Python stdlib removes a major failure point and keeps setup limited to env values.

## Why not a dedicated delivery agent yet

For V1, delivery is a narrow cross-cutting operation. A reusable skill on existing execution agents is simpler, easier to audit, and easier to install.
