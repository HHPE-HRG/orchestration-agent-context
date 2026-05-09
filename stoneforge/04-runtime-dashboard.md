# Stoneforge runtime + dashboard

Operator-facing surfaces. The runtime is the orchestration loop; the dashboards are how humans see and steer it.

## Apps and ports

| App                     | Path                | Port | Purpose                                |
| ----------------------- | ------------------- | ---- | -------------------------------------- |
| `quarry-server`         | `apps/quarry-server`| 3456 | Platform HTTP + WebSocket              |
| `quarry-web`            | `apps/quarry-web`   | 5173 | Platform SPA (Entities, Dependency Graph, Documents, Plans, Workflows, Settings) |
| `smithy-server`         | `apps/smithy-server`| 3457 | Orchestrator API                       |
| `smithy-web`            | `apps/smithy-web`   | 5174 | Orchestrator dashboard (Activity, Agents, Tasks, Workspaces, Editor, Merge Requests, Plans, Workflows, Settings, Metrics) |

Ports above come from `stoneforge/AGENTS.md` and are documented as gotcha #10 ("Server ports - Platform: 3456, Orchestrator: 3457 (not 3000)").

## Agent roles (orchestrator)

- **Director** — owns task backlog, makes strategic decisions, spawns workers. In `xlotyl_stoneforge` mode the Director must NOT decompose goals.
- **Worker** — executes assigned tasks, ephemeral or persistent.
- **Steward** — handles code merges, documentation scanning and fixes.

## Key runtime services

- `OrchestratorAPI` — agent registration/management.
- `DispatchService` — task assignment with inbox notifications.
- `SpawnerService` — process spawning, headless/interactive modes (`packages/smithy/src/runtime/spawner.ts`).
- `SessionManager` — agent session lifecycle (`packages/smithy/src/runtime/session-manager.ts`).

## Dual storage model (Quarry)

- **SQLite** is the cache (fast queries, FTS, indexes).
- **JSONL** is the source of truth (git-tracked, append-only).

After `sf import`, run `sf document reindex` to rebuild the FTS index — it is not auto-rebuilt on import.

## Dependency types

- **Blocking**: `blocks`, `awaits`, `parent-child` — affect task status.
- **Non-blocking**: `relates-to`, `mentions`, `references` — informational.
- `blocked` status is **computed** from dependencies, never set directly.

## Operator dashboards (where things live)

- **Activity:** `apps/smithy-web/src/routes/activity/`, `apps/smithy-web/src/components/activity/`
- **Agents:** `apps/smithy-web/src/routes/agents/`, `apps/smithy-web/src/components/agent/`
- **Tasks:** `apps/smithy-web/src/routes/tasks/`, `apps/smithy-web/src/components/task/`
- **Workspaces:** `apps/smithy-web/src/routes/workspaces/`, `apps/smithy-web/src/components/workspace/`, `apps/smithy-web/src/components/terminal/`
- **Editor:** `apps/smithy-web/src/routes/editor/`, `apps/smithy-web/src/components/editor/`
- **Merge Requests:** `apps/smithy-web/src/routes/merge-requests/`, `apps/smithy-web/src/components/merge-request/`
- **Plans:** `apps/smithy-web/src/routes/plans/` or `apps/quarry-web/src/routes/plans/`
- **Workflows:** `apps/smithy-web/src/routes/workflows/` or `apps/quarry-web/src/routes/workflows/`
- **Settings:** `apps/smithy-web/src/routes/settings/` or `apps/quarry-web/src/routes/settings/`
- **Metrics:** `apps/smithy-web/src/routes/metrics/`
- **Dashboard (quarry):** `apps/quarry-web/src/routes/dashboard/`
- **Entity:** `apps/quarry-web/src/routes/entities/`
- **Dependency Graph:** `apps/quarry-web/src/routes/dependency-graph/`

## Worktrees

Each running worker gets a git worktree. Worker pool, dispatch, and worktree lifecycle are entirely Stoneforge-internal — XLOTYL must not assume how they are scheduled.
