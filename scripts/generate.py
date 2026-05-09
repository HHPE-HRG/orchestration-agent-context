#!/usr/bin/env python3
"""
generate.py — single-pass Python generator for the orchestration-agent-context mirror.

Module purpose:
  Walk each source repo configured in context-config.json, collect git-tracked files
  (minus an exclusion blocklist), and produce per-repo:
    - file index   (generated/file-index.json)
    - symbol index (generated/symbol-index.json + */03-symbol-index.md)
    - markdown chunks under */chunks/ grouped by domain
    - repo map     (xlotyl/01-repo-map.md, stoneforge/01-repo-map.md)
  Plus a roll-up generated/source-manifest.json with commit SHAs / branches / timestamps.

Process flow:
  1. parse context-config.json
  2. clean regenerable outputs (chunks/, generated/) — leaves hand-curated docs alone
  3. for each source repo:
       a. collect tracked files via `git ls-files`
       b. apply exclusion blocklist (fnmatch + ** support)
       c. write file index entry
       d. for primary repos (xlotyl/stoneforge), write chunks per chunk_groups
       e. extract symbols via per-language regex pass
       f. write per-repo symbol index (markdown + JSON)
       g. write per-repo repo map
  4. write generated/source-manifest.json
  5. defensive secret scan over produced outputs; abort on hit

Comments throughout describe intended vs observed behavior so a future agent can
quickly confirm whether the generator is doing what the boundary docs say it does.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

# --- paths and config ------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "context-config.json"
GENERATED_DIR = ROOT_DIR / "generated"
GENERATOR_VERSION = "1.0.0"


def log(msg: str) -> None:
    print(f"generate.py: {msg}", flush=True)


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


# --- exclude matcher -------------------------------------------------------
# We translate the user's glob exclude_patterns into compiled regexes once,
# then test each path in O(patterns). This is the hot path for big repos.
def compile_excludes(patterns: list[str]) -> list[re.Pattern]:
    compiled = []
    for pat in patterns:
        regex = fnmatch.translate(pat)
        # Make ** behave a bit more sensibly across nested dirs.
        regex = regex.replace(".*.*.*", ".*")
        compiled.append(re.compile(regex))
    return compiled


def is_excluded(rel: str, compiled: list[re.Pattern]) -> bool:
    # Match either the full relative path, or any path segment, against the
    # compiled patterns. Segment-matching catches things like
    # "node_modules/**" matching deeply-nested files.
    parts = rel.split("/")
    for r in compiled:
        if r.match(rel):
            return True
        for seg in parts:
            if r.match(seg):
                return True
    return False


# --- git helpers -----------------------------------------------------------
def git_capture(cwd: Path, *args: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True, text=True, check=False
    )
    return out.stdout.strip()


def git_tracked_files(cwd: Path) -> list[str]:
    # Uses git's own ignore handling. We pass --cached --others --exclude-standard
    # so untracked-but-not-ignored files (e.g. brand-new code on a working
    # branch) are still mirrored.
    proc = subprocess.run(
        ["git", "-C", str(cwd), "ls-files",
         "--cached", "--others", "--exclude-standard"],
        capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


def git_dirty(cwd: Path) -> bool:
    a = subprocess.run(["git", "-C", str(cwd), "diff", "--quiet", "--ignore-submodules"]).returncode
    b = subprocess.run(["git", "-C", str(cwd), "diff", "--cached", "--quiet", "--ignore-submodules"]).returncode
    return a != 0 or b != 0


# --- language hints --------------------------------------------------------
LANG_BY_EXT = {
    ".ts": "ts", ".tsx": "ts", ".js": "js", ".mjs": "js", ".cjs": "js",
    ".jsx": "jsx", ".py": "python", ".json": "json", ".yml": "yaml",
    ".yaml": "yaml", ".md": "md", ".mdc": "md", ".toml": "toml",
    ".sh": "bash", ".bash": "bash", ".rs": "rust", ".go": "go",
    ".sql": "sql",
}


def language_for(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base.startswith("Dockerfile"):
        return "dockerfile"
    _, _, ext = base.rpartition(".")
    return LANG_BY_EXT.get("." + ext.lower(), "")


# --- symbol extraction -----------------------------------------------------
# Per-language regex patterns. We deliberately match top-of-line declarations
# only, so we don't pick up usages inside method bodies.
SYMBOL_PATTERNS_BY_EXT: dict[str, list[re.Pattern]] = {
    "ts": [
        re.compile(r"^\s*export\s+(?:async\s+)?(?:function|class|interface|type|enum|const|let)\s+(\w+)"),
        re.compile(r"^\s*(?:async\s+)?function\s+(\w+)"),
        re.compile(r"^\s*class\s+(\w+)"),
        re.compile(r"^\s*interface\s+(\w+)"),
        re.compile(r"^\s*type\s+(\w+)\s*="),
        re.compile(r"^\s*enum\s+(\w+)"),
    ],
    "py": [
        re.compile(r"^\s*def\s+(\w+)"),
        re.compile(r"^\s*async\s+def\s+(\w+)"),
        re.compile(r"^\s*class\s+(\w+)"),
    ],
    "rs": [
        re.compile(r"^\s*pub(?:\(\w+\))?\s+fn\s+(\w+)"),
        re.compile(r"^\s*fn\s+(\w+)"),
        re.compile(r"^\s*pub\s+struct\s+(\w+)"),
        re.compile(r"^\s*pub\s+enum\s+(\w+)"),
        re.compile(r"^\s*struct\s+(\w+)"),
        re.compile(r"^\s*enum\s+(\w+)"),
    ],
    "go": [
        re.compile(r"^\s*func\s+(\w+)"),
        re.compile(r"^\s*func\s+\([^)]+\)\s+(\w+)"),
        re.compile(r"^\s*type\s+(\w+)\s+(?:struct|interface)"),
    ],
}


EXT_TO_LANG_KEY = {
    ".ts": "ts", ".tsx": "ts", ".js": "ts", ".mjs": "ts", ".cjs": "ts", ".jsx": "ts",
    ".py": "py",
    ".rs": "rs",
    ".go": "go",
}


def extract_symbols(text: str, ext: str, max_lines: int = 5000) -> list[tuple[int, str]]:
    key = EXT_TO_LANG_KEY.get(ext)
    if not key:
        return []
    patterns = SYMBOL_PATTERNS_BY_EXT[key]
    out: list[tuple[int, str]] = []
    for i, line in enumerate(text.splitlines()[:max_lines], start=1):
        if len(line) > 400:
            continue
        for pat in patterns:
            if pat.match(line):
                out.append((i, line.strip()))
                break
        if len(out) > 500:
            break
    return out


# --- chunk writer ----------------------------------------------------------
def write_chunk(
    out_path: Path,
    repo_label: str,
    repo_gh: str,
    short_sha: str,
    branch: str,
    generated_at: str,
    group_name: str,
    include_paths: list[str],
    file_entries: list[tuple[str, Path, int]],
    per_file_cap: int,
) -> int:
    """
    Write a single domain chunk markdown file.

    file_entries: list of (relative_path, absolute_path, size_bytes) for files
    that fall under any include path.
    Returns: number of files actually inlined (not just listed/truncated).
    """
    inlined = 0
    with open(out_path, "w") as f:
        f.write(f"# {repo_label} :: {group_name}\n\n")
        f.write(
            f"_Generated by refresh.sh on {generated_at} from {repo_gh}@{short_sha} "
            f"({branch}). DO NOT EDIT — re-run ./refresh.sh to regenerate._\n\n"
        )
        f.write("Source roots included in this chunk:\n\n")
        for inc in include_paths:
            f.write(f"- `{inc}`\n")
        f.write("\n")

        if not file_entries:
            f.write("_No tracked files matched these source roots._\n")
            return 0

        for rel, full, size in file_entries:
            f.write("---\n\n")
            f.write(f"### `{rel}`\n\n")
            f.write(f"- repo: `{repo_gh}`\n")
            f.write(f"- size: {size} bytes\n\n")
            if size > per_file_cap:
                f.write(
                    f"_File exceeds per-file size cap ({per_file_cap} bytes); "
                    f"contents omitted. Read the live file at `{rel}` in `{repo_gh}`._\n\n"
                )
                continue
            try:
                with open(full, "rb") as fh:
                    raw = fh.read()
                # Skip files that look binary (NUL byte heuristic).
                if b"\x00" in raw[:8192]:
                    f.write("_Binary file; contents omitted._\n\n")
                    continue
                text = raw.decode("utf-8", errors="replace")
            except OSError:
                f.write("_Could not read file; contents omitted._\n\n")
                continue

            lang = language_for(rel)
            fence_open = f"```{lang}" if lang else "```"
            f.write(f"{fence_open}\n")
            # Defensive: if the file itself contains a triple backtick, switch
            # to a 4-backtick fence so we don't break markdown rendering.
            if "```" in text:
                f.seek(f.tell() - len(fence_open) - 1)  # rewind
                f.truncate()
                fence_open = ("`" * 4) + (lang if lang else "")
                f.write(f"{fence_open}\n")
                f.write(text)
                if not text.endswith("\n"):
                    f.write("\n")
                f.write(("`" * 4) + "\n\n")
            else:
                f.write(text)
                if not text.endswith("\n"):
                    f.write("\n")
                f.write("```\n\n")
            inlined += 1
    return inlined


# --- main per-repo processor -----------------------------------------------
def process_repo(repo_cfg: dict, cfg: dict, generated_at: str, compiled: list[re.Pattern]) -> dict:
    name = repo_cfg["name"]
    rel_path = repo_cfg["path"]
    gh_repo = repo_cfg["repo"]
    src_path = (ROOT_DIR / rel_path).resolve()

    log(f"source repo [{name}] at {src_path}")

    if not src_path.is_dir() or not (src_path / ".git").exists():
        return {
            "name": name, "repo": gh_repo, "path": rel_path,
            "status": "skipped", "reason": "missing-or-not-a-git-repo",
        }

    sha = git_capture(src_path, "rev-parse", "HEAD")
    short_sha = git_capture(src_path, "rev-parse", "--short", "HEAD")
    branch = git_capture(src_path, "rev-parse", "--abbrev-ref", "HEAD")
    dirty = git_dirty(src_path)

    # Tracked + intentionally-included new files.
    raw_files = git_tracked_files(src_path)
    log(f"  raw tracked files: {len(raw_files)}")
    filtered = [r for r in raw_files if not is_excluded(r, compiled)]
    log(f"  after excludes:    {len(filtered)}")

    # --- file index ---
    file_index: list[dict] = []
    for rel in filtered:
        full = src_path / rel
        try:
            size = full.stat().st_size
        except OSError:
            size = -1
        file_index.append({"repo": name, "path": rel, "size_bytes": size})
    with open(GENERATED_DIR / f"file-index.{name}.json", "w") as f:
        json.dump(file_index, f, indent=2)

    # --- chunks (only for primary repos) ---
    chunk_key = {"xlotyl": "xlotyl_chunks", "stoneforge": "stoneforge_chunks"}.get(name)
    chunks_written = 0
    if chunk_key:
        groups: dict[str, list[str]] = cfg.get(chunk_key, {})
        chunk_dir = ROOT_DIR / name / "chunks"
        chunk_dir.mkdir(parents=True, exist_ok=True)
        per_file_cap = int(cfg.get("per_file_size_limit_bytes", 200_000))

        # Build a path-index once for fast prefix matching.
        for group_name, includes in groups.items():
            entries: list[tuple[str, Path, int]] = []
            for rel in filtered:
                if any(rel == inc or rel.startswith(inc + "/") for inc in includes):
                    full = src_path / rel
                    try:
                        size = full.stat().st_size
                    except OSError:
                        continue
                    entries.append((rel, full, size))
            entries.sort()
            out_path = chunk_dir / f"{group_name}.md"
            write_chunk(
                out_path=out_path,
                repo_label=name,
                repo_gh=gh_repo,
                short_sha=short_sha,
                branch=branch,
                generated_at=generated_at,
                group_name=group_name,
                include_paths=includes,
                file_entries=entries,
                per_file_cap=per_file_cap,
            )
            log(f"  chunk {group_name}: {len(entries)} files")
            chunks_written += 1

    # --- symbol extraction ---
    # Only do the symbol pass for primary repos. Supporting forks
    # (claw-code, void, openclaw) would contribute tens of thousands of
    # symbols each, blowing up generated/symbol-index.json into something
    # no chat agent could consume. We still file-index them so the manifest
    # records what's there.
    if not repo_cfg.get("primary"):
        log("  skipping symbol pass (non-primary repo)")
        return {
            "name": name, "repo": gh_repo, "path": rel_path,
            "status": "ok",
            "commit_sha": sha, "short_sha": short_sha,
            "branch": branch, "dirty": dirty,
            "file_count": len(filtered),
            "chunks_written": chunks_written,
            "symbols_indexed": False,
        }

    # We bound work per file so a freakishly large generated file doesn't
    # explode the symbol pass.
    symbols: list[dict] = []
    for rel in filtered:
        ext = "." + rel.rsplit(".", 1)[-1].lower() if "." in rel else ""
        if ext not in EXT_TO_LANG_KEY:
            continue
        full = src_path / rel
        try:
            size = full.stat().st_size
        except OSError:
            continue
        if size > 500_000:
            # Big files (e.g. transpiled bundles) — skip symbol pass.
            continue
        try:
            with open(full, "rb") as fh:
                raw = fh.read()
            if b"\x00" in raw[:4096]:
                continue
            text = raw.decode("utf-8", errors="replace")
        except OSError:
            continue
        for line_no, sig in extract_symbols(text, ext):
            symbols.append({
                "repo": name, "path": rel,
                "line": line_no, "signature": sig,
            })
    with open(GENERATED_DIR / f"symbol-index.{name}.json", "w") as f:
        json.dump(symbols, f, indent=2)
    log(f"  symbols: {len(symbols)}")

    # --- per-repo human-readable symbol index ---
    if name in ("xlotyl", "stoneforge"):
        md_target = ROOT_DIR / name / "03-symbol-index.md"
        buckets: dict[str, list[dict]] = {}
        for entry in symbols:
            buckets.setdefault(entry["path"], []).append(entry)
        with open(md_target, "w") as f:
            f.write(f"# {name} symbol index\n\n")
            f.write(
                f"_Generated by refresh.sh on {generated_at} from "
                f"{gh_repo}@{short_sha} ({branch})._\n\n"
            )
            f.write(
                "Quick navigation aid only. Real signatures live in the "
                "`chunks/` files; this is a path index.\n\n"
            )
            for path in sorted(buckets):
                f.write(f"### `{path}`\n\n")
                for e in buckets[path][:60]:
                    sig = e["signature"]
                    if len(sig) > 200:
                        sig = sig[:200] + " …"
                    f.write(f"- L{e['line']}: `{sig}`\n")
                if len(buckets[path]) > 60:
                    f.write(
                        f"- … {len(buckets[path]) - 60} more symbols truncated.\n"
                    )
                f.write("\n")

    # --- per-repo map ---
    if name in ("xlotyl", "stoneforge"):
        map_target = ROOT_DIR / name / "01-repo-map.md"
        with open(map_target, "w") as f:
            f.write(f"# {name} repo map\n\n")
            f.write(
                f"_Generated by refresh.sh on {generated_at} from "
                f"{gh_repo}@{short_sha} ({branch})._\n\n"
            )
            f.write("## Top-level entries\n\n")
            for entry in sorted(src_path.iterdir()):
                if not entry.is_dir():
                    continue
                if is_excluded(entry.name + "/", compiled):
                    continue
                f.write(f"- `{entry.name}/`\n")
            f.write("\n## Tracked file count (post-exclude)\n\n")
            f.write(f"{len(filtered)} files.\n\n")
            f.write("## Notable files\n\n")
            notable_basenames = {
                "package.json", "pyproject.toml", "tsconfig.json",
                "Cargo.toml", "go.mod", "AGENTS.md", "README.md",
            }
            for rel in filtered:
                base = rel.rsplit("/", 1)[-1]
                if base in notable_basenames:
                    f.write(f"- `{rel}`\n")
            f.write("\n")

    return {
        "name": name, "repo": gh_repo, "path": rel_path,
        "status": "ok",
        "commit_sha": sha, "short_sha": short_sha,
        "branch": branch, "dirty": dirty,
        "file_count": len(filtered),
        "chunks_written": chunks_written,
        "symbols_indexed": True,
        "symbol_count": len(symbols),
    }


# --- main ------------------------------------------------------------------
def main() -> int:
    cfg = load_config()
    compiled = compile_excludes(cfg.get("exclude_patterns", []))
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log(f"starting at {generated_at}")

    # --- step 1: clean regenerable outputs (callers handle this in shell) ---
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    # --- step 2: per-repo processing ---
    repo_entries: list[dict] = []
    for repo_cfg in cfg["source_repos"]:
        try:
            entry = process_repo(repo_cfg, cfg, generated_at, compiled)
        except Exception as exc:
            log(f"  WARN: {repo_cfg.get('name')} failed: {exc!r}")
            entry = {
                "name": repo_cfg.get("name"),
                "repo": repo_cfg.get("repo"),
                "path": repo_cfg.get("path"),
                "status": "error",
                "error": repr(exc),
            }
        repo_entries.append(entry)

    # --- step 3: roll up indexes ---
    # Roll-up files contain ONLY primary repos (xlotyl, stoneforge). Supporting
    # repos keep their per-repo file-index for the manifest record but are not
    # mixed in — that would make the rolled-up indexes too large for chat
    # agents to consume.
    log("rolling up indexes (primary repos only)")
    primary_names = {r["name"] for r in cfg["source_repos"] if r.get("primary")}
    file_index_all: list[dict] = []
    symbol_index_all: list[dict] = []
    for repo_entry in repo_entries:
        name = repo_entry.get("name")
        if name not in primary_names:
            continue
        fi = GENERATED_DIR / f"file-index.{name}.json"
        if fi.exists():
            with open(fi) as f:
                file_index_all.extend(json.load(f))
        si = GENERATED_DIR / f"symbol-index.{name}.json"
        if si.exists():
            with open(si) as f:
                symbol_index_all.extend(json.load(f))
    with open(GENERATED_DIR / "file-index.json", "w") as f:
        json.dump(file_index_all, f, indent=2)
    with open(GENERATED_DIR / "symbol-index.json", "w") as f:
        json.dump(symbol_index_all, f, indent=2)

    # chunk-index.json
    chunk_index: list[dict] = []
    for repo in ("xlotyl", "stoneforge"):
        cdir = ROOT_DIR / repo / "chunks"
        if not cdir.is_dir():
            continue
        for entry in sorted(cdir.iterdir()):
            if entry.suffix != ".md":
                continue
            chunk_index.append({
                "repo": repo,
                "chunk": entry.stem,
                "path": str(entry.relative_to(ROOT_DIR)),
                "size_bytes": entry.stat().st_size,
            })
    with open(GENERATED_DIR / "chunk-index.json", "w") as f:
        json.dump(chunk_index, f, indent=2)

    # --- step 4: source manifest + human-readable freshness card ---
    log("writing source-manifest.json")
    manifest = {
        "schema_version": "1.0.0",
        "generator_version": GENERATOR_VERSION,
        "generated_at": generated_at,
        "refresh_command": "./refresh.sh",
        "exclude_patterns": cfg.get("exclude_patterns", []),
        "repos": repo_entries,
    }
    with open(GENERATED_DIR / "source-manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # FRESHNESS.md is the markdown projection of source-manifest.json. Many
    # chat agents read markdown more reliably than JSON, so we expose both.
    # This file is regenerated on every refresh — do not edit by hand.
    log("writing FRESHNESS.md")
    with open(GENERATED_DIR / "FRESHNESS.md", "w") as f:
        f.write("# Freshness\n\n")
        f.write(
            "_Markdown projection of `source-manifest.json`. "
            "Regenerated by `./refresh.sh`. DO NOT EDIT._\n\n"
        )
        f.write(f"**Generated:** `{generated_at}`\n\n")
        f.write(f"**Generator version:** `{GENERATOR_VERSION}`\n\n")
        f.write(f"**Refresh command:** `./refresh.sh`\n\n")
        f.write("## Source repos\n\n")
        f.write(
            "| name | repo | branch | short sha | dirty | files | chunks | symbols indexed |\n"
            "| ---- | ---- | ------ | --------- | ----- | ----- | ------ | --------------- |\n"
        )
        for r in repo_entries:
            if r.get("status") != "ok":
                f.write(
                    f"| {r.get('name','?')} | {r.get('repo','?')} | "
                    f"_skipped: {r.get('reason') or r.get('error') or r.get('status')}_ "
                    f"| — | — | — | — | — |\n"
                )
                continue
            f.write(
                f"| {r['name']} | `{r['repo']}` | `{r['branch']}` | "
                f"`{r['short_sha']}` | "
                f"{'**yes**' if r.get('dirty') else 'no'} | "
                f"{r.get('file_count', 0)} | "
                f"{r.get('chunks_written', 0)} | "
                f"{'yes' if r.get('symbols_indexed') else 'no'} |\n"
            )
        f.write("\n")
        f.write("## How to use this card\n\n")
        f.write(
            "- If `Generated` is older than the operator's expectation, "
            "ask for `./refresh.sh` to be re-run.\n"
            "- If a primary repo has `dirty: yes`, the chunks reflect "
            "uncommitted working-tree state on the operator's machine — flag it.\n"
            "- If a primary repo's `short sha` doesn't match what the operator "
            "is currently working on, the chunks are out of date for that repo.\n"
        )

    # --- step 5: secret scan ---
    log("running defensive secret scan over generated outputs")
    targets = [
        ROOT_DIR / "xlotyl" / "chunks",
        ROOT_DIR / "stoneforge" / "chunks",
        GENERATED_DIR,
    ]
    # The patterns below require an actual *value* after a key name, so
    # source code that *names* a key (e.g. a regex that detects AWS secrets,
    # or a variable named `aws_secret_access_key` in a struct definition)
    # does not trigger a false positive. We only fire when something looks
    # like an actual leaked credential value.
    secret_pattern = re.compile(
        r"(-----BEGIN [A-Z ]*PRIVATE KEY-----"
        r"|aws_secret_access_key\s*[:=]\s*[\"'][A-Za-z0-9/+=]{30,}[\"']"
        r"|aws_access_key_id\s*[:=]\s*[\"']?AKIA[A-Z0-9]{14,}"
        r"|api[_-]?key\s*[:=]\s*[\"'][A-Za-z0-9+/]{32,}[\"']"
        r"|password\s*[:=]\s*[\"'][^\"'\s${}]{14,}[\"']"
        r"|x-?api-?key\s*[:=]\s*[\"'][A-Za-z0-9_-]{32,}[\"']"
        r"|gh[ps]_[A-Za-z0-9]{30,}"
        r"|sk-[A-Za-z0-9]{30,}"
        r"|xox[abprs]-[A-Za-z0-9-]{20,})",
        re.IGNORECASE,
    )
    hits: list[str] = []
    for target in targets:
        if not target.exists():
            continue
        for path in target.rglob("*"):
            if not path.is_file():
                continue
            try:
                with open(path, "rb") as fh:
                    raw = fh.read()
                if b"\x00" in raw[:4096]:
                    continue
                text = raw.decode("utf-8", errors="replace")
            except OSError:
                continue
            for m in secret_pattern.finditer(text):
                hits.append(f"{path.relative_to(ROOT_DIR)}: {m.group(0)[:120]}")
                if len(hits) > 30:
                    break
            if len(hits) > 30:
                break
    if hits:
        print(
            "generate.py: SECRET-LIKE CONTENT DETECTED in generated outputs:",
            file=sys.stderr,
        )
        for h in hits:
            print("  " + h, file=sys.stderr)
        print(
            "generate.py: ABORTING. Inspect the listed lines and either "
            "tighten exclude_patterns or scrub the source.",
            file=sys.stderr,
        )
        return 3
    log("secret scan clean")

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
