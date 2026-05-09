# openclaw overview

`HHPE-HRG/openclaw` is a fork of `openclaw/openclaw`, a personal AI assistant that runs on the operator's own devices and bridges to many messaging channels (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Matrix, Teams, etc.). Within HHPE-HRG it is the **personal-assistant / multi-channel surface**.

## Role within HHPE-HRG

- Personal-assistant front-end (Gateway + channels + plugins).
- Voice / Canvas surfaces (macOS / iOS / Android).
- Treated as an **external contract** — orchestration code should integrate via the documented plugin SDK and channel boundaries, not via core internals.

## Repository shape (upstream-driven)

OpenClaw uses a strict plugin/channel boundary that agents must respect. Key directories:

- `src/` — core source (CLI wiring in `src/cli`, commands in `src/commands`, web provider in `src/provider-web.ts`, infra in `src/infra`, media pipeline in `src/media`).
- `src/plugin-sdk/` — **the public plugin contract**. Extensions may import from here.
- `src/plugins/` — plugin discovery, manifest validation, loader, registry, contract enforcement.
- `src/channels/` — core channel implementation behind the plugin/channel boundary.
- `src/telegram/`, `src/discord/`, `src/slack/`, `src/signal/`, `src/imessage/`, `src/web/` — built-in channel implementations.
- Bundled workspace plugin tree — bundled plugins; this is the closest example surface for third-party plugin authors.
- `docs/` — channel docs (`docs/channels/`), images, queue, Pi config.
- `apps/` — operator-facing surfaces.
- `extensions/` — extension code.
- `qa/` — QA harness.
- `Swabble/` — internal helper area.
- Tests are colocated as `*.test.ts`.

## Plugin / channel boundary (from upstream `AGENTS.md`)

Extensions may import:

- `openclaw/plugin-sdk/*` — public plugin SDK.
- Local `api.ts` / `runtime-api.ts` barrels.

Extensions must NOT import:

- `src/**` of core,
- `src/plugin-sdk-internal/**`,
- another extension's `src/**`.

This is the rule any agent recommending OpenClaw plugin work must follow.

## Plugin naming invariant

For repo-owned workspace plugins, keep the canonical plugin id aligned across:

- `openclaw.plugin.json:id`
- the default workspace folder name
- the package name (`@openclaw/<id>` or approved suffix forms `-provider`, `-plugin`, `-speech`, `-sandbox`, `-media-understanding`)
- `openclaw.install.npmSpec` equal to the package name
- `openclaw.channel.id` equal to the plugin id when present

Exceptions must be explicit and covered by the repo invariant test.

## What this mirror provides

This mirror records the **commit SHA, branch, and tracked-file count** for the local checkout in `generated/source-manifest.json`. It does **not** chunk source files, and does **not** produce a symbol index for this repo.

Reasoning:

- OpenClaw is large (~13,600 tracked files at the last refresh) and would dominate the mirror.
- The plugin/channel boundary is the operative contract; full source isn't needed for most orchestration reasoning.
- The upstream `AGENTS.md` (in `HHPE-HRG/openclaw/AGENTS.md`) is comprehensive enough to ground a chat agent.

## When to deepen this mirror

If a task genuinely needs deep OpenClaw context, ask the operator to:

1. Add an `openclaw_chunks` block to [`../context-config.json`](../context-config.json) targeting narrow subtrees (e.g. `src/plugin-sdk/`, a specific channel, a specific bundled plugin).
2. Extend [`../scripts/generate.py`](../scripts/generate.py) to treat `openclaw` as a primary repo for chunking.
3. Re-run `./refresh.sh`.

## Hard rules for agents

- Do **not** propose imports across the plugin/channel boundary; respect the public surface.
- Do **not** edit files covered by security-focused `CODEOWNERS` rules unless a listed owner explicitly opens that scope.
- Do **not** edit upstream content in this mirror. Submit fixes to `HHPE-HRG/openclaw` directly.
- File references in chat replies for OpenClaw work are repo-root relative only (e.g. `src/telegram/index.ts:80`); never absolute paths or `~/...`.

## Canonical path

`HHPE-HRG/openclaw`.
