#!/usr/bin/env python3
"""
Fabrique favicon.ico (16/32/48 px) à partir de la marque Kyroz.

Pourquoi un rastériseur maison plutôt qu'un outil : les convertisseurs
disponibles sur cette machine (qlmanage) aplatissent la transparence sur du
blanc — ce qui aurait remis exactement le carré blanc qu'on cherche à retirer.
Les trois formes de la marque sont des polygones à segments droits, donc on
peut les remplir soi-même proprement, avec anti-crénelage par sur-échantillonnage.
"""
import struct, zlib

# Tracés de la marque (mêmes coordonnées que kyroz-mark.svg), viewBox 72 72 366 366
VIEW = (72.0, 72.0, 366.0)
POLYS = [
    [(428.58, 82.30), (303.00, 85.30), (82.67, 306.38), (81.92, 427.45)],
    [(236.07, 337.96), (305.25, 429.70), (430.08, 429.70), (303.75, 277.06)],
    [(185.69, 82.30), (82.67, 82.30), (81.92, 240.96), (186.44, 143.21)],
]
INK = (255, 255, 255)   # blanc : l'icône est destinée aux interfaces sombres
SS = 4                  # sur-échantillonnage (4x4 = 16 échantillons par pixel)


def to_px(pt, size):
    ox, oy, span = VIEW
    return ((pt[0] - ox) / span * size, (pt[1] - oy) / span * size)


def inside(poly, x, y):
    """Test point-dans-polygone par lancer de rayon."""
    hit = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xint = x1 + (y - y1) / (y2 - y1) * (x2 - x1)
            if x < xint:
                hit = not hit
    return hit


def render(size):
    polys = [[to_px(p, size) for p in poly] for poly in POLYS]
    rows = []
    step = 1.0 / SS
    half = step / 2.0
    for py in range(size):
        row = bytearray()
        for px in range(size):
            covered = 0
            for sy in range(SS):
                y = py + half + sy * step
                for sx in range(SS):
                    x = px + half + sx * step
                    if any(inside(poly, x, y) for poly in polys):
                        covered += 1
            alpha = round(covered * 255 / (SS * SS))
            row += bytes((INK[0], INK[1], INK[2], alpha))
        rows.append(bytes(row))
    return rows


def png(size, rows):
    raw = b"".join(b"\x00" + r for r in rows)

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def ico(images):
    """Conteneur ICO à charges utiles PNG (supporté depuis Vista / tous navigateurs actuels)."""
    n = len(images)
    header = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    entries, blobs = b"", b""
    for size, data in images:
        entries += struct.pack("<BBBBHHII", size if size < 256 else 0,
                               size if size < 256 else 0, 0, 0, 1, 32,
                               len(data), offset)
        blobs += data
        offset += len(data)
    return header + entries + blobs


imgs = []
for s in (16, 32, 48):
    data = png(s, render(s))
    imgs.append((s, data))
    print(f"  {s}x{s} : {len(data)} octets")

out = ico(imgs)
with open("/Users/kevinberger/Kyroz_Site/favicon.ico", "wb") as f:
    f.write(out)
print(f"favicon.ico : {len(out)} octets, {len(imgs)} tailles")

# Un PNG 32px seul, utile comme icône de repli déclarée dans le HTML
with open("/Users/kevinberger/Kyroz_Site/favicon-32.png", "wb") as f:
    f.write(imgs[1][1])
print("favicon-32.png écrit")
