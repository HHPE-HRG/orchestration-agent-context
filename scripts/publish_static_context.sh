#!/usr/bin/env bash
# publish_static_context.sh — assemble a static-site bundle from this mirror.
#
# Module purpose:
#   Take the markdown surfaces (boundary docs, integration docs, overviews,
#   chunks, AGENTS, README, freshness) and copy them into a single _site/
#   directory ready to upload to any static host (Cloudflare Pages, Netlify,
#   GitHub Pages, internal docs portal). Adds a minimal index.html that links
#   to the markdown files so the bundle is browsable without a markdown
#   renderer.
#
#   This script does NOT publish anything itself. It only builds the bundle
#   locally. Publishing is the operator's deliberate next step (so the
#   private-vs-public access decision stays explicit).
#
# Process flow:
#   1. validate that we're at the repo root
#   2. wipe and recreate _site/
#   3. copy the markdown surfaces (preserving directory structure)
#   4. copy the generated/ artifacts (file/symbol/chunk indexes, manifest, FRESHNESS.md)
#   5. write _site/index.html as a thin landing page
#   6. print upload instructions
#
# Comments above each step describe intended behavior so a future agent can
# verify the script is doing what its name claims.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "$ROOT_DIR/context-config.json" ]]; then
  echo "publish_static_context.sh: must be run from the repo root (context-config.json not found)" >&2
  exit 2
fi

SITE_DIR="$ROOT_DIR/_site"
echo "publish_static_context.sh: assembling static bundle at $SITE_DIR"

# --- step 2: clean target ------------------------------------------------
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR"

# --- step 3: copy markdown surfaces -------------------------------------
# We copy explicitly named files/dirs rather than `cp -r .` so build artefacts
# (.git, _site itself, scripts/__pycache__, etc.) don't sneak in.
for src in \
    README.md \
    AGENTS.md \
    START_HERE.md \
    HOW_TO_QUERY_CONTEXT.md \
    context-config.json \
    .gitignore \
    refresh.sh \
    scripts \
    xlotyl \
    stoneforge \
    claw-code \
    void \
    openclaw \
    integration \
    tasks \
    generated; do
  if [[ -e "$ROOT_DIR/$src" ]]; then
    cp -R "$ROOT_DIR/$src" "$SITE_DIR/"
  fi
done

# --- step 5: write a tiny landing page so a browser can open _site/ -----
cat > "$SITE_DIR/index.html" <<'HTML'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HHPE-HRG · orchestration-agent-context</title>
<style>
  body { font-family: ui-sans-serif, system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #1a1a1a; }
  h1 { font-size: 1.5rem; }
  h2 { font-size: 1.1rem; margin-top: 2rem; }
  ul { padding-left: 1.25rem; }
  code { background: #f3f3f3; padding: 0.1em 0.35em; border-radius: 3px; }
  a { color: #0a58ca; text-decoration: none; }
  a:hover { text-decoration: underline; }
  .note { background: #fff8e1; border-left: 3px solid #f5a623; padding: 0.5rem 0.75rem; margin: 1rem 0; }
</style>
</head>
<body>
<h1>HHPE-HRG · orchestration-agent-context</h1>
<p>Generated, agent-readable context mirror of the HHPE-HRG orchestration repos. <strong>Not source of truth.</strong></p>

<div class="note">
  This is a static bundle of the markdown surfaces in
  <code>HHPE-HRG/orchestration-agent-context</code>. Any chat agent reading
  this site should start with <a href="START_HERE.md">START_HERE.md</a> and
  <a href="AGENTS.md">AGENTS.md</a>.
</div>

<h2>Read in this order</h2>
<ul>
  <li><a href="START_HERE.md">START_HERE.md</a></li>
  <li><a href="AGENTS.md">AGENTS.md</a></li>
  <li><a href="HOW_TO_QUERY_CONTEXT.md">HOW_TO_QUERY_CONTEXT.md</a></li>
  <li><a href="integration/00-xlotyl-stoneforge-boundary.md">integration/00-xlotyl-stoneforge-boundary.md</a></li>
  <li><a href="integration/06-current-roadmap.md">integration/06-current-roadmap.md</a></li>
</ul>

<h2>Per-repo entry points</h2>
<ul>
  <li><a href="xlotyl/00-boundary.md">xlotyl/00-boundary.md</a></li>
  <li><a href="stoneforge/00-boundary.md">stoneforge/00-boundary.md</a></li>
  <li><a href="claw-code/00-overview.md">claw-code/00-overview.md</a></li>
  <li><a href="void/00-overview.md">void/00-overview.md</a></li>
  <li><a href="openclaw/00-overview.md">openclaw/00-overview.md</a></li>
</ul>

<h2>Freshness</h2>
<ul>
  <li><a href="generated/FRESHNESS.md">generated/FRESHNESS.md</a> — human-readable</li>
  <li><a href="generated/source-manifest.json">generated/source-manifest.json</a> — machine-readable</li>
</ul>

<p style="margin-top:3rem; color:#666; font-size:0.85rem;">
  Built by <code>scripts/publish_static_context.sh</code>. Re-run <code>./refresh.sh</code> in the source repo to regenerate.
</p>
</body>
</html>
HTML

# Marker file: ensures GitHub Pages skips Jekyll, since markdown is what we
# expose (raw markdown files plus the index.html above). If you want Jekyll
# rendering on Pages, delete this file before uploading.
touch "$SITE_DIR/.nojekyll"

# --- step 6: print upload instructions ---------------------------------
SIZE=$(du -sh "$SITE_DIR" | awk '{print $1}')
echo "publish_static_context.sh: built $SITE_DIR ($SIZE)"
echo ""
echo "Next steps (operator decision required — none of these run automatically):"
echo ""
echo "  Cloudflare Pages:  wrangler pages deploy _site --project-name <project>"
echo "  Netlify:           netlify deploy --dir=_site --prod"
echo "  GitHub Pages:      enable Pages in repo settings, then trigger"
echo "                     .github/workflows/publish-static.yml manually"
echo "  Internal share:    rsync -avz _site/ <host>:<path>"
echo ""
echo "All of the above expose the bundle to anyone with the URL."
echo "Confirm sensitivity before publishing publicly."
