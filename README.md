<!-- this_file: README.md -->
# vexy-speakup-assets

Large deliverables for [vexy-speakup](https://github.com/vexyart/vexy-speakup),
stored with Git LFS and downloaded by the package on demand. Install the package,
then run `vexy-speakup assets fetch`, or let a chain that needs a bundled plugin
fetch it the first time.

## Free plugins

Unmodified VST3 bundles taken from each project's official release, re-zipped per
platform. Each project's licence is in `plugins/<id>/LICENSE`; source code is at
the linked repository and release.

| id | Plugin | Version | macOS | Windows x64 | Licence |
| --- | --- | --- | --- | --- | --- |
| podcast-plugins | PodcastPlugins TRACK, MASTER | 1.0.0 | yes | yes | GPL-3.0 |
| master_me | master_me | 1.3.1 | yes | yes | GPL-3.0 |
| noise-repellent | Noise Repellent | 0.4.1 | yes | yes | GPL-3.0 |
| vocal-gate | Vocal Gate | 1.0.5 | yes | no (Inno Setup 6.7 installer only) | GPL-3.0 |

Not included: `dereverb-vst3` has no licence, so it cannot be redistributed.

## Layout

```
manifest.json                                   # ids, versions, sha256, sizes
plugins/<id>/LICENSE
plugins/<id>/<version>/<macos|windows-x64>/<Bundle>.vst3.zip
tools/manifest.py                               # regenerate manifest.json
```

macOS bundles are universal, ad hoc signed, and load in pedalboard 0.9.26.

## Adding a release

1. Extract the `.vst3` bundle from the official release (`.dmg`/`.pkg`: mount or
   `pkgutil --expand-full`; Windows `.zip`: unzip).
2. `ditto -c -k --keepParent Bundle.vst3 plugins/<id>/<version>/<platform>/Bundle.vst3.zip`
3. Add the project to `SOURCES` in `tools/manifest.py`, run it, commit.
4. In vexy-speakup, update `ASSETS_REVISION` and the copied `assets_manifest.json`.
