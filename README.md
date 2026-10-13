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
| vocal-gate | Vocal Gate | 1.0.5 | yes | official installer | GPL-3.0 |

Vocal Gate for Windows ships only as an Inno Setup 6.7 installer, which current
extraction tools cannot unpack. It is stored unmodified as
`plugins/vocal-gate/1.0.5/windows-x64/VocalGate_Windows_Installer.exe`. On
Windows, `vexy-speakup assets fetch` runs it silently (`/VERYSILENT
/SUPPRESSMSGBOXES /NORESTART /SP-`). It asks for administrator rights (UAC),
installs `C:\Program Files\Common Files\VST3\Vocal Gate.vst3` and the VC++
runtime, and is uninstalled from Windows Settings > Apps.

Not included: `dereverb-vst3` has no licence, so it cannot be redistributed.

## Source code (GPL-3.0)

`plugins/<id>/<version>/source/` holds the complete source for each binary:

- PodcastPlugins and master_me: the upstream `-src.tar.xz` release archives
  (DPF and submodules included).
- Noise Repellent 0.4.1 (commit 34c80ce): the tagged tree plus the sources its
  CMake build fetches, under `deps/`: JUCE 8.0.15, libspecbleach v0.4.1 and
  FreeType VER-2-13-2.
- Vocal Gate 1.0.5 (commit 7393d65): the tagged tree (including its vendored
  ONNX Runtime) plus JUCE 8.0.12 under `deps/`.

## Layout

```
manifest.json                                   # ids, versions, sha256, sizes
plugins/<id>/LICENSE
plugins/<id>/<version>/<macos|windows-x64>/<Bundle>.vst3.zip   # or a vendor installer .exe
plugins/<id>/<version>/source/<id>-<version>-src.tar.xz
tools/manifest.py                               # regenerate manifest.json
```

macOS bundles are universal, ad hoc signed, and load in pedalboard 0.9.26.

## Adding a release

1. Extract the `.vst3` bundle from the official release (`.dmg`/`.pkg`: mount or
   `pkgutil --expand-full`; Windows `.zip`: unzip). A Windows single-file `.vst3` DLL is zipped at the archive root.
2. `ditto -c -k --keepParent Bundle.vst3 plugins/<id>/<version>/<platform>/Bundle.vst3.zip`
3. Add the complete corresponding source under `source/`.
4. Add the project to `SOURCES` in `tools/manifest.py`, run it, commit.
5. In vexy-speakup, update `ASSETS_REVISION` and the copied `assets_manifest.json`.
