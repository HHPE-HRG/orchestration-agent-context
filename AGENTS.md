# AGENTS.md — orchestration-agent-context

This file is the rules-of-engagement for any chat or coding agent reading this repo.

## What this repo is

A **generated context mirror** of the HHPE-HRG orchestration repos:

- `HHPE-HRG/xlotyl` — control plane (source of truth)
- `HHPE-HRG/stoneforge` — execution runtime (source of truth)
- `HHPE-HRG/claw-code`, `HHPE-HRG/void`, `HHPE-HRG/openclaw` — supporting forks

Everything under `xlotyl/chunks/`, `stoneforge/chunks/`, and `generated/` is **regenerated** by [`refresh.sh`](refresh.sh) from local sibling checkouts. The hand-curated docs (`*/00-boundary.md`, `integration/*`, this file, `README.md`) are stable.

## Hard rules for agents

1. **This is not source of truth.** Source of truth lives in `HHPE-HRG/xlotyl` and `HHPE-HRG/stoneforge`. Recommend changes against those repos, never against this mirror.

2. **Do not edit generated context manually.** If a chunk is wrong, fix the generator (`refresh.sh`, `context-config.json`) or fix the upstream source file, then re-run `./refresh.sh`. Manual edits to `chunks/` or `generated/` will be silently overwritten.

3. **Do not infer code that is not present in chunks.** If a symbol is referenced but its definition is not in any chunk, say so. Do not hallucinate the implementation.

4. **Ask for a refresh if context looks stale.** Check [`generated/source-manifest.json`](generated/source-manifest.json) for `generated_at` and per-repo `commit_sha`. If they are older than the user's expectation, ask the operator to run `./refresh.sh`.

5. **Preserve repo boundaries.** XLOTYL and Stoneforge own different things. Read [`integration/00-xlotyl-stoneforge-boundary.md`](integration/00-xlotyl-stoneforge-boundary.md) before suggesting any change that crosses repos.

6. **Cite context file paths.** When you make a recommendation, cite both:
   - the path inside this mirror (e.g. `xlotyl/chunks/response-control.md`),
   - the canonical path inside the source repo (e.g. `services/response-control-framework/src/...`).
   This lets a human verify the chunk against the live repo.

7. **Never request secrets.** This mirror deliberately excludes `.env*`, private keys, and model weights. Do not ask the operator to paste secrets into chat. Do not propose committing secrets to this repo.

8. **Never ask for a full repo upload.** The point of this mirror is that you don't need one. If a chunk is missing, ask for a more targeted refresh (e.g. "please re-run `./refresh.sh` and confirm the manifest covers `services/response-control-framework`") rather than the whole tree.

## Soft conventions

- Treat each `chunks/<topic>.md` as a paginated read. Do not summarize across topics without reading each.
- Treat `03-symbol-index.md` as a navigation aid, not a complete API surface. Real signatures live in chunks; the index just points at files.
- When recommending a code change, prefer to suggest the **exact source file path inside the canonical repo** so the operator can apply it locally.
- When you don't have enough context to answer, say so explicitly. Do not invent. The mirror's purpose is to make "I don't have that file in my context" verifiable.

## Boundary cheat sheet

| Concern                                       | Owner                              |
| --------------------------------------------- | ---------------------------------- |
| graph.json compilation, validation            | XLOTYL                             |
| graph.json execution                          | Stoneforge                         |
| capability package manifests, smoke metadata  | XLOTYL                             |
| `xsf` CLI / MCP catalogs                      | XLOTYL                             |
| `sf` CLI / dispatch                           | Stoneforge                         |
| Smithy runtime, Quarry data layer             | Stoneforge                         |
| response-control framework, wiki source       | XLOTYL                             |
| dashboards, worktrees, merge stewards         | Stoneforge                         |
| model harness routing, profiles, eligibility  | XLOTYL                             |
| terminality / mark-terminal validation        | XLOTYL                             |
| daemon-decision contract                      | XLOTYL defines, Stoneforge consumes|

## When in doubt

- Read [`README.md`](README.md) for the user-facing overview.
- Read [`integration/00-xlotyl-stoneforge-boundary.md`](integration/00-xlotyl-stoneforge-boundary.md) for the rule that decides which repo a change belongs in.
- Read [`integration/06-current-roadmap.md`](integration/06-current-roadmap.md) before suggesting "what should we do next" — the roadmap is the answer.
