# Rollout

## Recommended first rollout

1. Install the skill through the Paperclip UI.
2. Attach it to one delivery-capable agent, not the whole company first.
3. Configure a narrow allowlisted destination chat.
4. Run smoke tests.
5. Test one real issue with a non-sensitive markdown attachment.
6. Verify the returned summary comment format is acceptable.
7. Expand to additional agents only after successful review.

## Operational ownership

- delivery owner decides when Telegram delivery is appropriate
- executing agent follows the explicit trigger contract
- reviewer confirms no secrets or unsupported files were sent

## Rollback

- detach the skill from agents or the company
- keep env values but stop invoking the workflow
- no persistent state needs migration
