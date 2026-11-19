"""把 SVG 里的 <text> 全部转成 <path>：源文件不依赖任何字体。

为什么要这么做：fontTools 在这台机器的思源宋体上子集化会崩（glyf.trim IndexError），
而评审打开源文件时若缺字体会整体掉字。转路径后，矢量、分层、字体三件事都不再互相牵制。
"""
import os
import re

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONTS = {
    "Source Han Serif SC Heavy": r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf",
    "Noto Sans SC Medium": r"C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf",
    "Noto Sans SC": r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf",
}

_cache = {}


def _font(path):
    if path not in _cache:
        f = TTFont(path, fontNumber=0)
        upem = f["head"].unitsPerEm
        cmap = f.getBestCmap()
        gs = f.getGlyphSet()
        hmtx = f["hmtx"]
        _cache[path] = (upem, cmap, gs, hmtx)
    return _cache[path]


def _attr(attrs, name, default=None):
    m = re.search(r'\b' + name + r'="([^"]*)"', attrs)
    return m.group(1) if m else default


def text_to_path(match):
    attrs, body = match.group(1), match.group(2)
    if not body.strip():
        return ""
    fam = _attr(attrs, "font-family", "Noto Sans SC")
    size = float(_attr(attrs, "font-size", "1"))
    x = float(_attr(attrs, "x", "0"))
    y = float(_attr(attrs, "y", "0"))
    fill = _attr(attrs, "fill", "#000000")
    ls = float(_attr(attrs, "letter-spacing", "0"))
    anchor = _attr(attrs, "text-anchor", "start")
    op = _attr(attrs, "opacity")
    path = FONTS.get(fam, FONTS["Noto Sans SC"])
    upem, cmap, gs, hmtx = _font(path)
    s = size / upem

    glyphs, total = [], 0.0
    for i, ch in enumerate(body):
        gname = cmap.get(ord(ch))
        adv = hmtx[gname][0] if gname else upem * 0.5
        glyphs.append((ch, gname, adv, total))
        total += adv + (ls / s if i < len(body) - 1 else 0)
    total_px = total * s

    if anchor == "middle":
        x -= total_px / 2
    elif anchor == "end":
        x -= total_px

    d_parts = []
    for ch, gname, adv, off in glyphs:
        if not gname:
            continue
        pen = SVGPathPen(gs)
        gs[gname].draw(pen)
        d = pen.getCommands()
        if d:
            d_parts.append(f'<path d="{d}" transform="translate({x + off * s:.4f},{y:.4f}) scale({s:.6f},{-s:.6f})"/>')
    if not d_parts:
        return ""
    opacity = f' opacity="{op}"' if op else ""
    return f'<g fill="{fill}"{opacity}>' + "".join(d_parts) + "</g>"


def outline(svg):
    return re.sub(r"<text([^>]*)>([^<]*)</text>", text_to_path, svg)
