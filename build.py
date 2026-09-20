"""Build the static site into dist/ for S3 + CloudFront (or any static host).

Copies web/ as-is (plain ES modules, no bundler), writes config.js from the environment or .env,
optionally includes the SQLite database, and records the build in dist/version.json.

Usage:
  GOOGLE_MAP_API_KEY=... python3 build.py [--out dist] [--no-db]

The key is read from the environment first, then from .env, so CI can inject it as a secret.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
DB = ROOT / "db"
SKIP = {"config.js",               # generated per environment, never copied
        "config.example.js",
        "data/karucapatoxic.json"}  # raw scraper output, not read by the pages


def read_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$", line)
        if m and not line.lstrip().startswith("#"):
            env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def maps_config() -> dict[str, str]:
    env = {**read_env(ROOT / ".env"), **{k: v for k, v in os.environ.items() if v}}
    key = env.get("GOOGLE_MAP_API_KEY")
    if not key:
        raise SystemExit("GOOGLE_MAP_API_KEY is not set (environment or .env) — the map cannot load without it")
    return {"googleMapsApiKey": key, "googleMapId": env.get("GOOGLE_MAP_ID") or "DEMO_MAP_ID"}


def copy_web(out: Path) -> int:
    files = 0
    for src in WEB.rglob("*"):
        rel = src.relative_to(WEB).as_posix()
        if src.is_dir() or rel in SKIP or src.name in SKIP or src.name == ".DS_Store":
            continue
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        files += 1
    return files


def copy_db(out: Path) -> int:
    files = 0
    for name in ("armenia-new-builds.sqlite", "db.md"):
        src = DB / name
        if src.exists():
            (out / "db").mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, out / "db" / name)
            files += 1
    return files


def git_commit() -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def write_version(out: Path) -> dict:
    dataset = json.loads((WEB / "data" / "projects.json").read_text())["meta"]
    info = {
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": git_commit(),
        "data_generated": dataset.get("generated"),
        "projects": dataset.get("count"),
    }
    (out / "version.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    return info


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=ROOT / "dist")
    ap.add_argument("--no-db", action="store_true", help="skip the SQLite database download")
    args = ap.parse_args()

    config = maps_config()
    out = args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    files = copy_web(out)
    (out / "config.js").write_text(f"window.APP_CONFIG = {json.dumps(config)};\n", encoding="utf-8")
    files += 1
    if not args.no_db:
        files += copy_db(out)
    info = write_version(out)

    size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
    print(f"{out} — {files} files, {size / 1e6:.1f} MB")
    print(f"  data {info['data_generated']} · {info['projects']} projects · commit {info['commit'] or 'n/a'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
