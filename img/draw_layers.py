#!/usr/bin/env python3
"""Draws one SVG per keymap layer into this directory.

The layer contents below mirror config/corne_choc_pro.keymap and have to be
updated by hand when the keymap changes. Run: python3 img/draw_layers.py

Key syntax: "tap", "tap/hold" or "tap/hold/altgr".
"" = transparent, "x" = no function, "*" = the key held to reach the layer.
"""
from html import escape
from pathlib import Path

U = 56  # px per key unit
PAD = 16
TITLE_H = 34

# (x, y, rotation, rot_x, rot_y) in key units, taken from corne_choc_pro-layouts.dtsi
# without the four unpopulated centre positions.
STAGGER = [0.37, 0.37, 0.12, 0.0, 0.12, 0.24]
KEYS = []
for row in range(3):
    for col in range(6):
        KEYS.append((col, row + STAGGER[col], 0, 0, 0))
    for col in range(6):
        KEYS.append((9 + col, row + STAGGER[5 - col], 0, 0, 0))
KEYS += [
    (3.5, 3.12, 0, 0, 0),
    (4.5, 3.12, 12, 4.5, 4.12),
    (5.48, 2.83, 24, 5.48, 4.33),
    (8.52, 2.83, -24, 9.52, 4.33),
    (9.5, 3.12, -12, 10.5, 4.12),
    (10.5, 3.12, 0, 0, 0),
]
TALL = {38, 39}  # 1.5u thumb keys

BASE_THUMBS = ["ESC/MEDIA", "SPC/NAV", "TAB/NAV", "ENT/SYM", "BSPC/NUM", "DEL/FUN"]
MODS_L = ["GUI", "AltGr", "Ctrl", "Shift"]
MODS_R = ["Shift", "Ctrl", "AltGr", "GUI"]

LAYERS = [
    ("colemak", "Colemak-DH (default)", "#57606a", [
        "TAB", "Q", "W", "F", "P", "B",                         "J", "L", "U//ü", "Y", ";", "BSPC",
        "BSPC/Ctrl", "A/GUI/ä", "R/AltGr", "S/Ctrl/ß", "T/Shift", "G",  "M", "N/Shift", "E/Ctrl", "I/AltGr", "O/GUI/ö", "'",
        "AltGr", "Z", "X", "C", "D", "V",                       "K", "H", ",", ".", "/", "Shift",
        *BASE_THUMBS]),
    ("qwerty", "QWERTY", "#57606a", [
        "TAB", "Q", "W", "E", "R", "T",                         "Y", "U//ü", "I", "O//ö", "P", "BSPC",
        "BSPC/Ctrl", "A/GUI/ä", "S/AltGr/ß", "D/Ctrl", "F/Shift", "G",  "H", "J/Shift", "K/Ctrl", "L/AltGr", ";/GUI", "'",
        "AltGr", "Z", "X", "C", "V", "B",                       "N", "M", ",", ".", "/", "Shift",
        *BASE_THUMBS]),
    ("nav", "NAV", "#0a7ea4", [
        "", "x", "x", "x", "x", "x",                            "Redo", "Home", "↑", "End", "PgUp", "DEL",
        "", *MODS_L, "x",                                       "Caps", "←", "↓", "→", "PgDn", "",
        "", "Undo", "Cut", "Copy", "Paste", "x",                "x", "x", "x", "x", "x", "",
        "x", "*", "*",                                          "ENT", "BSPC", "DEL"]),
    ("num", "NUM", "#0969da", [
        "x", "[", "7", "8", "9", "]",                           "x", "x", "x", "x", "x", "x",
        "x", ";", "4", "5", "6", "=",                           "x", *MODS_R, "x",
        "x", "`", "1", "2", "3", "-",                           "x", "x", "x", "x", "x", "x",
        ",", "0", ".",                                          "\\", "*", "x"]),
    ("sym", "SYM", "#1a7f37", [
        "x", "{", "&", "*lit", "(", "}",                        "x", "x", "x", "x", "x", "x",
        "x", ":", "$", "%", "^", "+",                           "x", *MODS_R, "x",
        "x", "~", "!", "@", "#", "|",                           "x", "x", "x", "x", "x", "x",
        "(", ")", "_",                                          "*", "x", "x"]),
    ("fun", "FUN", "#cf222e", [
        "x", "F12", "F7", "F8", "F9", "PrtSc",                  "x", "x", "x", "x", "x", "x",
        "x", "F11", "F4", "F5", "F6", "ScrLk",                  "x", *MODS_R, "x",
        "x", "F10", "F1", "F2", "F3", "Pause",                  "x", "x", "x", "x", "x", "x",
        "Menu", "SPC", "TAB",                                   "x", "x", "*"]),
    ("media", "MEDIA", "#8250df", [
        "BT Clr", "BT 0", "BT 1", "BT 2", "BT 3", "BT 4",       "RGB", "Effect", "Hue", "Sat", "Bright", "x",
        "QWERTY on", *MODS_L, "x",                              "Mute", "Prev", "Vol−", "Vol+", "Next", "x",
        "QWERTY off", "x", "x", "Reset", "Boot", "Studio",      "x", "Mic mute", "x", "x", "x", "x",
        "*", "x", "x",                                          "Stop", "Play", "Mute"]),
]

MODS = {"GUI", "AltGr", "Ctrl", "Shift"}


def text(x, y, s, size, fill, weight=400):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="middle">{escape(s)}</text>')


def draw(slug, title, accent, keys):
    assert len(keys) == len(KEYS), (slug, len(keys))
    width = 15 * U + 2 * PAD
    height = int(4.6 * U) + 2 * PAD + TITLE_H
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" '
        f'height="{height}" font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif">',
        f'<rect width="{width}" height="{height}" rx="10" fill="#f6f8fa" stroke="#d0d7de"/>',
        f'<rect x="{PAD}" y="{PAD}" width="5" height="20" rx="2" fill="{accent}"/>',
        f'<text x="{PAD + 13}" y="{PAD + 16}" font-size="16" font-weight="600" fill="#1f2328">{escape(title)}</text>',
    ]
    for i, (spec, (kx, ky, rot, rx, ry)) in enumerate(zip(keys, KEYS)):
        tap, hold, alt = (spec.split("/") + ["", ""])[:3]
        if spec == "/":
            tap, hold, alt = "/", "", ""
        if tap == "*lit":
            tap = "*"
            held = False
        else:
            held = tap == "*"
        w, h = U - 6, (1.5 * U if i in TALL else U) - 6
        x, y = PAD + kx * U + 3, PAD + TITLE_H + ky * U + 3
        cx, cy = x + w / 2, y + h / 2
        tf = ""
        if rot:
            tf = f' transform="rotate({rot} {PAD + rx * U:.1f} {PAD + TITLE_H + ry * U:.1f})"'
        out.append(f"<g{tf}>")
        if tap == "x":
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="6" fill="#eaeef2" stroke="#d8dee4"/>')
        elif tap == "":
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="6" fill="none" '
                       f'stroke="#afb8c1" stroke-dasharray="4 3"/>')
        elif held:
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="6" fill="{accent}"/>')
            out.append(text(cx, cy + 4, "held", 11, "#ffffff", 600))
        else:
            is_mod = tap in MODS
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="6" fill="#ffffff" '
                       f'stroke="{accent if is_mod else "#afb8c1"}"/>')
            words = tap.split(" ") if len(tap) > 6 else [tap]
            size = 15 if len(tap) <= 2 else 11
            base = cy + (-1 if hold else 5) - (len(words) - 1) * 6
            for n, word in enumerate(words):
                out.append(text(cx, base + n * 13, word, size, accent if is_mod else "#1f2328", 600 if len(tap) <= 2 else 500))
            if hold:
                out.append(text(cx, y + h - 6, hold, 9.5, accent if accent != "#57606a" else "#0969da", 600))
            if alt:
                out.append(text(x + w - 9, y + 14, alt, 11, "#bc4c00", 600))
        out.append("</g>")
    out.append("</svg>")
    (Path(__file__).parent / f"{slug}.svg").write_text("\n".join(out) + "\n", encoding="utf-8")


for layer in LAYERS:
    draw(*layer)
