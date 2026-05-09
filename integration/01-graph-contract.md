# Graph contract (`graph.json`)

XLOTYL compiles `graph.json`. Stoneforge executes it. This document is a pointer index, not the schema itself — for the live schema, see XLOTYL's `schemas/` and `services/core-dev-services/src/capability-package/graph-compiler.ts`.

## Producer

- **Compiler:** `xlotyl/services/core-dev-services/src/capability-package/graph-compiler.ts` — entrypoint `compileCapabilityPackageGraph`.
- **Loader / resolver:** `xlotyl/services/core-dev-services/src/capability-package/loader.ts`, `resolve.ts`.
- **Validator:** `xlotyl/scripts/validate_capability_packages.py` (CLI), package smoke at `xlotyl/scripts/capability_package_smoke.py`.

## Consumer

- **Importers:** `xlotyl/services/core-dev-services/src/stoneforge/import.ts`, `import-run.ts` (XLOTYL-side test surface).
- **Stoneforge runtime:** consumes the imported graph via the Smithy runtime (`stoneforge/packages/smithy/src/runtime/`).
- **xsf bindings:** `xlotyl/services/core-dev-services/src/stoneforge/xsf-cli.ts`, `sf-cli-binding.ts`.

## Mutation policy

- **Format change** (fields, semantics, compatibility shape) → cross-repo change. Run both sides' contract tests.
- **Compiler-only refinement** (better diagnostics, more validators, no field changes) → XLOTYL-only.
- **Runtime-only refinement** (better dispatch on the same fields) → Stoneforge-only.

## Required orchestration mode

When `execution_mode = xlotyl_stoneforge`:

- Stoneforge Director must NOT decompose goals.
- Stoneforge mode-guard: `xlotyl/services/core-dev-services/src/stoneforge/mode-guard.ts`.

## Replan

- `xlotyl/services/core-dev-services/src/stoneforge/replan.ts`
- `xlotyl/services/core-dev-services/src/stoneforge/replan-pipeline.ts`
- Validator: `max_replan_cycles` (declared on every capability-package manifest under `validators[]`).

## Verification

After execution, the run-level evidence comes from:

- `xlotyl/services/core-dev-services/src/stoneforge/aggregate-run.ts`
- `xlotyl/services/core-dev-services/src/stoneforge/replay-run.ts`
- `xlotyl/services/core-dev-services/src/stoneforge/evaluation.ts`
- terminality: see [`05-terminality-contract.md`](05-terminality-contract.md).
