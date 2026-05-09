# XLOTYL contract index

Pointer index for everything XLOTYL exposes as a contract. Use this to navigate; the actual content lives in `chunks/` and (for live edits) in the canonical paths inside `HHPE-HRG/xlotyl`.

## Schemas

- `schemas/` — top-level schema directory.
- `schemas/capability-package/v1/` — capability package manifest schema.
- `schemas/domain/` — domain knowledge schemas.
- `schemas/model-runtime/` — model runtime profile / eligibility schemas.
- `schemas/shell-bridge/` — shell bridge contracts.

## Response control

- `services/response-control-framework/schemas/` — response-control schema.
- `services/response-control-framework/src/` — framework implementation.
- `knowledge/response-control/` — compiled JSON snapshots:
  - `agent-profiles.json`
  - `domain-knowledge-packages.json`
  - `runtime-environments.json`
  - `techniques.json`
  - `theory.json`

## Capability packages

- `capability-packages/stoneforge-runtime/` — reference package.
- `capability-packages/source-corroboration-runtime/` — second package, package-local validator.
- `scripts/capability_package_smoke.py` — compiler-driven smoke; emits `verification_report`.
- `scripts/validate_capability_packages.py` — schema validation.
- `scripts/check_capability_package_boundary.py` — boundary guard.
- `scripts/scaffold_capability_package.py` — scaffolder.

## Wiki / response-control narrative

- `knowledge/wiki/index.md` — wiki entrypoint.
- `knowledge/wiki/SCHEMA.md` — wiki schema.
- `knowledge/wiki/meta/documentation-layers.md` — layer policy.
- `knowledge/wiki/projects/xlotyl-stoneforge-connection.md` — XLOTYL ↔ Stoneforge note.
- `knowledge/wiki/projects/oma-http-discovery-and-parity.md` — OMA HTTP discovery / parity.
- `knowledge/wiki/orchestration/` — response-control narrative tree (agent-profiles, domain-knowledge-packages, runtime-environments, techniques, theory).

## XLOTYL ↔ Stoneforge integration (XLOTYL side)

- `services/core-dev-services/src/stoneforge/` — full XLOTYL-side integration:
  - `xsf-cli.ts` — `xsf` CLI entrypoint.
  - `sf-cli-binding.ts` — typed binding to `sf` JSON output.
  - `daemon-decision.ts` — decision-provider contract surface.
  - `mode-guard.ts` — `execution_mode = xlotyl_stoneforge` guard.
  - `import.ts`, `import-run.ts` — graph import / run import.
  - `mark-terminal.ts`, `terminality-validator.ts` — terminality contract.
  - `replan.ts`, `replan-pipeline.ts` — replan flow + cycle limits.
  - `validator-registry.ts` — validator registry used by graph compile.
  - `aggregate-run.ts`, `replay-run.ts`, `evaluation.ts` — post-run evidence.
  - `task-card-renderer.ts` — task card rendering.
  - `decision/` — decision sub-tree.
- `services/core-dev-services/src/capability-package/` — capability-package compiler:
  - `graph-compiler.ts` — `compileCapabilityPackageGraph`.
  - `loader.ts`, `resolve.ts`, `index.ts`.

## Verification reports

- Emitted by `scripts/capability_package_smoke.py`.
- Schema enforced via `scripts/validate_capability_packages.py`.
- Schema location: `schemas/capability-package/v1/` (report sub-schema).

## Model runtime / agent platform

- `services/model-runtime/` — runtime harness implementation.
- `services/agent-platform-service/` — agent platform service surfaces.
- `schemas/model-runtime/` — runtime schemas.

## Orchestration scripts

- `scripts/ci_orchestration_*.sh` — orchestration CI entrypoints.
- `scripts/orchestration_cli_harness.sh` — CLI harness.
- `scripts/orchestration_conversation_replay.mjs` — conversation replay.
- `scripts/orchestration_tier3_materialize.mjs` — tier-3 materialization.
