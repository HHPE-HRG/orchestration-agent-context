# Stoneforge boundary

`HHPE-HRG/stoneforge` is the **execution / orchestration runtime**. It is the source of truth for *how* graphs and tasks are run.

## Stoneforge owns

- **Smithy runtime** — agent orchestration loop in `packages/smithy/src/runtime/` (spawner, session manager, dispatch).
- **Quarry data layer** — durable JSONL source-of-truth + SQLite cache in `packages/quarry/`.
- **Agent dispatch** — `DispatchService`, inbox notifications, role assignment (Director / Worker / Steward).
- **Worktrees** — per-agent worktree isolation, worker pools.
- **Task and merge dashboards** — `apps/smithy-web`, `apps/quarry-web`, `apps/smithy-server`, `apps/quarry-server`.
- **Steward workflows** — merge flows, recovery flows, documentation scanning.
- **`sf` CLI surfaces** — `packages/smithy/src/bin/sf.ts`, `packages/quarry/src/bin/sf.ts` and the CLI command tree under `packages/quarry/src/cli/commands/`.

## Stoneforge does NOT own

- **XLOTYL graph planning** — graph compilation and validation live in XLOTYL. Stoneforge imports and executes graphs; it does not compile them.
- **XLOTYL capability-package semantics** — package manifests, smoke metadata, and validators live in XLOTYL.
- **XLOTYL wiki / response-control source of truth** — `knowledge/wiki/` and `knowledge/response-control/` live in XLOTYL.
- **XLOTYL model harness routing** — profile selection, eligibility, runtime routing.

## The integration rule (most important)

In **XLOTYL-controlled runs** (`execution_mode = xlotyl_stoneforge`):

- XLOTYL owns planning structure (`graph.json`).
- Stoneforge **executes** the imported graph.
- Stoneforge **Director must not autonomously decompose goals** in this mode. Visualization and scheduling are allowed; reshaping the plan is not.

When XLOTYL is **not** controlling the run, Stoneforge Director may decompose normally — that is its native mode.

For full integration semantics, see [`../integration/00-xlotyl-stoneforge-boundary.md`](../integration/00-xlotyl-stoneforge-boundary.md).
