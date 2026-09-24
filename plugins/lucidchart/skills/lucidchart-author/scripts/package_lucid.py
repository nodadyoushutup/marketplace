#!/usr/bin/env python3
"""Package a Lucid Standard Import *.lucid.json into a .lucid zip."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path


def package(src: Path, dest: Path) -> None:
    data = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{src}: root must be a JSON object")
    data.pop("__layoutContract__", None)
    if "version" not in data:
        raise SystemExit(f"{src}: missing required 'version'")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        raise SystemExit(f"{src}: 'pages' must be a non-empty array")
    for page in pages:
        if not isinstance(page, dict) or "id" not in page:
            raise SystemExit(f"{src}: each page needs an 'id'")
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("document.json", payload)
    print(f"wrote {dest} ({len(payload)} bytes document.json)")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("src", type=Path, help="path to *.lucid.json")
    p.add_argument(
        "dest",
        type=Path,
        nargs="?",
        help="output .lucid path (default: src with .lucid suffix)",
    )
    args = p.parse_args()
    src = args.src
    if not src.is_file():
        raise SystemExit(f"not a file: {src}")
    dest = args.dest
    if dest is None:
        dest = src.with_suffix("").with_suffix(".lucid")
        if src.name.endswith(".lucid.json"):
            dest = Path(str(src)[: -len(".lucid.json")] + ".lucid")
    package(src, dest)


if __name__ == "__main__":
    main()
