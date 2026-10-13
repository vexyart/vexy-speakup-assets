#!/usr/bin/env python3
# this_file: tools/manifest.py
"""Regenerate manifest.json from plugins/<id>/<version>/<platform>/<bundle>.zip."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "podcast-plugins": ("PodcastPlugins", "GPL-3.0", "https://github.com/trummerschlunk/PodcastPlugins", "1.0.0"),
    "master_me": ("master_me", "GPL-3.0", "https://github.com/trummerschlunk/master_me", "1.3.1"),
    "noise-repellent": ("Noise Repellent", "GPL-3.0", "https://github.com/lucianodato/noise-repellent", "v0.4.1"),
    "vocal-gate": ("Vocal Gate", "GPL-3.0", "https://github.com/dan-k-k/vocal-gate", "v1.0.5"),
}


def main() -> None:
    plugins = []
    for ident, (name, licence, source, tag) in SOURCES.items():
        files: dict[str, list[dict]] = {}
        for archive in sorted((ROOT / "plugins" / ident).glob("*/*/*.zip")):
            data = archive.read_bytes()
            files.setdefault(archive.parent.name, []).append(
                {
                    "path": archive.relative_to(ROOT).as_posix(),
                    "bundle": archive.name.removesuffix(".zip"),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                }
            )
        version = {a["path"].split("/")[2] for p in files.values() for a in p}.pop()
        plugins.append(
            {
                "id": ident,
                "name": name,
                "version": version,
                "license": licence,
                "license_file": f"plugins/{ident}/LICENSE",
                "source": source,
                "release": f"{source}/releases/tag/{tag}",
                "files": files,
            }
        )
    manifest = {"schema_version": 1, "plugins": plugins}
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
