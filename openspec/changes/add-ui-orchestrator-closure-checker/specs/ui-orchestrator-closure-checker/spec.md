## ADDED Requirements

### Requirement: UI orchestrator closure checker
The autonomous UI redesign skill SHALL provide a lightweight checker for a
structured final integrated acceptance ledger.

#### Scenario: Ledger passes
- **WHEN** every triggered required row has a valid passing, accepted-deviation,
  or justified skipped status with current evidence or a valid skip reason
- **THEN** the checker reports `closure_status: pass`

#### Scenario: Required evidence is stale or missing
- **WHEN** a triggered row has missing, stale, not-run, or untrusted evidence
- **THEN** the checker reports `closure_status: partial` or `blocked` and emits
  a next action

#### Scenario: A row is blocked
- **WHEN** any ledger row is `blocked`
- **THEN** the checker reports `closure_status: blocked`

### Requirement: Checker result feeds final verdict
The autonomous UI redesign orchestrator SHALL use the checker result before a
final completion claim when a structured final acceptance ledger exists.

#### Scenario: Checker downgrades
- **WHEN** the checker reports `partial` or `blocked`
- **THEN** the final answer cannot claim a full pass
