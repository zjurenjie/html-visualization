#!/usr/bin/env python3
"""Chart eval helper: blank/background/sanity check for rendered PNGs.

Usage: python check_png.py <png> <expected_bg_hex>
Prints JSON: {ok, size, gray_extrema, unique_colors, bg_match}
"""
import sys
import json

from PIL import Image


def main() -> int:
    png = sys.argv[1]
    expected_bg = sys.argv[2].lstrip("#")
    with Image.open(png) as im:
        size = im.size
        rgb = im.convert("RGB")
        # sample four corners + center band (at scale=2 use 16px inset)
        inset = 16
        w, h = size
        pts = [
            rgb.getpixel((inset, inset)),
            rgb.getpixel((w - 1 - inset, inset)),
            rgb.getpixel((inset, h - 1 - inset)),
            rgb.getpixel((w - 1 - inset, h - 1 - inset)),
        ]
        exp = tuple(int(expected_bg[i:i + 2], 16) for i in (0, 2, 4))
        bg_match = all(
            all(abs(p[i] - exp[i]) <= 12 for i in range(3)) for p in pts
        )
        gray = im.convert("L")
        extrema = gray.getextrema()
        # downsampled unique color count (detect blank / near-blank renders)
        small = rgb.resize((200, max(1, int(200 * h / w))))
        colors = small.getcolors(maxcolors=200 * 200)
        unique = len(colors) if colors else 40000
        ok = extrema[1] - extrema[0] > 8 and unique > 50 and bg_match
        print(json.dumps({
            "ok": ok,
            "size": {"width": size[0], "height": size[1]},
            "gray_extrema": extrema,
            "unique_colors_ds": unique,
            "bg_match": bg_match,
            "corner_sample": [list(p) for p in pts],
        }, ensure_ascii=False))
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
