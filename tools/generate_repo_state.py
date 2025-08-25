#!/usr/bin/env python3
"""
Generate repo_state.json (machine) and REPO_STATE.md (human).
Safe to run in any repo without internet. Python 3.10+ recommended.
"""
import os, re, json, sys, subprocess, pathlib, hashlib
from datetime import datetime, UTC

ROOT = pathlib.Path.cwd()

def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip()

def read_text(paths):
    for p in paths:
        f = ROOT / p
        if f.exists() and f.is_file():
            try:
                return f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                return ""
    return ""

def list_files():
    out = sh(r'git ls-files 2>/dev/null')
    if out:
        return out.splitlines()
    # Fallback if not a git repo
    files = []
    for p in ROOT.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            files.append(str(p.relative_to(ROOT)))
    return files

def file_digest(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()[:12]
    except Exception:
        return None

def detect_langs(files):
    exts = {}
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        exts[ext] = exts.get(ext, 0) + 1
    top = sorted(exts.items(), key=lambda x: (-x[1], x[0]))[:12]
    return [{"ext": k or "(no-ext)", "count": v} for k, v in top]

def grep_versions():
    data = {}
    # Python
    for fn in ("pyproject.toml","requirements.txt","Pipfile","environment.yml"):
        txt = read_text([fn])
        if txt:
            data.setdefault("python", {})[fn] = txt
    # Node
    pkg = read_text(["package.json"])
    if pkg:
        data.setdefault("node", {})["package.json"] = pkg
        lock = read_text(["package-lock.json","pnpm-lock.yaml","yarn.lock"])
        if lock: data["node"]["lockfile"] = lock
    # Docker
    for fn in ("Dockerfile","docker-compose.yml","compose.yml","compose.yaml"):
        txt = read_text([fn])
        if txt: data.setdefault("docker", {})[fn] = txt
    return data

def parse_make_targets():
    mk = read_text(["Makefile"])
    if not mk: return []
    targets = []
    for line in mk.splitlines():
        m = re.match(r"^([A-Za-z0-9._-]+):.*", line)
        if m and not m.group(1).startswith("."):
            targets.append(m.group(1))
    return sorted(set(targets))

def ci_workflows():
    ci = {}
    wf_dir = ROOT / ".github" / "workflows"
    if wf_dir.exists():
        for yml in sorted(wf_dir.glob("*.y*ml")):
            try:
                ci[yml.name] = yml.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass
    return ci

def git_meta():
    def safe(cmd): 
        out = sh(cmd)
        return out if out else None
    return {
        "is_git_repo": (ROOT/".git").exists(),
        "current_branch": safe("git rev-parse --abbrev-ref HEAD"),
        "latest_commit": safe("git log -1 --pretty=%H%n%an%n%ae%n%ad%n%s"),
        "tags": safe("git tag --sort=-creatordate | head -n 30"),
        "remotes": safe("git remote -v"),
        "status": safe("git status --porcelain=v1"),
        "recent_commits": safe("git log --date=iso --pretty=format:%h%x09%ad%x09%an%x09%s -n 50"),
    }

def test_info():
    # Basic heuristics
    files = list_files()
    test_dirs = [f for f in files if re.search(r"(^|/)(tests?|spec)(/|$)", f)]
    pytest_ini = read_text(["pytest.ini","pyproject.toml","tox.ini"])
    jest_cfg = read_text(["jest.config.js","jest.config.ts","package.json"])
    return {
        "test_paths_sample": test_dirs[:50],
        "python_test_config": pytest_ini if pytest_ini else None,
        "js_test_config": jest_cfg if jest_cfg else None,
    }

def parse_env_lines(txt: str) -> dict:
    """Return VAR names only (values redacted)."""
    env = {}
    if not txt:
        return env
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key = line.split("=", 1)[0].strip()
            if key:
                env[key] = "***REDACTED***"
    return env

def env_and_config():
    # IMPORTANT: Never read .env (user’s private secrets). Only .env.example / templates.
    example = read_text([".env.example", ".env.template"])
    return {
        # Store only key names from example files, values redacted.
        "dotenv_example": example,
        "config": {
            "settings.py": read_text(["settings.py"]),
            "config.yaml": read_text(["config.yaml","config.yml"]),
            "application.yml": read_text(["application.yml"]),
        }
    }

def docs_and_meta():
    return {
        "README": read_text(["README.md","README.rst"]),
        "CHANGELOG": read_text(["CHANGELOG.md"]),
        "ROADMAP": read_text(["ROADMAP.md"]),
        "LICENSE": read_text(["LICENSE"]),
        "CODEOWNERS": read_text([".github/CODEOWNERS","CODEOWNERS"]),
        "CONTRIBUTING": read_text(["CONTRIBUTING.md"]),
        "SECURITY": read_text(["SECURITY.md"]),
        "ADR": [p.read_text(encoding="utf-8", errors="replace")
                for p in sorted((ROOT/"docs").glob("adr/*.md"))] if (ROOT/"docs").exists() else [],
    }

def summarize_files(files):
    sample = []
    for f in files[:4000]:  # cap to keep file small
        digest = file_digest(f)
        sample.append({"path": f, "sha256_12": digest})
    return sample

def main():
    files = list_files()
    state = {
        "generated_at": datetime.now(UTC).isoformat(),
        "root": str(ROOT),
        "language_mix": detect_langs(files),
        "file_index": summarize_files(files),
        "git": git_meta(),
        "ci_workflows": ci_workflows(),
        "make_targets": parse_make_targets(),
        "env_and_config": env_and_config(),
        "package_manifests": grep_versions(),
        "tests": test_info(),
        "docs_meta": docs_and_meta(),
    }
    # Write JSON (machine)
    (ROOT/"repo_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    # Write MD (human)
    md = []
    md.append(f"# Repo State\n\n_Generated: {state['generated_at']}_\n")
    md.append("## Quick Facts\n")
    md.append("- Files indexed: **{}**".format(len(state["file_index"])))
    md.append("- Branch: **{}**".format(state["git"].get("current_branch")))
    md.append("- Latest commit:\n```\n{}\n```".format(state["git"].get("latest_commit") or "n/a"))
    md.append("\n## Language Mix")
    for item in state["language_mix"]:
        md.append(f"- `{item['ext']}`: {item['count']}")
    md.append("\n## Key Docs Present")
    for k,v in state["docs_meta"].items():
        if isinstance(v, str) and v:
            md.append(f"- {k}: ✅")
        elif isinstance(v, list) and v:
            md.append(f"- {k}: {len(v)} docs")
    md.append("\n## CI Workflows")
    if state["ci_workflows"]:
        for name in state["ci_workflows"]:
            md.append(f"- {name}")
    else:
        md.append("- (none)")
    mk = state["make_targets"]
    if mk:
        md.append("\n## Make Targets")
        md.append("```\n" + "\n".join(mk) + "\n```")
    stat = state["git"].get("status") or ""
    if stat.strip():
        md.append("\n## Git Status (porcelain)\n```\n"+stat+"\n```")
    rc = state["git"].get("recent_commits") or ""
    if rc.strip():
        md.append("\n## Recent Commits\n```\n"+rc+"\n```")
    pm = state["package_manifests"]
    if pm:
        md.append("\n## Package Manifests Found")
        for eco in pm:
            md.append(f"- **{eco}**: {', '.join(pm[eco].keys())}")
    env = state["env_and_config"]["dotenv_example"]
    if env:
        md.append("\n## .env / examples detected: ✅")
    (ROOT/"REPO_STATE.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Wrote repo_state.json and REPO_STATE.md")

if __name__ == "__main__":
    main()
