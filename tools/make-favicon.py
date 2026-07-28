#!/usr/bin/env python3
"""
Fabrique favicon.ico (16/32/48) + favicon-32.png depuis la marque Kyroz en
version OUTLINE (celle de la charte), marque seule sur fond transparent.

Deux choix techniques a connaitre avant de toucher a ce fichier :

1. RASTERISEUR MAISON. Les convertisseurs presents sur la machine (qlmanage)
   aplatissent la transparence sur du blanc, ce qui remettrait un carre blanc
   autour du logo. On dessine donc nous-memes, sans dependance.

2. EPAISSEUR DE TRAIT OPTIQUE. Le trait de la charte (9 unites sur 366) donne
   0,4 px a 16 px : le contour se referme en une tache. L'epaisseur est donc
   recalculee par taille pour valoir ~1,3 px a l'ecran.
"""
import struct, zlib

VIEW = (72.0, 72.0, 366.0)
SPAN = VIEW[2]
SHAPES = [
    [(428.58, 82.30), (303.00, 85.30), (82.67, 306.38), (81.92, 427.45)],
    [(236.07, 337.96), (305.25, 429.70), (430.08, 429.70), (303.75, 277.06)],
    [(185.69, 82.30), (82.67, 82.30), (81.92, 240.96), (186.44, 143.21)],
]
INK = (255, 255, 255)
SS = 4
STROKE_PX = 1.3


def signed_area(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def inset(poly, d):
    sign = 1.0 if signed_area(poly) > 0 else -1.0
    n = len(poly)
    lines = []
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        ln = (dx * dx + dy * dy) ** 0.5
        if ln == 0:
            return None
        nx, ny = -dy / ln * sign, dx / ln * sign
        lines.append((x1 + nx * d, y1 + ny * d, dx, dy))
    out = []
    for i in range(n):
        px, py, dx, dy = lines[i - 1]
        qx, qy, ex, ey = lines[i]
        den = dx * ey - dy * ex
        if abs(den) < 1e-9:
            return None
        t = ((qx - px) * ey - (qy - py) * ex) / den
        out.append((px + dx * t, py + dy * t))
    return out


def inside(poly, x, y):
    hit = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) / (y2 - y1) * (x2 - x1):
                hit = not hit
    return hit


def coverage(size, stroke_px=STROKE_PX):
    d_units = stroke_px / size * SPAN
    ox, oy = VIEW[0], VIEW[1]

    def to_px(poly):
        return [((p[0] - ox) / SPAN * size, (p[1] - oy) / SPAN * size) for p in poly]

    bands = []
    for shape in SHAPES:
        small = inset(shape, d_units)
        bands.append((to_px(shape), to_px(small) if small else None))

    step, rows = 1.0 / SS, []
    for py in range(size):
        row = []
        for px in range(size):
            c = 0
            for sy in range(SS):
                y = py + step / 2 + sy * step
                for sx in range(SS):
                    x = px + step / 2 + sx * step
                    for outer, inner in bands:
                        if inside(outer, x, y) and not (inner and inside(inner, x, y)):
                            c += 1
                            break
            row.append(c / (SS * SS))
        rows.append(row)
    return rows


def render(size):
    rows = []
    for row in coverage(size):
        b = bytearray()
        for a in row:
            b += bytes((INK[0], INK[1], INK[2], round(a * 255)))
        rows.append(bytes(b))
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
    n = len(images)
    out = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    blobs = b""
    for size, data in images:
        out += struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(data), offset)
        blobs += data
        offset += len(data)
    return out + blobs


if __name__ == "__main__":
    imgs = []
    for s in (16, 32, 48):
        data = png(s, render(s))
        imgs.append((s, data))
        print("  %dx%d : trait %.1f unites, %d octets" % (s, s, STROKE_PX / s * SPAN, len(data)))
    open("/Users/kevinberger/Kyroz_Site/favicon.ico", "wb").write(ico(imgs))
    open("/Users/kevinberger/Kyroz_Site/favicon-32.png", "wb").write(imgs[1][1])
    print("favicon.ico + favicon-32.png ecrits")
