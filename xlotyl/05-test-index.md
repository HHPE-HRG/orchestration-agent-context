# XLOTYL test index

Verification gates and test commands for the XLOTYL repo. Run from the `xlotyl/` repo root unless noted.

## Capability packages

```bash
# Schema validation across all packages
python scripts/validate_capability_packages.py

# Compiler-driven smoke; emits schema-valid verification_report artifacts
python scripts/capability_package_smoke.py

# Boundary guard
python scripts/check_capability_package_boundary.py
```

## core-dev-services (Stoneforge contract surfaces, XLOTYL-side)

```bash
pnpm install
pnpm --filter @xlotyl/core-dev-services build
pnpm --filter @xlotyl/core-dev-services test
pnpm --filter @xlotyl/core-dev-services test:e2e
```

Test directories of interest:

- `services/core-dev-services/src/__tests__/`
- `services/core-dev-services/e2e/`
- `services/core-dev-services/fixtures/`

## response-control-framework

```bash
cd services/response-control-framework
pip install -e ".[dev]"
pytest
```

## Orchestration CI scripts

```bash
bash scripts/ci_orchestration_conversation_replay.sh
bash scripts/ci_orchestration_prompt_bank.sh
bash scripts/ci_orchestration_tier3_materialize_all.sh
```

## Lint / hygiene

```bash
bash scripts/ci_python_lint_paths.sh
python scripts/check_legacy_names.py
python scripts/check_stale_org_paths.py
python scripts/check_deployed_branch_no_model_mocks.py
```

## Mock-Stoneforge contract test bootstrap

```bash
bash scripts/bootstrap_stoneforge_contract_env.sh
```

## What "success" means

A change is safe when, for the contract surfaces it touched:

- the relevant tests above pass locally,
- `python scripts/validate_capability_packages.py` is green,
- `python scripts/capability_package_smoke.py` emits valid `verification_report` for every required package,
- if it touches the XLOTYL ↔ Stoneforge boundary, the Stoneforge-side gates listed in [`../stoneforge/05-test-index.md`](../stoneforge/05-test-index.md) also pass.
