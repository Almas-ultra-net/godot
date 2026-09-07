#!/usr/bin/env python3
"""Generate Godot .tscn object scenes with sprite sizes parsed from
assets/sprites/sprites.json so Sprite2D scales and offhand offsets are exact.
"""
import os, json

SCENES = "scenes"
meta = json.load(open("assets/sprites/sprites.json"))

def header(n_ext, n_sub):
    return f"[gd_scene load_steps={n_ext + n_sub + 1} format=3]\n"

def ext(id_, type_, path_):
    return f'[ext_resource type="{type_}" path="{path_}" id="{id_}"]\n'

def sub(id_, type_, props):
    s = f'[sub_resource type="{type_}" id="{id_}"]\n'
    for k, v in props:
        s += f"{k} = {v}\n"
    return s

def node(name, type_, parent=".", props=None, children=None):
    line = f'[node name="{name}" type="{type_}" parent="{parent}"]\n'
    if props:
        for k, v in props:
            line += f"{k} = {v}\n"
    s = line
    for c in children or []:
        s += c
    return s

def write_scene(path, text):
    os.makedirs(SCENES, exist_ok=True)
    with open(os.path.join(SCENES, path), "w") as f:
        f.write(text)
    print("wrote", os.path.join(SCENES, path))

# --- scale helper: render a sprite of metadata size to target world size ---
def sprite_scale(name, target_w, target_h):
    m = meta[name]
    return min(target_w / m["w"], target_h / m["h"])

# ------------------------------------------------------------------ player
tw, th = 30, 44
sc = sprite_scale("player.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/player.gd")
text += ext("2", "Texture2D", "res://assets/sprites/player.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(26, 44)")])
text += node("Player", "CharacterBody2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "1"),
    ("collision_mask", "13"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", "Vector2(0, -22)"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("Camera2D", "Camera2D", ".", props=[
    ("position_smoothing_enabled", "true"),
    ("position_smoothing_speed", "8.0"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", "Vector2(0, -22)"),
])
write_scene("player.tscn", text)

# ------------------------------------------------------------------ enemy_guard
tw, th = 34, 44
sc = sprite_scale("enemy_guard.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/enemy.gd")
text += ext("2", "Texture2D", "res://assets/sprites/enemy_guard.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(28, 44)")])
text += node("EnemyGuard", "CharacterBody2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "1"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", "Vector2(0, -22)"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", "Vector2(0, -22)"),
])
write_scene("enemy_guard.tscn", text)

# ------------------------------------------------------------------ campfire
tw, th = 40, 48
sc = sprite_scale("campfire.png", tw, th)
text = header(2, 0)
text += ext("1", "Script", "res://scripts/campfire.gd")
text += ext("2", "Texture2D", "res://assets/sprites/campfire.png")
text += node("Campfire", "Area2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "0"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
write_scene("campfire.tscn", text)

# ------------------------------------------------------------------ lantern
tw, th = 34, 42
sc = sprite_scale("light_lantern.png", tw, th)
text = header(2, 0)
text += ext("1", "Script", "res://scripts/lantern.gd")
text += ext("2", "Texture2D", "res://assets/sprites/light_lantern.png")
text += node("Lantern", "Area2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "0"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
write_scene("lantern.tscn", text)

# ------------------------------------------------------------------ cloud
tw, th = 220, 93
sc = sprite_scale("cloud.png", tw, th)
text = header(2, 0)
text += ext("1", "Script", "res://scripts/cloud.gd")
text += ext("2", "Texture2D", "res://assets/sprites/cloud.png")
text += node("Cloud", "Node2D", ".", props=[
    ("script", 'ExtResource("1")'),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", "Vector2(0, 0)"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
write_scene("cloud.tscn", text)

# ------------------------------------------------------------------ stone_pillar
tw, th = 40, 120
sc = sprite_scale("stone_pillar.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/stone_pillar.gd")
text += ext("2", "Texture2D", "res://assets/sprites/stone_pillar.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(40, 120)")])
text += node("StonePillar", "StaticBody2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "1"),
    ("collision_mask", "0"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
])
write_scene("stone_pillar.tscn", text)

# ------------------------------------------------------------------ switch_lever
tw, th = 30, 42
sc = sprite_scale("switch_lever.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/switch_lever.gd")
text += ext("2", "Texture2D", "res://assets/sprites/switch_lever.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(46, 60)")])
text += node("SwitchLever", "Area2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "0"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
])
write_scene("switch_lever.tscn", text)

# ------------------------------------------------------------------ goal_door
tw, th = 120, 118
sc = sprite_scale("goal_door.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/goal_door.gd")
text += ext("2", "Texture2D", "res://assets/sprites/goal_door.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(80, 130)")])
text += node("GoalDoor", "Area2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "0"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
])
write_scene("goal_door.tscn", text)

# ------------------------------------------------------------------ light_crystal
tw, th = 20, 20
sc = sprite_scale("light_crystal.png", tw, th)
text = header(2, 1)
text += ext("1", "Script", "res://scripts/light_crystal.gd")
text += ext("2", "Texture2D", "res://assets/sprites/light_crystal.png")
text += sub("RectangleShape2D_1", "RectangleShape2D", [("size", "Vector2(20, 22)")])
text += node("LightCrystal", "Area2D", ".", props=[
    ("script", 'ExtResource("1")'),
    ("collision_layer", "0"),
    ("collision_mask", "1"),
])
text += node("Sprite2D", "Sprite2D", ".", props=[
    ("texture", 'ExtResource("2")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
    ("scale", f"Vector2({sc:.4f}, {sc:.4f})"),
])
text += node("CollisionShape2D", "CollisionShape2D", ".", props=[
    ("shape", 'SubResource("RectangleShape2D_1")'),
    ("position", f"Vector2(0, {-th*0.5:.1f})"),
])
write_scene("light_crystal.tscn", text)

print("All object scenes generated (sprite-size aware).")
