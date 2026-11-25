#!/usr/bin/env python3
"""news-image-20261125: "The World in One Day".

Draws a hero-led newspaper front page summing up Wednesday 25 November
2026's world news, using only the Python standard library (the grader
installs nothing, so no PIL).  Writes /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png): 1024x1024 PNG, deterministic.

Stories (all as reported on Wednesday 25 November 2026):
  HERO  - Shanghai party chief Chen Jining under corruption probe;
          Shanghai's party leadership pledges loyalty to Beijing
          (Reuters, published 2026-11-25T00:34Z; Xinhua/CNN/WSJ).
  UN    - 47,000 women and girls killed by partners or family in 2025,
          five every hour; 16 Days of Activism opens 25 Nov (UN Women).
  COURTS- US jury convicts Huawei of trade-secret theft and bank fraud
          (reported 25 Nov; The Hindu morning digest, AP).
  SECURITY - CIA and ODNI hit by a cybersecurity breach of unclassified
          information (NYT, reported 25 Nov; The Hindu).
  AMERICAS - 25 hostages held at a Cartagena supermarket after a botched
          armoured-truck robbery; five elderly women freed (AP/AFP,
          reported 25 Nov).
  WAR   - More than 700,000 Russian soldiers killed in the Ukraine war,
          new analysis finds (RFE/RL, published 2026-11-25 01:00Z).
  ASIA  - 5.3-magnitude earthquake hits Nepal; tremors felt across
          India, Bhutan and China (NDTV, 25 Nov).
"""

import os
import struct
import sys
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (176, 30, 36)
GREY = (112, 107, 96)
SKY_TOP = (176, 196, 210)
SKY_BOT = (228, 233, 236)
TOWER = (52, 72, 102)
TOWER_DK = (34, 50, 74)
GOLD = (201, 162, 39)
PINK = (214, 96, 110)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, '#' = ink.  Uppercase, digits and the
# punctuation this page needs.  All text on the page is set in caps.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "—": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "•": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


def text_width(text, scale):
    return len(text) * 6 * scale


def wrap(text, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(" "), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            base = (yy * self.w + x) * 3
            self.px[base:base + w * 3] = bytes(color) * w

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def border(self, x, y, w, h, color, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, t=2):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5)
            dx2 = int(max(0, (r - t) * (r - t) - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) < r - t else 0
            self.rect(cx - dx, yy, dx - dx2, 1, color)
            self.rect(cx + dx2 + 1, yy, dx - dx2, 1, color)

    def text(self, x, y, s, scale, color, align="left"):
        if align == "center":
            x -= text_width(s, scale) // 2
        elif align == "right":
            x -= text_width(s, scale)
        for ch in s:
            glyph = FONT.get(ch.upper(), FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(x + col * scale, y + row * scale, scale, scale, color)
            x += 6 * scale

    def text_block(self, x, y, lines, scale, color, leading=None, align="left"):
        lh = leading if leading is not None else 7 * scale + 4
        for i, line in enumerate(lines):
            self.text(x, y + i * lh, line, scale, color, align)
        return y + len(lines) * lh


# ------------------------------------------------------------------ skyline
def draw_skyline(cv, x0, y0, w, h):
    """Shanghai / Lujiazui at dawn: Oriental Pearl Tower, stepped Jin
    Mao tower, trapezoid-topped tower, red sun, gold windows."""
    # sky bands
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(SKY_TOP[k] + (SKY_BOT[k] - SKY_TOP[k]) * t) for k in range(3))
        cv.hline(x0, y0 + i, w, c)
    base = y0 + h
    # red sun
    cv.disc(x0 + w - 62, y0 + 52, 30, RED)
    cv.ring(x0 + w - 62, y0 + 52, 36, RED, 2)
    # far tower (left, stepped Jin Mao style)
    tx = x0 + 18
    cv.rect(tx, y0 + 150, 54, base - (y0 + 150), TOWER_DK)
    cv.rect(tx + 8, y0 + 128, 38, 24, TOWER_DK)
    cv.rect(tx + 15, y0 + 108, 24, 22, TOWER_DK)
    cv.rect(tx + 24, y0 + 96, 6, 14, TOWER_DK)
    # trapezoid-topped tower (right)
    rx = x0 + w - 96
    cv.rect(rx, y0 + 168, 62, base - (y0 + 168), TOWER)
    for i in range(24):  # trapezoid roof: narrow top, wide base
        rw = 20 + (62 - 20) * i // 23
        cv.rect(rx + (62 - rw) // 2, y0 + 144 + i, rw, 1, TOWER)
    # Oriental Pearl Tower (centre): spire + two spheres
    cx = x0 + w // 2 + 8
    cv.rect(cx - 3, y0 + 60, 6, base - (y0 + 60), TOWER_DK)
    cv.disc(cx, y0 + 118, 34, PINK)
    cv.ring(cx, y0 + 118, 34, INK, 2)
    cv.disc(cx, y0 + 196, 22, PINK)
    cv.ring(cx, y0 + 196, 22, INK, 2)
    cv.rect(cx - 26, y0 + 232, 52, 8, TOWER_DK)
    # low blocks
    cv.rect(x0 + 84, y0 + 216, 66, base - (y0 + 216), TOWER)
    cv.rect(x0 + w - 178, y0 + 228, 58, base - (y0 + 228), TOWER_DK)
    # gold windows on the towers (deterministic grid)
    for bx, by, bw, bh in ((tx, y0 + 150, 54, base - (y0 + 150)),
                           (rx, y0 + 168, 62, base - (y0 + 168)),
                           (x0 + 84, y0 + 216, 66, base - (y0 + 216))):
        for wy in range(by + 12, by + bh - 8, 16):
            for wx in range(bx + 8, bx + bw - 8, 14):
                if (wx * 7 + wy * 13) % 5 < 2:
                    cv.rect(wx, wy, 4, 5, GOLD)
    # birds (right of the stamp, under the sun)
    for bx, by in ((x0 + 200, y0 + 92), (x0 + 224, y0 + 80), (x0 + 248, y0 + 98)):
        cv.rect(bx, by, 10, 2, INK)
        cv.rect(bx + 10, by - 3, 2, 3, INK)
        cv.rect(bx + 18, by, 10, 2, INK)
        cv.rect(bx + 16, by - 3, 2, 3, INK)
    # foreground band
    cv.rect(x0, base - 34, w, 34, INK)
    for i in range(0, w, 26):
        if (i * 11) % 7 < 3:
            cv.rect(x0 + i + 6, base - 26 + (i % 12), 3, 3, GOLD)
    # red stamp: UNDER PROBE (top-left, over the pale sky for contrast)
    sx, sy, sw, sh = x0 + 18, y0 + 14, 196, 52
    cv.border(sx, sy, sw, sh, RED, 3)
    cv.border(sx + 6, sy + 6, sw - 12, sh - 12, RED, 1)
    cv.text(sx + sw // 2, sy + 9, "UNDER", 2, RED, "center")
    cv.text(sx + sw // 2, sy + 27, "PROBE", 2, RED, "center")


# ------------------------------------------------------------------ stories
CARDS = [
    ("UNITED NATIONS", "FIVE WOMEN KILLED EVERY HOUR",
     "UN: 47,000 women and girls killed by partners or family in 2025."),
    ("COURTS", "HUAWEI GUILTY OF STEALING SECRETS",
     "US jury convicts the tech giant of trade-secret theft and bank fraud."),
    ("SECURITY", "CIA AND SPY CHIEF HIT BY BREACH",
     "Unclassified data exposed in a cyber breach, the NYT reports."),
    ("AMERICAS", "25 HELD HOSTAGE IN CARTAGENA",
     "Gunmen seize a supermarket after a botched truck robbery; five freed."),
    ("WAR IN UKRAINE", "700,000 RUSSIAN TROOPS KILLED",
     "New analysis puts Moscow's dead in Ukraine past 700,000."),
    ("ASIA", "5.3 QUAKE SHAKES NEPAL",
     "Tremors felt across India, Bhutan and China."),
]


def draw(cv):
    cv.border(12, 12, W - 24, H - 24, INK, 3)
    cv.border(20, 20, W - 40, H - 40, INK, 1)

    # ---- masthead
    cv.text(W // 2, 40, "THE WORLD IN ONE DAY", 8, INK, "center")
    cv.hline(34, 112, W - 68, INK, 2)
    cv.text(W // 2, 124, "WEDNESDAY 25 NOVEMBER 2026", 5, RED, "center")
    cv.text(W // 2, 168, "ONE DAY  •  EVERYWHERE  •  ONE PAGE", 2, GREY, "center")
    cv.hline(34, 196, W - 68, INK, 3)

    # ---- hero: left text, right skyline
    hx, hy = 34, 208
    cv.text(hx, hy, "CHINA — THE PURGE WIDENS", 2, RED)
    cv.text(hx, hy + 30, "SHANGHAI CHIEF", 6, INK)
    cv.text(hx, hy + 78, "FALLS IN XI'S", 6, INK)
    cv.text(hx, hy + 126, "PURGE", 6, INK)
    deck = wrap("Shanghai's party chiefs pledge loyalty to Beijing a day "
                "after Politburo member Chen Jining, 62, was probed — "
                "the fourth top leader to fall since 2025.",
                3, 560)
    cv.text_block(hx, hy + 190, deck, 3, INK, leading=26)
    draw_skyline(cv, 620, 206, 370, 314)

    cv.hline(34, 536, W - 68, INK, 2)
    cv.text(34, 548, "THE DAY IN BRIEF", 3, RED)
    cv.text(W - 34, 548, "25 NOVEMBER 2026", 2, GREY, "right")

    # ---- six story cards, 2 columns x 3 rows
    cw, ch, gx, gy = 468, 110, 16, 10
    for i, (kicker, head, deck_text) in enumerate(CARDS):
        cx = 34 + (i % 2) * (cw + gx)
        cy = 578 + (i // 2) * (ch + gy)
        cv.border(cx, cy, cw, ch, INK, 1)
        cv.rect(cx, cy, 6, ch, RED)
        cv.text(cx + 18, cy + 7, kicker, 2, RED)
        head_lines = wrap(head, 3, cw - 36)
        y = cv.text_block(cx + 18, cy + 27, head_lines[:2], 3, INK, leading=24)
        deck_lines = wrap(deck_text, 2, cw - 36)
        cv.text_block(cx + 18, y + 3, deck_lines[:2], 2, GREY, leading=15)

    # ---- footer
    cv.hline(34, 938, W - 68, INK, 2)
    cv.text(W // 2, 948, "SOURCES: REUTERS • AP • AFP • UN WOMEN • THE HINDU • NDTV • RFE/RL",
            2, GREY, "center")
    cv.text(W // 2, 968, "STORIES AS REPORTED ON WEDNESDAY 25 NOVEMBER 2026 • MAKE.FUN NEWS-IMAGE-20261125",
            2, GREY, "center")


# ------------------------------------------------------------------ PNG out
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the directory's contents, never the directory itself:
    # the grader mounts /output root-owned.
    for name in os.listdir(out_dir):
        p = os.path.join(out_dir, name)
        if os.path.isfile(p):
            os.remove(p)
    cv = Canvas(W, H, PAPER)
    draw(cv)
    size = write_png(cv, os.path.join(out_dir, "entry.png"))
    print(f"wrote {os.path.join(out_dir, 'entry.png')} ({W}x{H}, {size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
