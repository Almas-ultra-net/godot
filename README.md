# Light & Shadow

> A 2D stealth-puzzle platformer built with **Godot 4**. Seen in the light,
> invisible in shadow. Move light sources, or wait for drifting clouds, to sneak
> past the guards.

![Genre: Stealth-Puzzle Platformer](https://img.shields.io/badge/genre-stealth--puzzle-1b2a4a)
![Engine: Godot 4.4](https://img.shields.io/badge/engine-Godot%204.4-478cbf)
![Language: GDScript](https://img.shields.io/badge/language-GDScript-cccc00)
![Target: Web](https://img.shields.io/badge/target-Web-e34f26)

## The core mechanic

You are a **shadow-keeper**. The game world is dark; light sources here are
both your friend and your danger.

- **In light** → guards see you and chase you.
- **In shadow** → you are invisible to guards.
- Move or toggle lights with levers, and hide under a **drifting cloud's
  shadow** to cross dangerous light pools.

## Controls

| Action             | Keys                     |
|--------------------|--------------------------|
| Move left / right  | `A` / `D` or Arrow keys  |
| Jump               | `Space`                  |
| Drop through       | `Down` + `Space`         |
| Interact (lever)   | `E`                      |
| Pause / Quit menu  | `Esc`                    |

## Running the game

1. Download and open **Godot 4.4**: https://godotengine.org/
2. Choose **Import**, then select the `project.godot` in this folder.
3. Press **F5** (or the ▶ Run button) to play.

> Sprites/pixel filters & input map are configured in `project.godot` and the
> autoloads. The game starts at the title screen.

## Project structure

```
project.godot            Configuration (main scene, rendering, filter, autoloads)
icon.svg                 Project icon
export_presets.cfg       Web (HTML5) export preset

scenes/
  main_menu.tscn         Title screen (start / quit)
  main.tscn              Level 1
  level_02.tscn          Level 2 (additional content)
  player.tscn            The shadow-keeper hero
  enemy_guard.tscn       A patrolling lantern-guard
  campfire.tscn          Static light source
  lantern.tscn           Movable / toggleable light
  cloud.tscn             Drifting cloud that casts a moving shadow
  stone_pillar.tscn      Obstacle that blocks light (real shadow)
  switch_lever.tscn      Toggles a nearby light on/off
  goal_door.tscn         Level exit
  light_crystal.tscn     Collectible score shards

scripts/
  input_config.gd        Autoload: registers input actions in code
  game_manager.gd        Autoload: score, caught/win flow, level management
  player.gd              Movement, jump, drop-through, coyote time, lit check
  enemy.gd               Patrol + FOV cone + chase
  light_source.gd        Base light (PointLight2D + light_zone Area2D)
  campfire.gd            Fixed campfire
  lantern.gd             Movable lantern
  cloud.gd               Drifting cloud + moving shadow zone
  switch_lever.gd        Interactable lever (toggles light, sounds)
  goal_door.gd           Level exit (chime)
  light_crystal.gd       Collectible (bob, pickup sound)
  hud.gd                 Score, timer, status
  stone_pillar.gd        Light occluder
  main_menu.gd           Title menu logic

assets/
  sprites/               Pixel-art sprites (transparent, optimized)
    sprites.json         Generated sprite metadata (sizes for scene generator)
    _gallery.png         Reference sheet
  audio/                 Generated sound effects (wav)

scripts_tools/
  remove_bg.py           Removes navy backgrounds from sprites
  optimize_assets.py     Crops + downscales sprites, writes sprites.json
  gen_scenes.py          Regenerates object scenes from sprites.json
  gen_main.py            Regenerates the main level scene
  gen_audio.py           Regenerates the sound effects (wav)
  validate_project.py    Sanity checks (pre-commit / CI)

CI / other
  .github/workflows/validate.yml   GitHub Actions lint + resource validation
  CHANGELOG.md                     Release notes
  CONTRIBUTING.md                  Contributor guide
```

## Feature checklist

**Movement / feel**
- [x] Left / right movement
- [x] Jump with coyote time + jump buffering
- [x] Drop-through one-way platforms
- [x] Squash & stretch on landing

**Light / shadow mechanic (core)**
- [x] Light zones (`light_zone` group + `PointLight2D`)
- [x] Shadow zones (`shadow_zone` group, from clouds)
- [x] `is_lit` = in light AND not in shadow
- [x] Guards only detect lit players

**Enemies**
- [x] Patrol between bounds
- [x] FOV cone detection (direction + range)
- [x] Chase & catch → restart level

**Puzzle / interactions**
- [x] Levers toggle nearest light (with sound + animation)
- [x] Drifting cloud shadow
- [x] Collectible crystals (score + pickup sound)
- [x] Goal door → next level
- [x] Fire flicker on lights

**Presentation / audio**
- [x] HUD (score, timer, status)
- [x] Title screen menu
- [x] 6 generated sound effects
- [x] Optimized Web-ready assets

## Exporting to Web (HTML5)

1. Install Godot 4.4 export templates (Editor → Manage Export Templates).
2. Open **Project → Export**, select the **Web** preset, click **Export Project**.
3. Serve `build/` (e.g. `python3 -m http.server`) and open in a browser.

## Dev tools & regenerating scenes

Asset *generation* is reproducible via the Python helpers:

```bash
python3 -m venv .venv && .venv/bin/pip install pillow numpy gdtoolkit
.venv/bin/python3 scripts_tools/remove_bg.py assets/sprites   # once (if sprites have bg)
.venv/bin/python3 scripts_tools/optimize_assets.py
.venv/bin/python3 scripts_tools/gen_scenes.py
.venv/bin/python3 scripts_tools/gen_main.py
.venv/bin/python3 scripts_tools/gen_audio.py
.venv/bin/python3 scripts_tools/validate_project.py
```

## License

See [LICENSE](LICENSE). (GPL-3.0)
