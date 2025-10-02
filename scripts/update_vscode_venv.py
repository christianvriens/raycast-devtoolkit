#!/usr/bin/env python3
"""
Update VS Code workspace settings to point to the project's python-tools virtualenv.

Usage: python3 scripts/update_vscode_venv.py

This script will:
 - verify python-tools/.venv exists
 - query the venv for sys.executable and site-packages path
 - update (or create) .vscode/settings.json with the interpreter path and
   add the site-packages path and ${workspaceFolder}/python-tools to
   python.analysis.extraPaths so Pylance can resolve installed packages.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PY = ROOT / "python-tools" / ".venv" / "bin" / "python"
VSCODE_SETTINGS = ROOT / ".vscode" / "settings.json"


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def get_venv_info(venv_python: Path):
    if not venv_python.exists():
        fail(f"Virtualenv python not found at {venv_python}. Create it first (./python-tools/run.sh)")

    cmd = [str(venv_python), "-c", (
        'import sys, json, sysconfig; ' 
        'p=sysconfig.get_paths().get("purelib") or sys.prefix; ' 
        'print(json.dumps({"exe":sys.executable, "site": p}))'
    )]

    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        fail(f"Failed to query venv python: {e.output}")

    try:
        info = json.loads(out.strip())
    except Exception as e:
        fail(f"Invalid json from venv python: {e}\nOutput:\n{out}")

    return info


def load_settings(path: Path):
    if not path.exists():
        return {}
    try:
        # settings.json may contain comments (jsonc). Attempt a tolerant load.
        txt = path.read_text(encoding="utf8")
        # strip simple C-style comments (very small heuristic)
        import re
        txt_no_comments = re.sub(r"(?m)^\s*//.*\n?", "", txt)
        return json.loads(txt_no_comments)
    except Exception:
        # fall back to empty
        return {}


def write_settings(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf8")


def main():
    info = get_venv_info(VENV_PY)
    exe = info.get("exe")
    site = info.get("site")

    if not exe or not site:
        fail("Could not determine venv interpreter or site-packages path")

    print(f"Detected venv python: {exe}")
    print(f"Detected site-packages: {site}")

    settings = load_settings(VSCODE_SETTINGS)

    # set interpreter
    settings["python.defaultInterpreterPath"] = exe
    settings["python.pythonPath"] = exe
    settings["python.terminal.activateEnvironment"] = True

    # extraPaths: include workspace python-tools and the absolute site-packages
    extra = settings.get("python.analysis.extraPaths") or []
    workspace_tools = "${workspaceFolder}/python-tools"
    if workspace_tools not in extra:
        extra.append(workspace_tools)

    if site not in extra:
        extra.append(site)

    settings["python.analysis.extraPaths"] = extra

    # keep pytest config
    if "python.testing.pytestEnabled" not in settings:
        settings["python.testing.pytestEnabled"] = True
    if "python.testing.pytestArgs" not in settings:
        settings["python.testing.pytestArgs"] = ["python-tools/tests"]

    write_settings(VSCODE_SETTINGS, settings)
    print(f"Wrote {VSCODE_SETTINGS}")


if __name__ == "__main__":
    main()
