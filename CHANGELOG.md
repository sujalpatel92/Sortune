# Changelog

## [0.0.5] - 2025-08-31



### Added

- enhance CI workflow and testing (d3e7f81…)



### Chore

- update for v0.0.4 (e8ffe85…)

- add version files to gitignore (dc2294d…)

- remove version files from version control (a300aa8…)



### Fixed

- Allow multiple --strip arguments in git-cliff command (96324e8…)

- Proper strip command value (fe2a9e3…)



## [0.0.4] - 2025-08-31



### Added

- Add AGENT_ONBOARDING.md for AI agents (392cdfe…)

- integrate YouTube Music via ytmusicapi across API and UI (897afb1…)

- Implement YouTube Music playlist import and model updates (99c5e3a…)

- enable persistence with volume and appendonly mode (78e1fe9…)

- implement LLM-powered playlist name suggestions (28a1547…)



### Build/CI

- prepend single release section and set PR metadata (ec4a9ae…)

- export SETUPTOOLS_SCM_PRETEND_VERSION from latest tag (6c8e5c2…)

- fix shell syntax and export version/compose env (18520fc…)



### Changed

- migrate to src/ layout for all Python packages (d827a2d…)



### Chore

- add v0.0.3 (8442efd…)

- cleanup duplicates (db3b9b9…)

- add repo state generator and bump versions to 0.0.3 (110bec4…)

- improve type hints in LangChain LLM provider (9420acf…)



### Docs

- rewrite AGENT_ONBOARDING with quickstart, versioning, and CI details (1731e2e…)

- add project documentation for development guidelines and setup (5bfdaae…)



### Tests

- add live API and client mapping tests; update fixtures (3b03517…)



## [0.0.3] - 2025-08-24



### Chore

- add v0.0.2 (f37e6c3…)



### Fixed

- Correct git-cliff range argument (187f16b…)



## [0.0.2] - 2025-08-24



### Fixed

- resolve workflow errors and update actions (bd4ac86…)

- resolve workflow errors and update actions (e6b0d86…)



## [0.0.1] - 2025-08-24



### Build/CI

- improve release workflows; tidy Makefile comments (4930dc3…)



## [0.0.0] - 2025-08-24



### Added

- add YouTube Music tools and LLM tagging; update deps (a73c941…)

- add Docker dev stack and project scaffolding (b5148c8…)

- scaffold services, Redis repo, sorting rule, demo UI, and tests (214eb48…)

- add GitHub CI workflow (c6505a0…)



### Build/CI

- add release-drafter config and publish workflow; docs: add CHANGELOG and ROADMAP (fc9783e…)

- adopt git-cliff release flow and manual changelog PR workflow (bbf8a9a…)

- adopt hatch-vcs across monorepo and expose __version__ (b605961…)

- checkout with full history and tags for workflows (babfce1…)



### Chore

- add genrate-commit-message workflow (a0e2c6b…)

- expand .gitignore for Python, envs, IDE, and OS artifacts (ec4aa9b…)

- initialize Python project and update workflow (2b9ae06…)

- ignore env, credentials, and cache artifacts (569738f…)

- broaden .gitignore for tooling, data, and cache (8b95ac5…)

- run uv with --no-project for dev cmds (936f335…)

- add GitHub issue and PR templates; chore(scripts): add v0.1.0 issue bootstrap script (52c36cb…)

- reset package versions to 0.0.0 across monorepo (5430b94…)

- integrate setuptools-scm and improve local install flow (1ab2e83…)

- standardize Hatch VCS versioning across apps and packages (97d6893…)



### Docs

- revamp README with badges, quick start, dev.sh, and architecture (c2e68f3…)



### Fixed

- create virtual environment in CI (16d8554…)

- fix E501 line length errors in code (014be7f…)

- repair git-cliff template formatting and parsing (6b2e482…)




