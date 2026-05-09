# `sf` CLI contract

`sf` is Stoneforge's operator CLI. XLOTYL consumes it as a contract.

## Producer (Stoneforge)

- `stoneforge/packages/smithy/src/bin/sf.ts` — Smithy `sf` entrypoint.
- `stoneforge/packages/quarry/src/bin/sf.ts` — Quarry `sf` entrypoint.
- `stoneforge/packages/quarry/src/cli/commands/` — command implementations.

## Consumer (XLOTYL)

- `xlotyl/services/core-dev-services/src/stoneforge/sf-cli-binding.ts` — typed binding for `sf` command output.
- `xlotyl/services/core-dev-services/src/stoneforge/xsf-cli.ts` — XLOTYL-side `xsf` CLI that wraps `sf`.
- Contract tests: under `xlotyl/services/core-dev-services/` (vitest).

## What is a contract

The following are part of the contract and require coordinated change in both repos:

- Command names (`sf task ready`, `sf task blocked`, `sf show <id>`, `sf task create`, `sf dependency add`, `sf task close`, `sf stats`, ...).
- JSON stdout shape and field names emitted in JSON output mode.
- Exit codes.
- Error envelope shape.
- Behavior of flags that XLOTYL contract tests rely on.

## What is NOT a contract

- Human-readable formatting of standard (non-JSON) output, as long as JSON mode is preserved.
- Internal command implementation.
- Color, spinners, prompt UX.

## How to verify

Run XLOTYL contract tests:

```bash
cd xlotyl
pnpm --filter @xlotyl/core-dev-services test
```

Run Stoneforge xlotyl-tagged tests:

```bash
cd stoneforge
pnpm --filter @stoneforge/smithy test:xlotyl-daemon-decision
```
