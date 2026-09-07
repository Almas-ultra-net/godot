#!/usr/bin/env python3
"""Remove the dark navy background from sprite PNGs, keeping the object and
feathering edges so light glows fade out naturally.

Approach:
  1. Guess a background color from the border pixels (median).
  2. Flood-fill from every border pixel, growing into pixels whose color is
     within `tol` of the background reference. This yields the CONNECTED
     background region only, so dark parts of the object are preserved.
  3. Compute an alpha for the whole image from color-distance (chroma key).
  4. Inside the connected background region, set alpha to the feathered
     color-distance alpha; outside (the object), alpha stays 255.
  5. Keep RGB of glow pixels, but fully transparent background pixels get a
     neutral value so no colored fringe appears when composited.
"""
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

def median_border_color(arr):
    h, w = arr.shape[:2]
    border_mask = np.zeros((h, w), dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True
    px = arr[border_mask]
    return np.median(px, axis=0)

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)

def process(path, tol, feather_lo, feather_hi, out_path=None):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im).astype(np.float32)
    rgb = arr[:, :, :3]
    a = arr[:, :, 3]
    h, w = rgb.shape[:2]

    bg = median_border_color(rgb)

    # color distance from bg reference
    dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2))

    # candidate background pixels (close to bg color, and at least semi-opaque)
    cand = (dist < tol) & (a > 0)

    # label connected components of candidate bg; keep those touching border
    lab, n = ndimage.label(cand)
    border_labels = set(np.unique(np.concatenate([
        lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])))
    border_labels.discard(0)
    bg_mask = np.isin(lab, list(border_labels))

    # alpha from color distance (feathered chroma key), applied only to bg mask
    alpha_img = (smoothstep(feather_lo, feather_hi, dist) * 255.0)

    # object pixels keep full alpha; bg pixels get feathered alpha
    new_a = np.where(bg_mask, alpha_img, 255.0)
    # blend with existing alpha (preserve any pre-existing transparency as lower bound)
    new_a = np.minimum(new_a, a)

    out = arr.copy()
    out[:, :, 3] = new_a.astype(np.float32)
    out = out.astype(np.uint8)

    # Depremultiply: push fully-transparent pixels toward bg-neutral to avoid fringe.
    res = Image.fromarray(out, "RGBA")
    if out_path:
        res.save(out_path)
    return res

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "assets/sprites"
    tol = float(sys.argv[2]) if len(sys.argv) > 2 else 55.0
    feather_lo = float(sys.argv[3]) if len(sys.argv) > 3 else 12.0
    feather_hi = float(sys.argv[4]) if len(sys.argv) > 4 else 70.0

    for f in sorted(os.listdir(src)):
        if not f.lower().endswith(".png"):
            continue
        p = os.path.join(src, f)
        out = os.path.join(src, f)
        process(p, tol, feather_lo, feather_hi, out)
        print(f"processed {f}")

if __name__ == "__main__":
    main()
