#!/usr/bin/env python3
"""Run project sanity checks. Use as a pre-commit / CI gate.
  python3 scripts_tools/validate_project.py
"""
import os, re, glob, subprocess

issues = []

def check(cond, msg):
    if not cond:
        issues.append(msg)

# 1. project.godot
g = open("project.godot").read()
check("config/name=" in g, "project.godot: no config/name")
check("main_scene" in g, "project.godot: no main_scene")
for m in re.findall(r"\*res://(scripts/[^\"]+\.gd)", g):
    check(os.path.exists(m), f"autoload missing {m}")

# 2. scene resource refs exist
for f in glob.glob("scenes/*.tscn"):
    txt = open(f).read()
    for p in re.findall(r"res://([^\"]+)", txt):
        check(os.path.exists(p), f"{f}: missing {p}")

# 3. sprite & audio refs exist
for f in glob.glob("scripts/*.gd") + glob.glob("scenes/*.tscn"):
    txt = open(f).read()
    for p in re.findall(r"res://(assets/[^\"]+\.(?:png|wav|json))", txt):
        check(os.path.exists(p), f"{f}: missing asset {p}")

# 4. lint scripts
try:
    r = subprocess.run([".venv/bin/gdlint"] + glob.glob("scripts/*.gd"),
                       capture_output=True, text=True)
    if r.returncode != 0:
        issues.append("gdlint failures:\n" + r.stdout)
except FileNotFoundError:
    print("gdlint not found; install gdtoolkit (.venv/bin/pip install gdtoolkit)")

# 5. required dirs/file inventory
required = [
    "project.godot", "icon.svg", "README.md", "LICENSE",
    "scenes/main_menu.tscn", "scenes/main.tscn",
    "scripts/player.gd", "scripts/enemy.gd", "scripts/light_source.gd",
    "scripts/game_manager.gd", "scripts/input_config.gd", "scripts/hud.gd",
    "assets/sprites/light_mask.png", "assets/sprites/sprites.json",
]
for rq in required:
    check(os.path.exists(rq), f"required file missing: {rq}")

print("=== PROBLEMS ===" if issues else "=== ALL CHECKS PASSED ===")
for i in issues:
    print(" -", i)
print()
print("scenes:", len(glob.glob("scenes/*.tscn")),
      "| scripts:", len(glob.glob("scripts/*.gd")),
      "| sprites:", len(glob.glob("assets/sprites/*.png")),
      "| audio:", len(glob.glob("assets/audio/*.wav")))
raise SystemExit(1 if issues else 0)
