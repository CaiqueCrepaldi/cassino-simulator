"""Generates a casino chip icon and saves it as casino.ico."""

import math
from PIL import Image, ImageDraw, ImageFont


def draw_casino_chip(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r = size // 2 - 2

    # Shadow
    shadow_offset = max(2, size // 48)
    draw.ellipse(
        [cx - r + shadow_offset, cy - r + shadow_offset,
         cx + r + shadow_offset, cy + r + shadow_offset],
        fill=(0, 0, 0, 100),
    )

    # Outer ring (gold)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#B8860B")

    # Red body
    inner_r = int(r * 0.88)
    draw.ellipse(
        [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
        fill="#CC0000",
    )

    # Dashed border segments (white/gold alternating)
    seg_count = 16
    seg_r_outer = int(r * 0.88)
    seg_r_inner = int(r * 0.72)
    for i in range(seg_count):
        angle_start = (360 / seg_count) * i - 90
        angle_end   = angle_start + (360 / seg_count) * 0.55
        color = "#FFD700" if i % 2 == 0 else "#FFFFFF"
        draw.arc(
            [cx - seg_r_outer, cy - seg_r_outer,
             cx + seg_r_outer, cy + seg_r_outer],
            start=angle_start, end=angle_end,
            fill=color,
            width=max(2, int(r * 0.16)),
        )

    # Inner white circle
    white_r = int(r * 0.70)
    draw.ellipse(
        [cx - white_r, cy - white_r, cx + white_r, cy + white_r],
        fill="#FFFFFF",
    )

    # Red circle inside white
    red2_r = int(r * 0.60)
    draw.ellipse(
        [cx - red2_r, cy - red2_r, cx + red2_r, cy + red2_r],
        fill="#CC0000",
    )

    # "777" text
    text = "777"
    font_size = max(6, int(r * 0.40))
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = cy - th // 2 - bbox[1]

    # Text shadow
    draw.text((tx + 1, ty + 1), text, font=font, fill="#800000")
    draw.text((tx, ty), text, font=font, fill="#FFD700")

    return img


def main() -> None:
    sizes = [16, 24, 32, 48, 64, 128, 256]
    frames = [draw_casino_chip(s) for s in sizes]

    frames[0].save(
        "casino.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=frames[1:],
    )
    print("casino.ico gerado com sucesso!")


if __name__ == "__main__":
    main()