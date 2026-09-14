"""Write web/config.js (git-ignored) from .env so the browser app gets the Google Maps key without committing it."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$", line)
        if m and not line.lstrip().startswith("#"):
            env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def main() -> int:
    env_file = ROOT / ".env"
    if not env_file.exists():
        print(".env not found", file=sys.stderr)
        return 1
    env = read_env(env_file)
    key = env.get("GOOGLE_MAP_API_KEY")
    if not key:
        print("GOOGLE_MAP_API_KEY missing in .env", file=sys.stderr)
        return 1
    config = {"googleMapsApiKey": key, "googleMapId": env.get("GOOGLE_MAP_ID") or "DEMO_MAP_ID"}
    (ROOT / "web" / "config.js").write_text(f"window.APP_CONFIG = {json.dumps(config)};\n", encoding="utf-8")
    print("wrote web/config.js", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
