#!/usr/bin/env python3
"""Optimize sprite assets for the Web build:
  1. Crop away transparent padding (shrinks dimensions + file size).
  2. Downscale to a sensible in-game resolution (pixel art preserved).
  3. Save as optimized PNG with reduced palette where possible.

Writes a metadata table (sprites.json) so the scene generator can compute
exact Sprite2D transforms (offset to bottom-center, scale=1).

Run from repo root:  python3 scripts_tools/optimize_assets.py
"""
import os, json
from PIL import Image

SPR = "assets/sprites"

# name -> target for the LARGER dimension (keeps aspect ratio)
# platform_tile is special-cased to a clean tile size.
# Target size for the *largest* dimension (max side) of each sprite.
TARGETS = {
    "player.png": 96,
    "enemy_guard.png": 96,
    "campfire.png": 96,
    "light_lantern.png": 84,
    "cloud.png": 220,
    "stone_pillar.png": 160,
    "switch_lever.png": 60,
    "goal_door.png": 176,
    "light_crystal.png": 48,
    "platform_tile_sq.png": 48,  # clean 48x48 tile for repeated flooring
}

def opaque_bbox(img, alpha_thresh=6):
    a = img.split()[-1]
    bbox = a.point(lambda p: 255 if p > alpha_thresh else 0).getbbox()
    return bbox

def main():
    meta = {}
    for name, target in TARGETS.items():
        path = os.path.join(SPR, name)
        im = Image.open(path).convert("RGBA")
        bbox = opaque_bbox(im)
        if bbox is None:
            print("skip (empty):", name)
            continue
        im = im.crop(bbox)  # crop padding
        w, h = im.size
        # Only downscale if larger than the target max side; never upscale,
        # and never re-blur already-optimized sprites (keeps pixel art crisp).
        if max(w, h) > target:
            scale = target / float(max(w, h))
            new_w = max(1, round(w * scale))
            new_h = max(1, round(h * scale))
            im = im.resize((new_w, new_h), Image.LANCZOS)
        else:
            new_w, new_h = w, h
        if name == "platform_tile_sq.png":
            new_w = new_h = 48
            if im.size != (48, 48):
                im = im.resize((48, 48), Image.LANCZOS)
        im.save(path)
        meta[name] = {
            "w": new_w, "h": new_h,
            "source_w": bbox[2] - bbox[0],
            "source_h": bbox[3] - bbox[1],
        }
        print(f"{name:20s} -> {new_w}x{new_h}  (was {w}x{h})")

    return meta

if __name__ == "__main__":
    meta = main()
    with open(os.path.join(SPR, "sprites.json"), "w") as f:
        f.write(json.dumps(meta, indent=2))
    print("wrote sprites.json")
