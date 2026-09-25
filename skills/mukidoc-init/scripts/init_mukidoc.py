#!/usr/bin/env python3
"""Create the bundled MukiDoc skeleton without generating project knowledge."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4


ASSETS = Path(__file__).resolve().parent.parent / "assets"
VERSION = re.compile(r"<!-- MukiDoc protocol version: (\d+\.\d+\.\d+) -->")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def protocol_version(data):
    matches = VERSION.findall(data.decode("utf-8", errors="replace"))
    return matches[0] if len(matches) == 1 else None


def version_tuple(value):
    return tuple(int(part) for part in value.split("."))


def safe_relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError("Invalid bundle path: " + value)
    if str(path) != value or str(path) == ".":
        raise ValueError("Non-canonical bundle path: " + value)
    return Path(*path.parts)


def load_bundle():
    manifest = json.loads((ASSETS / "manifest.json").read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported bundle manifest schema")
    for value in (manifest["skill_version"], manifest["protocol_version"]):
        if not re.fullmatch(r"\d+\.\d+\.\d+", value):
            raise ValueError("Bundle versions must use major.minor.patch")
    directories = manifest["directories"]
    files = manifest["files"]
    if len(set(directories)) != len(directories) or "AGENTS.md" not in files:
        raise ValueError("Invalid skeleton manifest")
    contents = {}
    for name in directories:
        safe_relative(name)
    for name, digest in files.items():
        relative = safe_relative(name)
        data = (ASSETS / "template" / relative).read_bytes()
        if sha256(data) != digest:
            raise ValueError("Bundle checksum mismatch: " + name)
        contents[name] = data
    if protocol_version(contents["AGENTS.md"]) != manifest["protocol_version"]:
        raise ValueError("Protocol marker and bundle version differ")
    for name in list(directories) + list(files):
        parent = PurePosixPath(name).parent
        if str(parent) != "." and str(parent) not in directories:
            raise ValueError("Skeleton parent directory is missing: " + str(parent))
    return manifest, contents


def check_path(root, relative, directory=False):
    """Reject conflicting path types before writing any skeleton files."""
    path = root
    parts = safe_relative(relative).parts
    for index, part in enumerate(parts):
        path = path / part
        if path.is_symlink():
            raise ValueError("Managed path is a symlink: " + str(path))
        if not path.exists():
            continue
        want_directory = index < len(parts) - 1 or directory
        if want_directory and not path.is_dir():
            raise ValueError("Expected a directory: " + str(path))
        if not want_directory and not path.is_file():
            raise ValueError("Expected a regular file: " + str(path))


def agent_state(target, template, bundled_version):
    if not target.exists():
        return {"state": "missing", "installed_version": None, "sha256": None}
    data = target.read_bytes()
    installed = protocol_version(data)
    if data == template:
        state = "current"
    elif installed is None:
        state = "unversioned"
    elif version_tuple(installed) < version_tuple(bundled_version):
        state = "older"
    elif version_tuple(installed) > version_tuple(bundled_version):
        state = "newer"
    else:
        state = "same_version_modified"
    return {"state": state, "installed_version": installed, "sha256": sha256(data)}


def replace_agent(target, data, expected_digest):
    original = target.read_bytes()
    if sha256(original) != expected_digest:
        raise ValueError("AGENTS.md changed since review; inspect it again before updating")
    backup = target.with_name(
        "AGENTS.md.bak." + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        + "." + uuid4().hex[:8]
    )
    mode = stat.S_IMODE(target.stat().st_mode)
    # Back up exact bytes before replacing; the backup is never overwritten.
    with backup.open("xb") as handle:
        handle.write(original)
    os.chmod(backup, mode)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".mukidoc-agent-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
        os.chmod(temporary, mode)
        if target.is_symlink() or sha256(target.read_bytes()) != expected_digest:
            raise ValueError("AGENTS.md changed during update; original backup has been retained")
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return backup.name


def initialize(args):
    manifest, contents = load_bundle()
    root = Path(args.target).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise ValueError("Target is not a directory: " + str(root))
    for parent in root.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError("Target parent is not a directory: " + str(parent))
    for name in manifest["directories"]:
        check_path(root, name, directory=True)
    for name in contents:
        check_path(root, name)

    agent = agent_state(root / "AGENTS.md", contents["AGENTS.md"], manifest["protocol_version"])
    state = agent["state"]
    replace = False
    if args.update_agent or args.replace_agent:
        if not args.expected_agent_sha256:
            raise ValueError("Replacement requires --expected-agent-sha256 from the reviewed report")
        if args.expected_agent_sha256 != agent["sha256"]:
            raise ValueError("AGENTS.md changed since review; inspect it again before updating")
        if state == "newer":
            raise ValueError("Refusing to downgrade a newer protocol")
        if args.update_agent and state != "older":
            raise ValueError("--update-agent is only for a recognized older protocol")
        if args.replace_agent and state not in ("unversioned", "same_version_modified"):
            raise ValueError("--replace-agent is only for unversioned or same-version modified files")
        replace = True
    elif args.expected_agent_sha256:
        raise ValueError("--expected-agent-sha256 requires a replacement option")

    missing_dirs = [name for name in manifest["directories"] if not (root / name).exists()]
    create = [name for name in contents if not (root / name).exists()]
    kept = [name for name in contents if (root / name).exists() and not (name == "AGENTS.md" and replace)]
    # Keeping empty base directories is useful even before the project runs git init.
    keep_files = []
    for name in manifest["directories"]:
        if any(other.startswith(name + "/") for other in manifest["directories"]):
            continue
        if any(other.startswith(name + "/") for other in contents):
            continue
        path = root / name
        if not path.exists() or not any(path.iterdir()):
            keep_files.append(name + "/.gitkeep")

    needs_confirmation = not replace and state in ("older", "unversioned", "same_version_modified")
    agent.update({
        "bundled_version": manifest["protocol_version"],
        "needs_confirmation": needs_confirmation,
        "action": "replace" if replace else "create" if state == "missing" else "keep",
        "backup": None,
    })
    report = {
        "status": "planned" if args.dry_run else "initialized",
        "target": str(root), "skill_version": manifest["skill_version"],
        "dry_run": args.dry_run, "directories_created": missing_dirs,
        "files_created": create + keep_files, "files_preserved": kept, "agent": agent,
    }
    if args.dry_run:
        return report

    root.mkdir(parents=True, exist_ok=True)
    for name in missing_dirs:
        (root / name).mkdir(parents=True, exist_ok=True)
    for name in create:
        with (root / name).open("xb") as handle:
            handle.write(contents[name])
    for name in keep_files:
        with (root / name).open("xb"):
            pass
    if replace:
        agent["backup"] = replace_agent(root / "AGENTS.md", contents["AGENTS.md"], args.expected_agent_sha256)
    if needs_confirmation:
        report["status"] = "initialized_agent_preserved"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Project directory to initialize")
    parser.add_argument("--dry-run", action="store_true", help="Describe changes without writing anything")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--update-agent", action="store_true", help="Apply an explicitly approved older-protocol update")
    group.add_argument("--replace-agent", action="store_true", help="Apply an explicitly approved unversioned/modified-file replacement")
    parser.add_argument("--expected-agent-sha256", help="Hash of the exact AGENTS.md reviewed before approval")
    args = parser.parse_args()
    try:
        result = initialize(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error),
                          "note": "No existing document is intentionally overwritten without an approved replacement. Inspect the target after an I/O failure; new skeleton files or a backup may already exist."}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
