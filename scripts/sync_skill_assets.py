#!/usr/bin/env python3
"""Export the canonical repository protocol into the standalone init skill."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "skills/mukidoc-init/assets"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check the bundle without modifying it")
    args = parser.parse_args()
    manifest_path = ASSETS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    data = (ROOT / "AGENTS.md").read_bytes()
    versions = re.findall(rb"<!-- MukiDoc protocol version: (\d+\.\d+\.\d+) -->", data)
    if len(versions) != 1:
        raise ValueError("Canonical AGENTS.md must have exactly one protocol version marker")
    version = versions[0].decode()
    current = ASSETS / "template/AGENTS.md"
    if not args.check and current.exists() and current.read_bytes() != data:
        before = tuple(map(int, manifest["protocol_version"].split(".")))
        after = tuple(map(int, version.split(".")))
        if after <= before:
            raise ValueError("Bump the protocol version before exporting changed protocol content")
    expected = dict(manifest)
    expected["protocol_version"] = version
    expected["files"] = dict(manifest["files"])
    for name in manifest["files"]:
        content = data if name == "AGENTS.md" else (ASSETS / "template" / name).read_bytes()
        expected["files"][name] = hashlib.sha256(content).hexdigest()
    if args.check:
        if not current.exists() or current.read_bytes() != data or expected != manifest:
            raise ValueError("Skill assets are stale; export and review the changed bundle")
        print("Canonical protocol and all bundled file checksums match.")
    else:
        current.write_bytes(data)
        manifest_path.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Exported MukiDoc protocol " + version)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
