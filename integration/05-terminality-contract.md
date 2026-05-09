# Terminality contract (`mark-terminal`)

Terminality is the contract that decides when a graph run is "done", and how that decision is recorded.

## Producer / validator (XLOTYL)

- `xlotyl/services/core-dev-services/src/stoneforge/mark-terminal.ts`
- `xlotyl/services/core-dev-services/src/stoneforge/terminality-validator.ts`

## What it must do

1. **Validate** terminality. A run is terminal only if the validator says so. The validator is the only source of truth.
2. **Log audit records.** When a `mark-terminal` call concludes the run, an audit record is emitted.
3. **Log noop records.** When a `mark-terminal` call would be a no-op (the run is already terminal, or the conditions aren't met), a noop record is emitted instead of mutating state.

Both audit and noop records flow into the run's evidence stream and (where applicable) into the `verification_report`.

## What it must NOT do

- Silently mutate run state without emitting a record.
- Skip the validator.
- Treat absence of a record as success.

## Stoneforge interaction

Stoneforge calls into `mark-terminal` via the XLOTYL-defined contract. Stoneforge does not implement terminality logic itself. If terminality semantics need to change, that is an XLOTYL change with paired Stoneforge contract test updates.

## See also

- [`01-graph-contract.md`](01-graph-contract.md) — graph contract overview.
- [`04-package-smoke-contract.md`](04-package-smoke-contract.md) — terminality decision flows into the verification_report.
