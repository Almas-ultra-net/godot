#!/usr/bin/env python3
"""Generate the main level scene (scenes/main.tscn).
The level is built from platform tiles (48x48) forming the ground, a raised
platform, a one-way platform, and all the game objects placed in a sensible
layout. Run from repo root.
"""
import os, json

SCENES = "scenes"
meta = json.load(open("assets/sprites/sprites.json"))

def header(n_ext, n_sub):
    return f"[gd_scene load_steps={n_ext + n_sub + 1} format=3]\n"

ext_res = [
    ("1", "Script", "res://scripts/hud.gd"),
    ("2", "PackedScene", "res://scenes/player.tscn"),
    ("3", "PackedScene", "res://scenes/enemy_guard.tscn"),
    ("4", "PackedScene", "res://scenes/campfire.tscn"),
    ("5", "PackedScene", "res://scenes/lantern.tscn"),
    ("6", "PackedScene", "res://scenes/cloud.tscn"),
    ("7", "PackedScene", "res://scenes/stone_pillar.tscn"),
    ("8", "PackedScene", "res://scenes/switch_lever.tscn"),
    ("9", "PackedScene", "res://scenes/goal_door.tscn"),
    ("10", "PackedScene", "res://scenes/light_crystal.tscn"),
    ("11", "Texture2D", "res://assets/sprites/platform_tile_sq.png"),
]

sub_res = [
    ("RectangleShape2D_floor", "RectangleShape2D", [("size", "Vector2(48, 48)")]),
    ("RectangleShape2D_oneway", "RectangleShape2D", [("size", "Vector2(48, 16)")]),
]

def build_text():
    t = header(len(ext_res), len(sub_res))
    for id_, typ, p in ext_res:
        t += f'[ext_resource type="{typ}" path="{p}" id="{id_}"]\n'
    for id_, typ, props in sub_res:
        t += f'[sub_resource type="{typ}" id="{id_}"]\n'
        for k, v in props:
            t += f"{k} = {v}\n"

    t += '[node name="Main" type="Node2D"]\n'
    t += '[node name="Environment" type="CanvasModulate" parent="."]\n'
    t += 'color = Color(0.42, 0.46, 0.58)\n'
    t += '[node name="HUD" type="CanvasLayer" parent="."]\n'
    t += 'script = ExtResource("1")\n'
    t += '[node name="ScoreLabel" type="Label" parent="HUD"]\n'
    t += 'offset_left = 16.0\noffset_top = 12.0\noffset_right = 360.0\noffset_bottom = 46.0\n'
    t += 'text = "Light Shards: 0"\n'
    t += 'theme_override_colors/font_color = Color(1, 1, 1, 1)\n'
    t += 'theme_override_font_sizes/font_size = 20\n'
    t += '[node name="TimerLabel" type="Label" parent="HUD"]\n'
    t += 'offset_left = 1000.0\noffset_top = 12.0\noffset_right = 1264.0\noffset_bottom = 46.0\n'
    t += 'text = "Time: 00:00"\n'
    t += 'horizontal_alignment = 2\n'
    t += 'theme_override_colors/font_color = Color(1, 1, 1, 1)\n'
    t += 'theme_override_font_sizes/font_size = 20\n'
    t += '[node name="HintLabel" type="Label" parent="HUD"]\n'
    t += 'offset_left = 16.0\noffset_top = 48.0\noffset_right = 1264.0\noffset_bottom = 74.0\n'
    t += 'text = "A/D move   Space jump   Down+Space drop   E interact"\n'
    t += 'theme_override_colors/font_color = Color(1, 1, 1, 0.8)\n'
    t += 'theme_override_font_sizes/font_size = 15\n'
    t += '[node name="StatusLabel" type="Label" parent="HUD"]\n'
    t += 'offset_left = 360.0\noffset_top = 300.0\noffset_right = 920.0\noffset_bottom = 340.0\n'
    t += 'text = ""\n'
    t += 'horizontal_alignment = 1\n'
    t += 'theme_override_colors/font_color = Color(1, 0.85, 0.3, 1)\n'
    t += 'theme_override_font_sizes/font_size = 28\n'

    # ground floor
    for i in range(0, 30):
        cx = 24 + i * 48
        t += block(cx, 24, "Floor%d" % i, "RectangleShape2D_floor")

    # raised platform (jump reachable)
    for j, cx in enumerate([480, 528, 576, 624, 672]):
        t += block(cx, -96, "PlatA%d" % j, "RectangleShape2D_floor")

    # upper platform near goal
    for k, cx in enumerate([1000, 1048, 1096, 1144]):
        t += block(cx, -160, "PlatB%d" % k, "RectangleShape2D_floor")

    # one-way platforms
    for m, (cx, cy) in enumerate([(700, -180), (860, -240)]):
        t += oneway(cx, cy, "OneWay%d" % m)

    # objects
    t += inst("Player", "2", (120, -60))
    t += inst("EnemyGuard", "3", (560, -50))
    t += inst("Campfire", "4", (1160, -20))
    t += inst("Lantern", "5", (760, -40))
    t += inst("SwitchLever", "8", (720, 0))
    t += inst("StonePillar", "7", (940, 0))
    t += inst("Cloud", "6", (400, -260))
    t += inst("GoalDoor", "9", (1240, 0))
    t += inst("LightCrystal1", "10", (300, -30))
    t += inst("LightCrystal2", "10", (1080, -170))
    t += inst("LightCrystal3", "10", (760, -120))
    return t

def block(cx, cy, name, subshape, sc="1.0, 1.0"):
    s = f'[node name="{name}" type="StaticBody2D" parent="."]\n'
    s += f'position = Vector2({cx}, {cy})\n'
    s += 'collision_layer = 1\n'
    s += 'collision_mask = 0\n'
    s += f'[node name="Sprite2D" type="Sprite2D" parent="{name}"]\n'
    s += 'texture = ExtResource("11")\n'
    s += f'scale = Vector2({sc})\n'
    s += f'[node name="CollisionShape2D" type="CollisionShape2D" parent="{name}"]\n'
    s += f'shape = SubResource("{subshape}")\n'
    return s

def oneway(cx, cy, name):
    s = f'[node name="{name}" type="StaticBody2D" parent="."]\n'
    s += f'position = Vector2({cx}, {cy})\n'
    s += 'collision_layer = 4\n'
    s += 'collision_mask = 0\n'
    s += f'[node name="Sprite2D" type="Sprite2D" parent="{name}"]\n'
    s += 'texture = ExtResource("11")\n'
    s += 'scale = Vector2(1.0, 0.333)\n'
    s += f'[node name="CollisionShape2D" type="CollisionShape2D" parent="{name}"]\n'
    s += 'shape = SubResource("RectangleShape2D_oneway")\n'
    s += 'one_way_collision = true\n'
    return s

def inst(name, ext_id, pos):
    s = f'[node name="{name}" parent="." instance=ExtResource("{ext_id}")]\n'
    s += f'position = Vector2({pos[0]}, {pos[1]})\n'
    return s

os.makedirs(SCENES, exist_ok=True)
with open(os.path.join(SCENES, "main.tscn"), "w") as f:
    f.write(build_text())
print("wrote scenes/main.tscn")
