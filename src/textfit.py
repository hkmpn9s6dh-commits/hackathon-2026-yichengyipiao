"""字宽测量与自适应字号（排版判据的唯一来源）"""
import os
from functools import lru_cache
from PIL import ImageFont

F_SERIF = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
F_SANS_M = r"C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf"
F_SANS_B = r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf"


@lru_cache(maxsize=512)
def _font(path, px):
    return ImageFont.truetype(path, px)


def width_mm(text, path, pt, tracking_em=0.0):
    """返回以 mm 计的文字宽度（1pt = 25.4/72 mm）。tracking 为字距，单位 em。"""
    px = 200
    f = _font(path, px)
    adv = 0.0
    for ch in text:
        adv += f.getlength(ch)
    adv += tracking_em * px * max(0, len(text) - 1)
    return adv / px * pt * 25.4 / 72.0


def fit_size(text, path, box_mm, pt_max, pt_min=1.0, tracking_em=0.0, step=0.05):
    """在 box_mm 内能放下的最大字号。"""
    pt = pt_max
    while pt >= pt_min:
        if width_mm(text, path, pt, tracking_em) <= box_mm:
            return round(pt, 2)
        pt -= step
    return pt_min
