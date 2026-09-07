# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Title screen menu (`main_menu.tscn`) with Start / Quit.
- A second level (`level_02.tscn`) demonstrating a working light/cloud puzzle.
- HUD: score, timer, and a status/announcement line.
- Six generated sound effects under `assets/audio/`.
- Fire-flicker on light sources.
- Guard FOV cone detection (directional sight, in addition to range).
- Player "juice": coyote time, jump buffering, landing squash.
- Helper tools: background remover, sprite optimizer, scene generators.
- `CHANGELOG.md` and `CONTRIBUTING.md`.

### Changed
- Refactored all object scenes to use exact sprite-derived scales and correct
  bottom-center pivots (no more hard-coded magic scales).
- Sprites optimized: cropped transparent padding + downscaled for a Web build
  (assets went from ~10 MB to ~330 KB).
- `project.godot` now boots into the title screen; a Web export preset is
  included.

### Fixed
- GDScript style/lint issues (gdlint clean).
- Removed unused oversized tile asset.

## [0.1.0] - 2026-09-07
### Added
- Initial Godot 4 project skeleton with the core light/shadow mechanic.
- Player movement (left/right, jump, drop-through), patrol enemy with chase,
  light sources, cloud shadow, levers, collectibles, goal door.
- Pixel-art sprites with transparent backgrounds (backgrounds removed).
