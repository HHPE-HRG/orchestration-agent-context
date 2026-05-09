# Stoneforge test index

Verification gates and test commands for the Stoneforge repo. Run from the `stoneforge/` repo root unless noted.

## Build

```bash
pnpm install
pnpm --filter @stoneforge/smithy build
```

## Full test suite

```bash
pnpm test
```

Run this when changes touch core runtime behavior, dispatch semantics, or CLI contracts.

## XLOTYL-tagged contract tests

```bash
pnpm --filter @stoneforge/smithy test:xlotyl-daemon-decision
```

This is the gate for the XLOTYL ↔ Stoneforge `xlotyl_stoneforge` mode contract.

## Per-package

```bash
pnpm --filter @stoneforge/smithy   test
pnpm --filter @stoneforge/quarry   test
pnpm --filter @stoneforge/core     test
pnpm --filter @stoneforge/storage  test
pnpm --filter @stoneforge/ui       test
```

Tests are colocated with source: `*.test.ts` next to `*.ts`. See `sf show el-50x1` (in the live Stoneforge repo) for Bun vs Vitest test runner conventions.

## Bun usage

```bash
bun install
bun run build
bun test
bun test --watch
```

## Running apps for manual verification

```bash
bun run --filter @stoneforge/quarry-server  dev    # Platform server (port 3456)
bun run --filter @stoneforge/quarry-web     dev    # Platform web (port 5173)
bun run --filter @stoneforge/smithy-server  dev    # Orchestrator (port 3457)
bun run --filter @stoneforge/smithy-web     dev    # Orchestrator UI (port 5174)
```

## What "success" means

A change is safe when:

- `pnpm install && pnpm --filter @stoneforge/smithy build` succeeds.
- `pnpm --filter @stoneforge/smithy test:xlotyl-daemon-decision` passes.
- `pnpm test` passes (when touching core runtime, dispatch, or CLI).
- For cross-repo changes (graph format, sf CLI, decision-provider, task lifecycle, dispatch semantics, verification report contract), the XLOTYL-side gates in [`../xlotyl/05-test-index.md`](../xlotyl/05-test-index.md) also pass.
