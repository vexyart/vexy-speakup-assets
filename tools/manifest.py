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

# Vendor installers kept verbatim when no plain bundle can be extracted. The package
# runs them silently on the user's machine; `installs_to` is where the bundle lands.
INSTALLERS = {
    "VocalGate_Windows_Installer.exe": {
        "bundle": "Vocal Gate.vst3",
        "installer": "inno",
        "args": ["/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-"],
        "installs_to": "common-vst3",
    },
}


def main() -> None:
    plugins = []
    for ident, (name, licence, source, tag) in SOURCES.items():
        files: dict[str, list[dict]] = {}
        folder = ROOT / "plugins" / ident
        archives = sorted([*folder.glob("*/*/*.zip"), *folder.glob("*/*/*.exe")])
        for archive in archives:
            data = archive.read_bytes()
            extra = INSTALLERS.get(archive.name, {})
            files.setdefault(archive.parent.name, []).append(
                {
                    "path": archive.relative_to(ROOT).as_posix(),
                    "bundle": archive.name.removesuffix(".zip"),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                    **extra,
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
