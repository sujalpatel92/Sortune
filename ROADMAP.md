# Roadmap

This document outlines the planned milestones and release versions for the **YouTube Music Playlist Manager (YT Music Experiments)** project.  
We follow **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`.

---

## v0.1.0 — Foundations

**Goal:** Establish core plumbing.

- CLI authentication and fetch library.
- Local cache (SQLite) with minimal schema.
- Config/secrets management (`.env`).
- Logging, error handling, unit tests.

✅ **Exit Criteria:** Fetch ≥2k tracks without errors; warm cache ≥10× faster than cold.

---

## v0.2.0 — Curation Core

**Goal:** Enable basic playlist hygiene.

- Deduplication (videoId + fuzzy matching).
- Bulk ops: move, copy, merge, split playlists.
- Smart sorting (date, energy proxy, popularity).
- Tagging system (CRUD + auto-tags).

✅ **Exit Criteria:** One-click dedupe; tag CRUD working; dry-run mode for all ops.

---

## v0.3.0 — Rules & Recipes

**Goal:** Repeatable, automatable curation.

- Playlist recipes (YAML/JSON).
- Scheduled rebuilds (cron-style).
- Conflict detection + safe mode.

✅ **Exit Criteria:** Run a recipe to produce a fresh playlist reproducibly.

---

## v0.4.0 — Discovery Assist

**Goal:** Help find great additions.

- Related-track graph (artist overlap, co-appearances).
- “Fill the vibe” recommender (metadata-based).
- Quick-add UX via CLI TUI or minimal web UI.

✅ **Exit Criteria:** Suggestions feel on-theme; <1s latency from cache.

---

## v0.5.0 — LLM Enrichment (Opt-In)

**Goal:** Add lightweight AI features.

- Track/artist short notes cached locally.
- Natural-language filters → recipe translation.
- Confirmation diff for edits.

✅ **Exit Criteria:** NL → recipe translation reaches ≥85% precision on curated test set.

---

## v0.6.0 — Sync & Portability

**Goal:** Safe adoption & portability.

- Import/export recipes (JSON), playlist snapshots (CSV).
- Backup/restore cache; migration scripts.
- Idempotent writes; retry & backoff logic.

✅ **Exit Criteria:** Backup/restore of 10k-track library with no data loss.

---

## v0.7.0 — Automations

**Goal:** “Set it and forget it.”

- Triggers: new releases, new likes, stale playlists.
- Notifiers: email/Discord/Slack.
- Auto-apply tagged rules.

✅ **Exit Criteria:** At least 2 reliable automations run for 1 week.

---

## v0.8.0 — UX Polish

**Goal:** Minimal, pleasant UI.

- Responsive web UI: library explorer, recipe builder, preview diffs.
- Progress bars, rollback, shortcuts.
- Multi-account session profiles.

✅ **Exit Criteria:** End-to-end flows possible without CLI.

---

## v0.9.0 — Quality & Hardening

**Goal:** Production readiness.

- Test coverage ≥70%; fuzz tests for title/artist normalization.
- Performance improvements: parallel fetch, lazy hydration.
- Observability: structured logs, metrics, traces.

✅ **Exit Criteria:** P95 fetch <2s from warm cache; no known data-losing bugs.

---

## v1.0.0 — Stable

**Goal:** Lock dependable baseline.

- Versioned REST API with extension hooks.
- Security review (secrets, tokens, PII).
- Documentation: quickstart, recipes gallery, ops handbook.

✅ **Exit Criteria:** Fresh install → curated playlist in <15 minutes using only docs.

---

## Release Cadence

- **Minors**: ~every 2 weeks until v1.0.  
- **Patches**: As needed for fixes.  
- All releases tagged with changelog (Keep a Changelog format).

---

## Key Principles

- **Dry-run by default** for any write.  
- **Local-first** cache; explicit opt-in for AI enrichment.  
- **Reproducibility**: every action produces a diff & log.  
- **Portability**: import/export for recipes & snapshots.  

---

## Metrics to Track

- Library sync time (cold vs warm).  
- Dedupe precision/recall.  
- Suggestion acceptance rate.  
- Automation success/rollback count.  
- Crash-free sessions; P95 latencies.  

---

## Risks & Mitigations

- **API fragility / rate limits** → Retry/backoff, offline cache workflows.  
- **Metadata inconsistencies** → Layered matchers (ID > exact > fuzzy), human confirm.  
- **Scope creep** → Recipes as contract; everything expressed as recipes.  
