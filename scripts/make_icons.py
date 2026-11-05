#!/usr/bin/env python3
"""SafeBunk launcher icons — seedha Android res folders me icons likhta hai.

Usage: python3 scripts/make_icons.py <res_dir> [logo_png]
Capacitor ke default template ke mipmap PNGs ko overwrite karta hai,
isliye koi external tool (capacitor-assets/sharp) fail ho to bhi
APK me app ka apna logo-icon hi lagega.
"""
import sys, os
from PIL import Image, ImageDraw

res_dir = sys.argv[1] if len(sys.argv) > 1 else "android/app/src/main/res"
logo_path = sys.argv[2] if len(sys.argv) > 2 else "assets/logo.png"

logo = Image.open(logo_path).convert("RGBA")
DENS = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}

def save(img, folder, name):
    d = os.path.join(res_dir, folder)
    os.makedirs(d, exist_ok=True)
    img.save(os.path.join(d, name), "PNG")
    print("wrote", os.path.join(d, name), img.size)

for dens, scale in DENS.items():
    folder = f"mipmap-{dens}"
    # Legacy launcher icon 48dp
    s = int(48 * scale)
    icon = logo.resize((s, s), Image.LANCZOS)
    save(icon, folder, "ic_launcher.png")
    # Round icon: gol mask
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s, s), fill=255)
    rnd = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    rnd.paste(icon, (0, 0), mask)
    save(rnd, folder, "ic_launcher_round.png")
    # Adaptive foreground 108dp — logo full-bleed (uska apna black bg hai)
    f = int(108 * scale)
    save(logo.resize((f, f), Image.LANCZOS), folder, "ic_launcher_foreground.png")

print("ICONS DONE ->", res_dir)
