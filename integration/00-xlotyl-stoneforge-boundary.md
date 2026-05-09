# XLOTYL ↔ Stoneforge integration boundary

This is the single most important document in this mirror. It exists so a chat agent cannot accidentally recommend a change that crosses the line.

## Canonical repos

- XLOTYL: `HHPE-HRG/xlotyl` (control plane)
- Stoneforge: `HHPE-HRG/stoneforge` (runtime)

Both are independent. They are **not** linked by git submodule. They are linked by:

- npm contracts (XLOTYL consumes Stoneforge contracts via `@xlotyl/core-dev-services` and SF-CLI helpers),
- shared scripts,
- this mirror plus the live wiki pages:
  - `xlotyl/knowledge/wiki/projects/xlotyl-stoneforge-connection.md`
  - `stoneforge/docs/wiki/xlotyl-stoneforge-connection.md`
  - `stoneforge/docs/contracts/xlotyl-boundary.md`

## What each side does

| Concern                                                              | Owner       |
| -------------------------------------------------------------------- | ----------- |
| Compile and validate `graph.json`                                    | XLOTYL      |
| Execute imported `graph.json`                                        | Stoneforge  |
| Capability package manifests, smoke metadata, validators             | XLOTYL      |
| `xsf` CLI / MCP contract                                             | XLOTYL      |
| `sf` CLI surfaces                                                    | Stoneforge  |
| Smithy runtime, dispatch, worktrees                                  | Stoneforge  |
| Quarry data layer (JSONL + SQLite)                                   | Stoneforge  |
| Wiki / response-control source of truth                              | XLOTYL      |
| Model harness routing, profiles, eligibility                         | XLOTYL      |
| Operator dashboards                                                  | Stoneforge  |
| Merge / steward workflows                                            | Stoneforge  |
| Terminality validation, mark-terminal audit/noop records             | XLOTYL      |
| Replan pipeline, max-replan-cycles validator                         | XLOTYL      |
| Decision-provider / daemon-decision contract                         | XLOTYL defines, Stoneforge consumes |

## The integration rule

In **XLOTYL-controlled runs** (`execution_mode = xlotyl_stoneforge`):

1. XLOTYL compiles and validates `graph.json`.
2. Stoneforge imports and executes `graph.json` as-is.
3. **Stoneforge Director MUST NOT decompose goals** in this mode. It may schedule and visualize, but must not reshape the plan.
4. XLOTYL-owned graph / replan / terminality semantics are preserved end-to-end.

When the run is not XLOTYL-controlled, Stoneforge Director's native goal-decomposition behavior is allowed.

## Cross-repo change list

The following classes of change require coordinated edits in **both** repos and require the **paired contract test suite** to pass:

- **Graph format** — anything affecting `graph.json` shape, fields, or semantics.
- **`sf` CLI behavior** — JSON stdout shape, exit codes, command names. XLOTYL contract tests in `services/core-dev-services` consume these.
- **Decision-provider behavior** — `xlotyl_stoneforge` mode contract.
- **Daemon-decision contract** — `services/core-dev-services/src/stoneforge/daemon-decision.ts` ↔ Stoneforge runtime.
- **Task lifecycle** — task status fields, dispatch status semantics, terminality flags.
- **Dispatch semantics** — anything that changes when a task moves from ready → in_progress → done.
- **Verification report contract** — schema-valid `verification_report` shape (XLOTYL emits, Stoneforge consumes when round-tripping).

If a change is purely:

- **Inside Stoneforge** and preserves all of the contracts above (e.g. dashboard styling, internal worktree scheduling, internal merge logic) — it is Stoneforge-only.
- **Inside XLOTYL** and does not change graph/CLI/decision-provider/task-lifecycle/verification-report contracts (e.g. wiki edits, capability package internals, response-control content updates) — it is XLOTYL-only.

When in doubt, treat it as cross-repo and run both contract suites.

## Compatibility gates (run before claiming success)

From `stoneforge/`:

```bash
pnpm install
pnpm --filter @stoneforge/smithy build
pnpm --filter @stoneforge/smithy test:xlotyl-daemon-decision
pnpm test   # if touching core runtime, dispatch, or CLI
```

From `xlotyl/`:

```bash
# Capability-package smoke (compiler-driven; emits schema-valid verification_report)
python scripts/capability_package_smoke.py
python scripts/validate_capability_packages.py
```

If both sides pass, the boundary is intact for the change at hand.

## Things that are NOT contracts

- Internal Stoneforge UI structure.
- Internal Stoneforge dashboard route layout.
- Internal XLOTYL wiki page organization.
- Internal capability-package validator implementation (as long as the validator id and its emitted record shape are stable).

## See also

- [`01-graph-contract.md`](01-graph-contract.md) — graph.json format pointers.
- [`02-sf-cli-contract.md`](02-sf-cli-contract.md) — sf CLI surface contract.
- [`03-capability-package-contract.md`](03-capability-package-contract.md) — capability-package manifest contract.
- [`04-package-smoke-contract.md`](04-package-smoke-contract.md) — compiler-driven smoke + verification_report.
- [`05-terminality-contract.md`](05-terminality-contract.md) — mark-terminal validation, audit/noop records.
- [`06-current-roadmap.md`](06-current-roadmap.md) — active next steps.
