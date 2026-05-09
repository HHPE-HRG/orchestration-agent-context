# XLOTYL boundary

`HHPE-HRG/xlotyl` is the **control plane**. It is the source of truth for orchestration intent, contracts, and verification.

## XLOTYL owns

- **Control plane APIs** — HTTP and MCP surfaces in `services/api-service`, `services/router-service`, `services/mcp-registry-service`, `services/structure-service`.
- **Wiki / response-control** — `knowledge/wiki/` (orchestration narrative, projects, meta) and `knowledge/response-control/` (compiled JSON: `agent-profiles.json`, `domain-knowledge-packages.json`, `runtime-environments.json`, `techniques.json`, `theory.json`).
- **Capability packages** — `capability-packages/` and the package schema at `schemas/capability-package/`. `stoneforge-runtime` is the reference package; `source-corroboration-runtime` is the second package.
- **Capability-package compiler** — `services/core-dev-services/src/capability-package/graph-compiler.ts` (`compileCapabilityPackageGraph`).
- **Capability-package smoke tooling** — `scripts/capability_package_smoke.py`, `scripts/validate_capability_packages.py`, `scripts/scaffold_capability_package.py`, `scripts/check_capability_package_boundary.py`.
- **Graph compiler / planner** — produces `graph.json` consumed by Stoneforge.
- **xsf CLI / MCP contract** — `services/core-dev-services/src/stoneforge/xsf-cli.ts`, `sf-cli-binding.ts`, `daemon-decision.ts`, `import.ts`, `import-run.ts`, `mark-terminal.ts`, `terminality-validator.ts`, `replan.ts`, `replan-pipeline.ts`, `mode-guard.ts`, `validator-registry.ts`, `aggregate-run.ts`, `replay-run.ts`, `evaluation.ts`.
- **Model / runtime harnesses** — `services/model-runtime`, `schemas/model-runtime`, `services/agent-platform-service`. Profile/eligibility routing for hosted models lives here.
- **Verification reports** — schema-valid `verification_report` artifacts emitted by package smoke and validators.
- **Local-artifact and mock Stoneforge contract tests** — Stoneforge contract surfaces consumed (and tested) from XLOTYL via `@xlotyl/core-dev-services`.

## XLOTYL does NOT own

- Stoneforge UI (`apps/smithy-web`, `apps/quarry-web`, `apps/smithy-server`, `apps/quarry-server`).
- Smithy dispatch internals (`packages/smithy/src/runtime/spawner.ts`, `session-manager.ts`, dispatch service).
- Worktree scheduling internals (Stoneforge worker pools, isolation, lifecycle).
- Merge steward internals (Stoneforge merge/recovery flows, conflict resolution).
- Stoneforge dashboard behavior (Activity, Agents, Tasks, Workspaces, Editor, Merge Requests, Plans, Workflows, Settings, Metrics).
- `sf` CLI surfaces in `packages/smithy/src/bin/sf.ts` and `packages/quarry/src/bin/sf.ts`. XLOTYL **consumes** these as a contract; it does not own them.

## Hard rule for agents

If a change is about *what to plan, validate, or compile*, it lives in XLOTYL.
If a change is about *how a planned graph is dispatched and executed*, it lives in Stoneforge.

When in doubt, see [`../integration/00-xlotyl-stoneforge-boundary.md`](../integration/00-xlotyl-stoneforge-boundary.md).
