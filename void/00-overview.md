# void overview

`HHPE-HRG/void` is a fork of the open-source IDE `voideditor/void`, which itself is a fork of `microsoft/vscode` (`code-oss-dev`). Within HHPE-HRG it serves as the **editor / IDE component** alongside the orchestration runtime.

## Role within HHPE-HRG

- IDE / editor surface (VSCode-style) for human operators.
- Pinned by XLOTYL as a git submodule at `xlotyl/void` (see `xlotyl/.gitmodules`).
- Treated as an **external contract** — orchestration code that integrates with the editor should target documented extension/plugin points, not internal layout.

## Upstream status (as of this mirror)

The upstream maintainers have **paused active work** on the Void IDE to explore other coding ideas; the repo continues to run but without active maintenance. New upstream features should not be assumed; document any HHPE-HRG-specific divergence in the live source repo.

## Repository shape (upstream-driven)

- `src/` — main editor source (mirrors VSCode's tree).
- `extensions/` — bundled extensions.
- `cli/` — CLI surface.
- `remote/` — remote-development bits.
- `build/` — build pipeline.
- `scripts/` — operational scripts.
- `test/` — test trees.
- `void_icons/`, `resources/` — branding/UI assets.

## What this mirror provides

This mirror records the **commit SHA, branch, and tracked-file count** for the local checkout in `generated/source-manifest.json`. It does **not** chunk source files, and does **not** produce a symbol index for this repo.

Reasoning:

- `void` is a ~8,000-file codebase mostly inherited from VSCode. Chunking it would 10× the mirror size without meaningfully improving orchestration reasoning.
- Operators integrating with `void` typically work against extension/plugin points documented upstream (`VOID_CODEBASE_GUIDE.md`, `HOW_TO_CONTRIBUTE.md`).

## When to deepen this mirror

If a task genuinely needs deep `void` context, ask the operator to:

1. Add a `void_chunks` block to [`../context-config.json`](../context-config.json) targeting **specific narrow subtrees** (do not chunk `src/vs/...` wholesale).
2. Extend [`../scripts/generate.py`](../scripts/generate.py) to treat `void` as a primary repo for chunking.
3. Re-run `./refresh.sh`.

## Hard rules for agents

- Do **not** make recommendations that assume Void will gain new upstream features without confirmation — upstream is paused.
- Do **not** propose IDE changes as part of an XLOTYL/Stoneforge orchestration task unless the operator explicitly opens that scope.
- Do **not** edit upstream content in this mirror. Submit fixes to `HHPE-HRG/void` directly.

## Canonical path

`HHPE-HRG/void` (and `xlotyl/void` as the XLOTYL-side submodule path).
