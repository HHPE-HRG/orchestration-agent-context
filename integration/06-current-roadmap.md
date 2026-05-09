# Current roadmap

This is the active orchestration roadmap as of the latest refresh. Treat this as the answer to "what should we do next?".

## Current status

- **Stoneforge reference package exists.** `xlotyl/capability-packages/stoneforge-runtime/` is the reference manifest shape and adapter set.
- **`source-corroboration-runtime` exists** as the second capability package, with a package-local validator (`source_corrob_min_packet_validator`).
- **Capability package smoke is compiler-driven** via `xlotyl/scripts/capability_package_smoke.py`, calling `compileCapabilityPackageGraph` in `xlotyl/services/core-dev-services/src/capability-package/graph-compiler.ts`.
- **Package smoke emits schema-valid `verification_report`** artifacts.
- **`mark-terminal` validates terminality and logs audit / noop records** via `terminality-validator.ts` and `mark-terminal.ts`.
- **`provider_reasoner` is NOT a task-card executor enum.** Use `strategic_reviewer` for provider-style reviewer behavior until model harness profiles exist.

## Next steps (in order)

1. **Remove smoke-index drift.** Discover package smokes from `manifest.smoke.required = true` instead of maintaining a separate smoke index. The manifest is the source of truth.
2. **Add an orchestration-state schema.** Formalize the in-flight orchestration state object that XLOTYL emits and Stoneforge consumes, so it can be validated end-to-end.
3. **Add a model harness profile schema.** Once profiles exist, `provider_reasoner` (and other provider-style reviewer enums) can land cleanly without the current `strategic_reviewer` workaround.
4. **Make `compileCapabilityPackageGraph` emit `orchestration_state`.** The compiler should produce the orchestration-state object directly, alongside the graph, so consumers don't have to re-derive it.
5. **Add a package-specific validator for `source-corroboration-runtime`.** Beyond the minimal packet validator, add a domain-aware validator that exercises the corroboration packet shape against expected evidence patterns.
6. **Then add more complex packages.** In order of growing complexity:
   - `document-formatting-runtime`
   - `cad-runtime`
   - `solver-runtime`

## Hard rules around this roadmap

- Do NOT add a third capability package before step 5 completes. The boundary checks need a second domain-aware validator before the matrix grows.
- Do NOT introduce `provider_reasoner` as a task-card executor enum until step 3 (model harness profile schema) lands.
- Do NOT regress the compiler-driven smoke contract while doing step 1 (smoke-index removal). The smoke must continue to call `compileCapabilityPackageGraph`.
- Do NOT split orchestration-state emission across XLOTYL and Stoneforge. XLOTYL emits it. Stoneforge consumes it.
