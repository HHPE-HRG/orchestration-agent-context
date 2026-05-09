# claw-code overview

`HHPE-HRG/claw-code` is the **vendored coding-agent harness** that XLOTYL pins as the source of code-execution capability inside the orchestration story. It is a fork; the upstream lives at `ultraworkers/claw-code`.

## Role within HHPE-HRG

- Coding-agent CLI surface (`claw`).
- Pinned by XLOTYL as a git submodule at `xlotyl/claw-code-main` (see `xlotyl/.gitmodules`, branch `model-free-dev`).
- Treated as an **external contract** — XLOTYL and Stoneforge code that calls into `claw` should not assume internal Rust/Python module layout.

## Repository shape (upstream-driven)

- `rust/` — canonical Rust workspace and the `claw` CLI binary. This is the runtime surface.
- `USAGE.md` — task-oriented usage guide (build, auth, CLI, sessions, parity harness).
- `PARITY.md` — Rust-port parity status against the older Python reference.
- `ROADMAP.md` — upstream roadmap and cleanup backlog.
- `PHILOSOPHY.md` — project intent / system-design framing.
- `src/` + `tests/` — companion Python/reference workspace and audit helpers; not the primary runtime surface.
- `docs/container.md` — container-first workflow.

## What this mirror provides

This mirror records the **commit SHA, branch, and tracked-file count** of the local checkout in `generated/source-manifest.json`. It does **not** chunk source files, and does **not** produce a symbol index for this repo. Indexing is intentionally shallow because:

- The orchestration story is XLOTYL ↔ Stoneforge; `claw-code` is a downstream consumer.
- The upstream README, USAGE, PARITY, and ROADMAP cover internal contracts adequately for chat agents.
- Including the full Rust workspace would dwarf the primary chunks.

## When to deepen this mirror

If a task genuinely needs deep `claw-code` context, ask the operator to:

1. Add a `claw_code_chunks` block to [`../context-config.json`](../context-config.json) listing the relevant subtrees (e.g. `rust/crates/...`, `USAGE.md`, `PARITY.md`).
2. Extend [`../scripts/generate.py`](../scripts/generate.py) to map `claw-code` to that block (the existing logic only treats `xlotyl` and `stoneforge` as primary).
3. Re-run `./refresh.sh`.

## Hard rules for agents

- Do **not** propose changes to `claw-code` internals as part of an XLOTYL/Stoneforge change unless the operator explicitly opens that scope.
- Do **not** confuse `HHPE-HRG/claw-code` with the deprecated `claw-code` crate on crates.io. The upstream README warns: `cargo install claw-code` installs the **wrong** thing.
- Do **not** edit upstream content in this mirror. Submit fixes to `HHPE-HRG/claw-code` directly (or to `ultraworkers/claw-code` upstream).

## Canonical path

`HHPE-HRG/claw-code` (and `xlotyl/claw-code-main` as the XLOTYL-side submodule path).
