# Maturity definition and agent handoff (links only)

This mirror does **not** duplicate the workbook or questionnaires. Canonical narrative and policy stubs live in the **Xlotyl** and **Stoneforge** repositories.

## Pins for this refresh (operator-local checkouts)

Agents: treat these as the **minimum** SHAs this `orchestration-agent-context` refresh was generated against. Re-run [`../refresh.sh`](../refresh.sh) after updating sibling checkouts.

| Repo | Branch (typical) | Commit (short) | Full SHA |
| --- | --- | --- | --- |
| `HHPE-HRG/xlotyl` | `feat/maturity-lane-D-tracing-ci` | `4685cc0` | `4685cc09fc9598afcd636015a62c331d959ce2fd` |
| `HHPE-HRG/stoneforge` | `feat/maturity-lane-B-director-guard` | `6685584` | `66855845054150448bc05b86a7674c9f74c95d11` |

Canonical `HEAD` links below follow **`main`** / default branches; use the table when you need proof the mirror included a specific convergence commit set.

## Read first (cross-session)

1. **[`STRATEGY.md` (raw)](https://github.com/HHPE-HRG/xlotyl/blob/main/STRATEGY.md)** — product anchor.
2. **[Strategy and maturity handoff](https://github.com/HHPE-HRG/xlotyl/blob/main/knowledge/wiki/meta/strategy-and-maturity-handoff.md)** — numbered reading list for coding agents (`AGENTS.md`, documentation layers, maturity page, boundaries, Stoneforge Director register).

## Four maturity gates & questionnaire

3. **[Orchestration maturity ambiguity](https://github.com/HHPE-HRG/xlotyl/blob/main/knowledge/wiki/projects/orchestration-maturity-ambiguity.md)** — gates, rollup bar, **open decisions questionnaire**, **resolved answers → `xlotyl/docs`**.

## Policy / ADR targets (implement in Xlotyl)

- [`docs/policies/tracing-observability-policy.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/policies/tracing-observability-policy.md)
- [`docs/policies/guardrail-failure-modes.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/policies/guardrail-failure-modes.md) (appendix: adapter ↔ tests for **U10**)
- [`docs/policies/guardrail-failure-modes.yaml`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/policies/guardrail-failure-modes.yaml)
- [`docs/policies/human-in-the-loop-policy.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/policies/human-in-the-loop-policy.md)
- [`docs/meta/maturity-lane-contracts.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/meta/maturity-lane-contracts.md) (checkpoint **C0** + changelog)
- [`docs/adr/0006-orchestration-checkpoints-and-idempotency.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/adr/0006-orchestration-checkpoints-and-idempotency.md)
- [`docs/adr/0007-maturity-certificate-spec.md`](https://github.com/HHPE-HRG/xlotyl/blob/main/docs/adr/0007-maturity-certificate-spec.md)

### Tooling & operators (same convergence window as pins)

- [`scripts/sync-director-register.mjs`](https://github.com/HHPE-HRG/xlotyl/blob/4685cc09fc9598afcd636015a62c331d959ce2fd/scripts/sync-director-register.mjs) — R3 mirror Stoneforge → `fixtures/ci/director-path-register.json`
- [`services/core-dev-services/src/stoneforge/guardrail-runtime.ts`](https://github.com/HHPE-HRG/xlotyl/blob/4685cc09fc9598afcd636015a62c331d959ce2fd/services/core-dev-services/src/stoneforge/guardrail-runtime.ts) — YAML-aligned **`evaluate`** ingest guardrails
- [`docs/operators/orchestration-maturity-certificate-runbook.md`](https://github.com/HHPE-HRG/xlotyl/blob/4685cc09fc9598afcd636015a62c331d959ce2fd/docs/operators/orchestration-maturity-certificate-runbook.md) — **`--validate-schema`**, **`--fail-on-gate-fail`**, env pins
- Chunk mirror: `xlotyl/chunks/orchestration-maturity-tooling.md` (from `refresh.sh`)

## Stoneforge inventory (maintained alongside Smithy/runtime)

7. **[`director-path-register.md`](https://github.com/HHPE-HRG/stoneforge/blob/main/docs/orchestration/director-path-register.md)** — `xlotyl_stoneforge` decomposition path enumeration + tests (SF‑P04–P07 closed per pins).
8. **`@stoneforge/core` director guard** — [`packages/core/src/xlotyl/director-task-guard.ts`](https://github.com/HHPE-HRG/stoneforge/blob/66855845054150448bc05b86a7674c9f74c95d11/packages/core/src/xlotyl/director-task-guard.ts)
- Chunk mirror: `stoneforge/chunks/core-runtime.md` (from `refresh.sh`)

**Last mirrored:** 2026-05-10 (see [`generated/FRESHNESS.md`](../generated/FRESHNESS.md)).
