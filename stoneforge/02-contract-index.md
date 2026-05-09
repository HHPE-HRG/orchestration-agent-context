# Stoneforge contract index

Pointer index for everything Stoneforge exposes (or consumes) as a contract.

## `sf` CLI

- `packages/smithy/src/bin/sf.ts` — Smithy `sf` entrypoint.
- `packages/quarry/src/bin/sf.ts` — Quarry `sf` entrypoint.
- `packages/quarry/src/cli/commands/` — command implementations.
- Contract details: [`../integration/02-sf-cli-contract.md`](../integration/02-sf-cli-contract.md).

## Smithy runtime

- `packages/smithy/src/runtime/` — runtime loop, spawner, session manager, dispatch.
- `packages/smithy/src/api/orchestrator-api.ts` — Orchestrator API surface.
- `packages/smithy/src/services/` — internal services.
- `packages/smithy/src/prompts/` — built-in prompts (overridable via `.stoneforge/prompts/`).
- `packages/smithy/src/providers/` — provider integrations.

## Quarry data layer

- `packages/quarry/src/api/quarry-api.ts` — QuarryAPI surface.
- `packages/quarry/src/services/dependency.ts` — dependency service.
- `packages/quarry/src/sync/service.ts` — sync service (JSONL ↔ SQLite).
- `packages/quarry/src/systems/identity.ts` — identity / signing.
- `packages/quarry/src/config/` — configuration.

## Core types

- `packages/core/src/types/` — Element, Task, Message, Document, Entity, etc.
- `packages/core/src/types/event.ts` — event sourcing types.
- `packages/core/src/types/task.ts` — task type and status.

## XLOTYL integration (Stoneforge side)

- `docs/contracts/xlotyl-boundary.md` — Stoneforge's authoritative boundary statement.
- `docs/wiki/xlotyl-stoneforge-connection.md` — the twin wiki page.

## XLOTYL-tagged tests

Stoneforge runs `xlotyl_*`-tagged contract tests that XLOTYL relies on:

```bash
pnpm --filter @stoneforge/smithy test:xlotyl-daemon-decision
```

## Apps (dashboard surfaces)

- `apps/smithy-server/` — Orchestrator HTTP API (port 3457).
- `apps/smithy-web/` — Orchestrator dashboard (port 5174).
- `apps/quarry-server/` — Platform HTTP + WebSocket (port 3456).
- `apps/quarry-web/` — Platform SPA (port 5173).

These are NOT contracts. They are operator surfaces. Internal layout can change freely.

## What is NOT a Stoneforge contract

- Internal dashboard route layout.
- Worker pool internals.
- Session manager internals (as long as the orchestrator API surface is preserved).
- Spawner internals (as long as it produces the documented run artifacts).
