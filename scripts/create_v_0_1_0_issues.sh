#!/usr/bin/env bash
set -euo pipefail
MS="v0.1.0 – First Release"


# A) Foundations
gh issue create --title "Repo skeleton: src/ layout + packaging (hatchling)" \
--body "Set up src/ layout; fix editable install; add uv lockfile.\n\nAC:\n- [ ] Editable install works with uv\n- [ ] pyproject configured (hatchling)\n- [ ] CI builds" \
--label infra --milestone "$MS"


gh issue create --title "CI: lint + test matrix (3.11/3.12)" \
--body "GitHub Actions with ruff, black, pytest; cache uv.\nAC:\n- [ ] Lint job\n- [ ] Test matrix\n- [ ] Coverage artifact" \
--label infra --milestone "$MS"


# B) YT Music Client
gh issue create --title "Auth: import headers + status command" \
--body "Implement 'sortune auth import-headers <path>' and 'sortune auth status'.\nAC:\n- [ ] Validates headers\n- [ ] Clear errors + docs" \
--label core --label cli --milestone "$MS"


gh issue create --title "Playlists: list + export to CSV/JSON" \
--body "List user playlists, export tracks/metadata.\nAC:\n- [ ] 'sortune playlists list'\n- [ ] 'sortune playlists export --id <id> --to csv|json'" \
--label core --label api --milestone "$MS"


# C) Core Ops
gh issue create --title "Dedupe: exact (videoId) with dry-run + apply + undo" \
--body "Exact duplicate detection and removal with JSON undo patch.\nAC:\n- [ ] '--dry-run' report\n- [ ] '--apply' changes\n- [ ] 'undo' restores" \
--label core --milestone "$MS"


gh issue create --title "Dedupe: fuzzy (normalized title+artists) with thresholds" \
--body "Fuzzy match with conservative defaults; preview diff.\nAC:\n- [ ] Threshold config\n- [ ] False-positive guardrails\n- [ ] Tests with edge cases" \
--label core --milestone "$MS"


gh issue create --title "Sorting strategies + stable sort" \
--body "Sort by added date, title, artist, album, duration.\nAC:\n- [ ] Stable across runs\n- [ ] CLI flags documented" \
--label core --milestone "$MS"


gh issue create --title "Filter language → predicate compiler" \
--body "Mini query language (field:op:value), supports likeStatus, inLibrary, contains, duration range.\nAC:\n- [ ] Parser + validators\n- [ ] Tests covering operators" \
--label core --milestone "$MS"


gh issue create --title "Bulk remove/move with dry-run" \
--body "Remove by filter; move/copy between playlists.\nAC:\n- [ ] 'remove' and 'move' subcommands\n- [ ] Dry-run preview\n- [ ] Undo file" \
--label core --milestone "$MS"


# D) AI Assist (Optional)
gh issue create --title "AI provider interface + deterministic seed" \
--body "Define BaseLLM interface; seedable prompts; provider selection.\nAC:\n- [ ] Provider abstraction\n- [ ] Config + env support" \
--label optional --label ai --milestone "$MS"


gh issue create --title "Ollama provider (local default)" \
--body "Local-first tags/description generation; model configurable.\nAC:\n- [ ] Works offline\n- [ ] Deterministic mode" \
--label optional --label ai --milestone "$MS"


# E) Reports
gh issue create --title "Export utilities: CSV/JSON + HTML report (Jinja2)" \
--body "Writers for CSV/JSON and styled HTML summaries with diffs.\nAC:\n- [ ] '--report out/report.html'\n- [ ] Includes version, command, decisions" \
--label core --milestone "$MS"


# F) CLI & UX
gh issue create --title "Typer CLI scaffolding + global flags" \
--body "Typer app with --dry-run everywhere, --verbose/--quiet, consistent exit codes.\nAC:\n- [ ] Subcommands mapped to ops\n- [ ] Rich tables + progress" \
--label infra --label cli --milestone "$MS"


# G) Docs
gh issue create --title "README Quickstart + SECURITY + recipes" \
--body "Auth headers how-to; example flows; data handling notes.\nAC:\n- [ ] README\n- [ ] SECURITY.md\n- [ ] Example recipes" \
--label docs --milestone "$MS"


# H) Testing
gh issue create --title "Test suite: unit (ops) + integration toggled by env" \
--body "Pytest with fixtures for synthetic playlists; live tests behind env flag.\nAC:\n- [ ] Unit tests for ops\n- [ ] Integration tests (@slow)" \
--label infra --milestone "$MS"


# Release meta
gh issue create --title "Release v0.1.0 checklist" \
--body "Track final steps to cut v0.1.0. See acceptance list in issue body." \
--label release --milestone "$MS"