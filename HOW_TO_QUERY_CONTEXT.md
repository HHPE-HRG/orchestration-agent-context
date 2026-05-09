# How to query this context

A short query playbook for chat agents. Use this when you need to find specific code, a symbol, or an answer about behavior.

## Step 0: confirm freshness

Open [`generated/FRESHNESS.md`](generated/FRESHNESS.md). If the `Generated:` timestamp looks stale relative to the operator's expectation, stop and ask for a refresh. Do not quote symbols from a stale mirror without warning.

## Step 1: pick the right repo

If you don't already know which repo owns the concern, read [`integration/00-xlotyl-stoneforge-boundary.md`](integration/00-xlotyl-stoneforge-boundary.md). The cheat sheet table tells you which repo each concern lives in.

## Step 2: navigate by index

In rough order of cost / specificity:

| Goal | File |
| ---- | ---- |
| "Where do contracts of type X live?" | `xlotyl/02-contract-index.md` or `stoneforge/02-contract-index.md` |
| "What is currently shipped vs roadmap?" | `xlotyl/06-current-orchestration-state.md`, `integration/06-current-roadmap.md` |
| "What capability packages exist?" | `xlotyl/04-capability-packages.md` |
| "How do I run the tests for X?" | `xlotyl/05-test-index.md`, `stoneforge/05-test-index.md` |
| "Where does symbol `Foo` live?" | `xlotyl/03-symbol-index.md`, `stoneforge/03-symbol-index.md`, or `generated/symbol-index.json` |
| "What files are in subtree X?" | `xlotyl/01-repo-map.md`, `stoneforge/01-repo-map.md`, or `generated/file-index.json` |
| "What chunks exist?" | `generated/chunk-index.json` |

## Step 3: open the chunk

Once you have a path, open the matching chunk under `xlotyl/chunks/` or `stoneforge/chunks/`. The chunk groups are domain-aligned:

| Repo | Chunk | Use when |
| ---- | ----- | -------- |
| xlotyl | `core-dev-services` | XLOTYL-side Stoneforge contracts (xsf CLI, daemon-decision, import, mark-terminal, replan, etc.) |
| xlotyl | `capability-packages` | live package manifests, validators, examples |
| xlotyl | `response-control` | response-control framework src + schemas |
| xlotyl | `schemas` | top-level schemas (capability-package, model-runtime, shell-bridge, domain) |
| xlotyl | `agent-platform` | agent-platform-service implementation |
| xlotyl | `model-runtime` | model runtime harness + schemas |
| xlotyl | `wiki-response-control` | knowledge/wiki + knowledge/response-control content |
| stoneforge | `smithy` | runtime, dispatch, prompts, providers |
| stoneforge | `quarry` | data layer (JSONL + SQLite + sync) |
| stoneforge | `dashboard` | server/web apps for both Smithy and Quarry |
| stoneforge | `cli` | sf CLI surfaces (smithy and quarry bins, command tree) |
| stoneforge | `xlotyl-integration` | docs/contracts/xlotyl-boundary.md, docs/wiki/xlotyl-stoneforge-connection.md |

Each chunk file starts with a header listing the source roots it includes and the source SHA it was generated from. If the header SHA is not the SHA in `generated/FRESHNESS.md`, something is inconsistent — flag it and ask for a refresh.

## Step 4: cite

When recommending a change, cite both:

1. **Mirror path** (so a human can verify against the chunk you actually read):
   `xlotyl/chunks/capability-packages.md → capability.manifest.json for source-corroboration-runtime`
2. **Canonical source path** (so a human can apply the change):
   `HHPE-HRG/xlotyl :: capability-packages/source-corroboration-runtime/capability.manifest.json`

Without both, the operator cannot tell whether you read the live tree or a stale chunk.

## Step 5: what to do when context is missing

You will sometimes need a file that isn't in any chunk. The honest options, in order:

1. **Check whether it's just out of scope.** Anything under `node_modules/`, `dist/`, `build/`, `.venv/`, `__pycache__/`, binary media, or `.env*` is excluded by design — see [`context-config.json`](context-config.json). Don't ask for a refresh; ask the operator to read the live file.
2. **Check whether the chunk group includes the path.** Open the relevant `chunks/<topic>.md` header to see the listed source roots. If the path isn't in any group, propose adding it to `context-config.json` (under `xlotyl_chunks` or `stoneforge_chunks`) and re-running `./refresh.sh`.
3. **Check whether the chunk truncated the file.** Files larger than `per_file_size_limit_bytes` (200 KB by default) are listed by path with a "contents omitted" note. Either bump the cap in `context-config.json` and re-refresh, or ask the operator to read the live file at the canonical path.
4. **If none of the above applies, request a targeted refresh.** Phrase it precisely: "please run `./refresh.sh` and confirm the manifest covers `<canonical path>` at SHA <expected>".

Never invent the contents of a missing file.

## Step 6: the supporting repos

`claw-code/`, `void/`, and `openclaw/` are intentionally indexed shallowly. They have a single hand-curated `00-overview.md` per repo. There are no chunks. If a task genuinely requires deep context for one of these, ask the operator to:

1. Add chunk groups for that repo to `context-config.json` (e.g. a `claw-code-chunks` block analogous to `xlotyl_chunks`),
2. Re-run `./refresh.sh`,
3. Re-prompt you with the new chunks available.

This keeps the default mirror small and focused on the orchestration story.

## Anti-patterns to avoid

- Quoting a symbol whose definition isn't in any chunk just because you saw the name in a symbol index.
- Recommending a "small" change without checking whether the affected file lives in a chunk that's actually fresh.
- Treating `generated/file-index.json` as proof a file exists today — it only proves the file existed at the SHA in `generated/source-manifest.json`.
- Asking for a "fresh upload of the whole repo" — this mirror exists so you don't have to.
