# Contributing

Thanks for your interest in **Light & Shadow**! This document outlines how to
work with the codebase.

## Getting started

1. Install **Godot 4.4** (the project targets `4.4`, GL Compatibility renderer).
2. Clone and import `project.godot`.
3. Press **F5** to run from the title screen.

## Project layout

- `scenes/` — Godot scenes (`.tscn`). The *level* scenes (`main.tscn`,
  `level_02.tscn`) are mostly generated from the helper scripts.
- `scripts/` — GDScript. `input_config.gd` and `game_manager.gd` are autoloads.
- `assets/sprites/` — pixel-art PNGs. `sprites.json` holds generated metadata.
- `scripts_tools/` — Python helpers used to (re)create assets and scenes.

## Regenerating scenes & assets

Some files are generated. After editing sprite files or a generator, run:

```bash
python3 -m venv .venv && .venv/bin/pip install pillow numpy
.venv/bin/python3 scripts_tools/remove_bg.py assets/sprites   # once, if needed
.venv/bin/python3 scripts_tools/optimize_assets.py
.venv/bin/python3 scripts_tools/gen_scenes.py
.venv/bin/python3 scripts_tools/gen_main.py
```

> If you manually edit `main.tscn` / the object scenes, be aware they can be
> overwritten by these generators. Prefer editing `scripts_tools/*.py` and the
> per-object scenes, and regenerate where appropriate.

## Coding conventions

- GDScript, tabs for indentation, `snake_case` for functions/variables.
- `@export` for tunable values; keep behaviour in `scripts/`.
- Run the linter before committing: `.venv/bin/gdlint scripts/*.gd`
  (or `gdlint` if installed globally).

## Adding a new object

1. Drop a transparency-enabled PNG in `assets/sprites/`.
2. Add it to `TARGETS` in `scripts_tools/optimize_assets.py`.
3. Run `optimize_assets.py` to update `sprites.json`.
4. Add a scene entry in `scripts_tools/gen_scenes.py` (or a hand-written
   `.tscn`).
5. Add behaviour in `scripts/`, and instance it in a level.

## Testing

- Run the game in the editor; verify the light/shadow mechanic by standing in a
  lit area (a guard should chase) then hiding under a cloud's shadow (guard
  should stop).
- Confirm levers toggle lights and play a sound, and that crystals/doors work.

## License

By contributing you agree your contributions are licensed under
[GPL-3.0](LICENSE).
