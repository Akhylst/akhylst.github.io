"""Üç sitenin ana ekran simgeleri (PWA): İlk Notada (plak), Hayvan Terazisi (pirinç terazi), Bizim Oyunlar (kalp).
Her biri 1024 px'te çizilip küçültülür (yumuşak kenar); içerik ortadaki %62'de (Android'in yuvarlak/maskeli kırpması kesmesin).
Çıktı: ikon-512.png, ikon-192.png, ikon-180.png (iPhone) → ../sarki_oyunu/web, ../hayvan_terazisi/web, bu klasör.
Kullanım: python -I ikon.py"""
import math
import os

from PIL import Image, ImageDraw

K = os.path.dirname(os.path.abspath(__file__))
S = 1024


def kaydet(img, klasor):
    for n in (512, 192, 180):
        img.resize((n, n), Image.LANCZOS).save(os.path.join(klasor, f"ikon-{n}.png"), optimize=True)
    print("ikon ->", klasor)


def daire(d, x, y, r, renk):
    d.ellipse((x - r, y - r, x + r, y + r), fill=renk)


def plak():
    img = Image.new("RGB", (S, S), "#fde3ec")
    d = ImageDraw.Draw(img)
    c = S / 2
    daire(d, c, c, 0.34 * S, "#17131f")
    r = 0.17 * S
    while r < 0.33 * S:  # oluklar
        d.ellipse((c - r, c - r, c + r, c + r), outline="#2e2738", width=5)
        r += 0.026 * S
    d.arc((c - 0.3 * S, c - 0.3 * S, c + 0.3 * S, c + 0.3 * S), 200, 250, fill="#4a4157", width=10)  # parıltı
    daire(d, c, c, 0.135 * S, "#e8467b")
    daire(d, c, c, 0.024 * S, "#17131f")
    return img


def terazi():
    img = Image.new("RGB", (S, S), "#1c1f27")
    d = ImageDraw.Draw(img)
    k, renk, w = 0.62 * S / 24, "#e6bd62", int(0.045 * S)
    p = lambda x, y: (S / 2 + (x - 12) * k, S / 2 + (y - 12) * k)  # logodaki 24 birimlik çizim
    def cizgi(a, b):
        d.line([p(*a), p(*b)], fill=renk, width=w)
        for q in (a, b):
            daire(d, *p(*q), w / 2, renk)
    cizgi((12, 3), (12, 20)); cizgi((7, 21), (17, 21)); cizgi((4, 7), (20, 7))
    for x in (4, 20):
        cizgi((x, 7), (x - 2.5, 13)); cizgi((x, 7), (x + 2.5, 13))
        (x0, y0), (x1, y1) = p(x - 2.8, 10.4), p(x + 2.8, 15.6)
        d.pieslice((x0, y0, x1, y1), 0, 180, fill=renk)  # kefe
    return img


def kalp():
    img = Image.new("RGB", (S, S))
    d = ImageDraw.Draw(img)
    a, b = (255, 124, 164), (109, 79, 230)
    for y in range(S):  # yukarıdan aşağı pembe → mor
        t = y / S
        d.line([(0, y), (S, y)], fill=tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)))
    pts = []
    for i in range(400):  # kalp eğrisi
        t = 2 * math.pi * i / 400
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((S / 2 + x * 0.0185 * S, S / 2 - y * 0.0185 * S + 0.02 * S))
    d.polygon(pts, fill="#ffffff")
    return img


if __name__ == "__main__":
    kaydet(plak(), os.path.join(K, "..", "sarki_oyunu", "web"))
    kaydet(terazi(), os.path.join(K, "..", "hayvan_terazisi", "web"))
    kaydet(kalp(), K)
