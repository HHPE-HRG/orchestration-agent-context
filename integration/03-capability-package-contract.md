# Capability package contract

A capability package is a **hard manifest boundary**. The manifest tells XLOTYL's compiler what execution adapters, validators, and smoke metadata to wire up for a given runtime environment.

## Live packages

- `xlotyl/capability-packages/stoneforge-runtime/` — **reference package**.
- `xlotyl/capability-packages/source-corroboration-runtime/` — **package #2**, includes a package-local validator (`source_corrob_min_packet_validator`).

## Manifest schema

- Schema: `xlotyl/schemas/capability-package/v1/`
- Manifest file: `capability.manifest.json` at the package root.

## Required fields (observed from live packages)

```json
{
  "schema_version": "1.0.0",
  "package_id": "...",
  "label": "...",
  "domain": "...",
  "summary": "...",
  "status": "active",
  "owners": ["xlotyl"],
  "domain_knowledge_packages": ["artifact://domain-knowledge-package/..."],
  "smoke": {
    "required": true,
    "mode": "local-artifact",
    "example_task_card": "examples/min-task-card.json",
    "source_goal": "..."
  },
  "runtime_environments": [
    { "id": "...", "status": "active", "summary": "..." }
  ],
  "execution_adapters": [
    { "id": "xlotyl_stoneforge_validate" },
    { "id": "xlotyl_stoneforge_import" },
    { "id": "xlotyl_stoneforge_approve" },
    { "id": "xlotyl_stoneforge_activate" },
    { "id": "xlotyl_stoneforge_sync" },
    { "id": "xlotyl_stoneforge_evaluate" },
    { "id": "xlotyl_stoneforge_replan" },
    { "id": "xlotyl_stoneforge_replay" },
    { "id": "xlotyl_stoneforge_aggregate" },
    { "id": "xlotyl_stoneforge_mark_terminal" }
  ],
  "validators": [
    { "id": "graph_schema_validation" },
    { "id": "acyclic_dependency_check" },
    { "id": "approval_before_activation" },
    { "id": "max_replan_cycles" }
  ]
}
```

## Package-local validators

A package may declare a local validator:

```json
{
  "id": "package_local:<name>",
  "path": "capability-packages/<package-id>/validators/<file>.py",
  "summary": "..."
}
```

These are deterministic and must be runnable offline (no network) when `smoke.mode = "local-artifact"`.

## Hard rules for agents

1. **Do not invent execution adapter IDs.** The set above is the contract. New adapters are a cross-repo change.
2. **Do not invent validator IDs.** Adding a global validator changes the schema. Local validators (`package_local:*`) are scoped to a single package.
3. **`stoneforge-runtime` is the reference package.** When in doubt about manifest shape, copy from there.
4. **`source-corroboration-runtime` is the second package.** It is the canonical example of a package with a package-local validator.

## Tooling

- Smoke: `xlotyl/scripts/capability_package_smoke.py` — compiler-driven smoke. Emits a schema-valid `verification_report` artifact (see [`04-package-smoke-contract.md`](04-package-smoke-contract.md)).
- Validate: `xlotyl/scripts/validate_capability_packages.py` — schema validation across all packages.
- Boundary check: `xlotyl/scripts/check_capability_package_boundary.py` — guards the package-as-hard-manifest boundary.
- Scaffold: `xlotyl/scripts/scaffold_capability_package.py` — generates a new package skeleton.

## Reasoner / reviewer note

`provider_reasoner` is **not** currently a task-card executor enum.
For provider-style reviewer behavior, use `strategic_reviewer` until model harness profiles exist.
This is a known gap; see [`06-current-roadmap.md`](06-current-roadmap.md) item "model harness profile schema".
