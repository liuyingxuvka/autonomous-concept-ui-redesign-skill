## Overview

Add a focused checker that reads a JSON final acceptance ledger and returns the
same style of closure report used by the Guard-family workflows:
`closure_status`, `findings`, `missing_inputs`, `stale_evidence`,
`skipped_checks`, and `next_actions`.

## Decisions

- Keep the checker small and standard-library-only.
- Do not replace the child skills' own standards. The checker only verifies
  that the orchestrator ledger has rows, current evidence, valid statuses, and
  downgrade handling.
- Treat `blocked` rows as blockers, stale or missing evidence as partial unless
  already blocked, and unsupported skipped rows as partial.
- Accept either a top-level list of rows or an object with `ledger_rows` or
  `rows`.

## Non-Goals

- Do not score visual quality.
- Do not parse screenshots or browser logs.
- Do not make the UI skill depend on a package install.
