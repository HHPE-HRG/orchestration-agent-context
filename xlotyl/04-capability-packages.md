# Capability packages

Capability packages are hard manifest boundaries. Each package tells the compiler exactly which adapters, validators, and smoke metadata to wire up.

For the contract details, see [`../integration/03-capability-package-contract.md`](../integration/03-capability-package-contract.md) and [`../integration/04-package-smoke-contract.md`](../integration/04-package-smoke-contract.md).

## Live packages (status: active)

### `stoneforge-runtime` — reference package

- **Path:** `capability-packages/stoneforge-runtime/`
- **Domain:** `orchestration`
- **Owners:** `xlotyl`
- **Smoke mode:** `local-artifact`, required.
- **Runtime environment:** `engineering_orchestration_stack`.
- **Execution adapters:** the canonical 10:
  `xlotyl_stoneforge_validate`, `xlotyl_stoneforge_import`, `xlotyl_stoneforge_approve`, `xlotyl_stoneforge_activate`, `xlotyl_stoneforge_sync`, `xlotyl_stoneforge_evaluate`, `xlotyl_stoneforge_replan`, `xlotyl_stoneforge_replay`, `xlotyl_stoneforge_aggregate`, `xlotyl_stoneforge_mark_terminal`.
- **Validators:** the global four:
  `graph_schema_validation`, `acyclic_dependency_check`, `approval_before_activation`, `max_replan_cycles`.

### `source-corroboration-runtime` — package #2

- **Path:** `capability-packages/source-corroboration-runtime/`
- **Domain:** `research`
- **Owners:** `xlotyl`
- **Smoke mode:** `local-artifact`, required.
- **Runtime environment:** `source_corroboration_workbench`.
- **Execution adapters:** same canonical 10 as the reference package.
- **Validators:** the global four PLUS one package-local validator:
  - `package_local:source_corrob_min_packet_validator`
  - Path: `capability-packages/source-corroboration-runtime/validators/source_corrob_min_packet_validator.py`
  - Local-only, deterministic, no network.

## Adapter set (locked)

The 10 adapter IDs above are the contract. New adapters are a cross-repo change.

## Validator set (locked, with one local extension)

The four global validators are the contract. Packages may declare additional `package_local:*` validators that are scoped to that package only.

## Smoke

Smoke must:

- be discovered from `manifest.smoke.required = true`,
- call `compileCapabilityPackageGraph`,
- run all global validators,
- run any local validators,
- exercise import → approve → activate,
- emit a schema-valid `verification_report`.

See `scripts/capability_package_smoke.py`.

## Reasoner / reviewer note

`provider_reasoner` is **not** a task-card executor enum. Use `strategic_reviewer` until the model harness profile schema lands. See [`../integration/06-current-roadmap.md`](../integration/06-current-roadmap.md) item 3.
