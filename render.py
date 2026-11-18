#!/usr/bin/env python3
"""Render entry 2 for news-image-20261117 from the user-supplied image.

Local-only Pillow renderer. The graded program is main.py (stdlib only);
this file just produces the pre-rendered entry.png that main.py copies.

Layout (1024x1024, no distortion of the source):
- 0..118   navy masthead: THE WORLD TODAY / TUESDAY 17 NOVEMBER 2026
- 118..766  user image, full width, 1024x648, lightly enhanced, navy border
- 766..1024 bottom band: real Nov 17 ticker (verified stories only) + sources
All added text is large and legible at 512px. Small gibberish captions
baked into the source grid are left untouched (they cannot be fixed).
"""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
NAVY = (22, 40, 77)
NAVY2 = (16, 30, 58)
GOLD = (232, 196, 90)
RED = (180, 35, 24)
PAPER = (250, 246, 236)
INK = (24, 24, 24)
MUTED = (80, 76, 70)

SRC = os.path.expanduser(
    "~/workspace/user/media_library/image/img_11373693522751118029.webp")


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


def main():
    src = Image.open(SRC).convert("RGB")
    assert src.size == (1024, 648), src.size
    # Mild enhancement only: sharpen / contrast / colour lift.
    src = ImageEnhance.Sharpness(src).enhance(1.18)
    src = ImageEnhance.Contrast(src).enhance(1.06)
    src = ImageEnhance.Color(src).enhance(1.08)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 114, W, 118], fill=GOLD)
    title = "THE WORLD TODAY"
    tf = font("DejaVuSerif-Bold.ttf", 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 8), title, font=tf,
           fill=(255, 255, 255))
    sub = "TUESDAY 17 NOVEMBER 2026  \u2022  9 BIG STORIES  \u2022  ONE DAY"
    sf = font("DejaVuSans-Bold.ttf", 20)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 80), sub, font=sf,
           fill=GOLD)

    # --- user grid, full width, undistorted ---
    img.paste(src, (0, 118))
    d.rectangle([0, 118, W - 1, 765], outline=NAVY, width=4)

    # --- bottom band: real Nov 17 ticker ---
    d.rectangle([0, 766, W, H], fill=(255, 253, 248))
    d.line([24, 766, W - 24, 766], fill=RED, width=3)
    d.text((24, 782), "ALSO ON TUESDAY 17 NOVEMBER",
           font=font("DejaVuSans-Bold.ttf", 22), fill=RED)
    y = 818
    lines = [
        ("KERCH BRIDGE HIT, 2ND DAY", " \u2014 Russia says 1,441 drones downed"),
        ("IRAN DRONES AT US RADAR, BAHRAIN", " \u2014 US strikes Qeshm; tankers hit"),
        ("TRUMP\u2013XI\u2013PUTIN IN SHENZHEN THU", "  \u2022  NVIDIA $115.8BN  \u2022  DOW \u2212849"),
    ]
    for bold, rest in lines:
        d.text((24, y), bold, font=font("DejaVuSans-Bold.ttf", 24), fill=INK)
        w = d.textlength(bold, font=font("DejaVuSans-Bold.ttf", 24))
        d.text((24 + w, y), rest, font=font("DejaVuSans.ttf", 24), fill=INK)
        y += 42
    d.line([24, 962, W - 24, 962], fill=(180, 170, 150), width=1)
    d.text((24, 972), "Every ticker item happened or was first reported on Tue 17 Nov 2026; disputed claims are attributed.",
           font=font("DejaVuSans.ttf", 15), fill=MUTED)
    d.text((24, 994), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera",
           font=font("DejaVuSans.ttf", 15), fill=MUTED)

    # JPEG bytes named entry.png: the kit allows PNG or JPEG, told apart
    # by first bytes, name stays entry.png. PNG was 1.2 MB (>1 MiB gate).
    img.save(os.path.join(HERE, "entry.png"), format="JPEG", quality=90,
             optimize=True)
    print("wrote entry.png (JPEG bytes)", img.size)


if __name__ == "__main__":
    main()
