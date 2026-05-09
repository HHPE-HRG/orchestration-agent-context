# Current orchestration state

Snapshot of the XLOTYL orchestration story as of the last refresh.

## Reference package

`stoneforge-runtime` is the reference capability package. It defines the canonical adapter set (10) and the canonical global validator set (4). Any new package must reproduce these exactly.

## Second package

`source-corroboration-runtime` is the second capability package. It is the current example of:

- a non-orchestration domain (`research`),
- a package-local validator (`package_local:source_corrob_min_packet_validator`),
- a deterministic offline smoke flow.

## Smoke

Smoke is compiler-driven. `scripts/capability_package_smoke.py` calls `compileCapabilityPackageGraph` directly and emits a schema-valid `verification_report` artifact.

## Terminality

`mark-terminal.ts` and `terminality-validator.ts` enforce terminality. Audit and noop records are written; no silent state mutation.

## Provider reasoner gap

`provider_reasoner` is not a task-card executor enum. Provider-style reviewer behavior currently routes through `strategic_reviewer`. This is a deliberate workaround until the model harness profile schema lands.

## Things explicitly NOT done yet

These are NOT current state — they are roadmap. See [`../integration/06-current-roadmap.md`](../integration/06-current-roadmap.md):

- smoke-index drift removal (still indexed somewhere; should be discovered via manifest),
- orchestration-state schema,
- model harness profile schema,
- compiler-emitted orchestration_state,
- domain-aware validator for source-corroboration-runtime,
- additional packages (`document-formatting-runtime`, `cad-runtime`, `solver-runtime`).

If a chat agent is asked "is X done?" and X appears in the roadmap above, the answer is **no**.
