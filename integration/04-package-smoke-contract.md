# Package smoke + verification_report contract

Package smoke proves that a capability package can be compiled, imported, approved, and activated end-to-end against deterministic local artifacts. The smoke must be **compiler-driven** and must emit a **schema-valid `verification_report`**.

## Compiler-driven smoke

- Entrypoint: `xlotyl/scripts/capability_package_smoke.py`
- Compiler: `xlotyl/services/core-dev-services/src/capability-package/graph-compiler.ts`
  - Function: `compileCapabilityPackageGraph`
- Mode: `smoke.mode = "local-artifact"` in the package manifest. No network. No mock Stoneforge daemon other than what XLOTYL ships in `mocks/`.

## What "compiler-driven" means

Smoke must call the compiler. It must NOT:

- hand-craft a graph,
- bypass adapter registration,
- skip validator registration,
- short-circuit terminality.

It must:

- load the manifest,
- compile the graph,
- run all global validators (`graph_schema_validation`, `acyclic_dependency_check`, `approval_before_activation`, `max_replan_cycles`),
- run any package-local validators declared in the manifest,
- exercise the import → approve → activate path.

## verification_report

The smoke emits a `verification_report` JSON artifact. It must:

- pass schema validation against XLOTYL's report schema,
- include the package id and manifest hash,
- include the validator results (per-validator outcome and any diagnostic),
- include the adapter call trace,
- include the terminality decision (see [`05-terminality-contract.md`](05-terminality-contract.md)).

This artifact is what other agents and CI use to gate package-package promotion.

## Smoke discovery

Smoke must be discovered from `manifest.smoke.required = true`. **Do not maintain a hand-rolled smoke index.** A roadmap item explicitly calls this out — see [`06-current-roadmap.md`](06-current-roadmap.md) → "remove smoke-index drift".

## Local validator example

`xlotyl/capability-packages/source-corroboration-runtime/validators/source_corrob_min_packet_validator.py`

This is a deterministic, offline validator. Use it as the template for any new package-local validator.
