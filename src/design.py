"""《一城一票》视觉系统：所有版面由数据驱动，单位一律 mm。

票面骨架（一票）：
  0   ┌ 打孔边 ┐
  4.4  眉批：江蘇省城市足球聯賽 / 2026
  6.2  ┌ 形象窗口 ┐
 44    └─────────┘
 54    城市名（大宋）        红印（右）
 57.6  拼音
 64.5  口号
 66.8  ─────────
 70.8  嘟嘟·原型 / 编号
 75    └───────┘
"""
import base64, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CITIES = json.load(open(os.path.join(ROOT, "data", "cities.json"), encoding="utf-8"))

PAPER = "#F4EFE4"
PAPER_2 = "#E9E2D1"
INK = "#1A1917"
INK_SOFT = "#4B463C"
RED = "#A6322A"
GOLD = "#A8823C"
DEEP = "#12211D"

F_SERIF = r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
SERIF = "Source Han Serif SC Heavy"
SANS = "Noto Sans SC"
SANS_M = "Noto Sans SC Medium"

ABBR = {"nanjing": "宁", "wuxi": "锡", "xuzhou": "徐", "changzhou": "常",
        "suzhou": "苏", "nantong": "通", "lianyungang": "连", "huaian": "淮",
        "yancheng": "盐", "yangzhou": "扬", "zhenjiang": "镇", "taizhou": "泰",
        "suqian": "宿"}

_ARTS = {}


def art_b64(city_id):
    if city_id not in _ARTS:
        p = os.path.join(ROOT, "assets", "art", "glaze", city_id + ".png")
        with open(p, "rb") as f:
            _ARTS[city_id] = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return _ARTS[city_id]


def seal(x, y, size, ch, color=RED, opacity=1.0, rotate=0.0):
    s = size
    return f'''<g transform="translate({x},{y}) rotate({rotate})" opacity="{opacity}">
  <rect x="0" y="0" width="{s}" height="{s}" rx="{s*0.07}" fill="none" stroke="{color}" stroke-width="{s*0.062}"/>
  <rect x="{s*0.085}" y="{s*0.085}" width="{s*0.83}" height="{s*0.83}" rx="{s*0.04}" fill="none" stroke="{color}" stroke-width="{s*0.022}" opacity="0.5"/>
  <text x="{s/2}" y="{s*0.545}" font-family="{SERIF}" font-size="{s*0.66}" fill="{color}"
        text-anchor="middle">{ch}</text>
</g>'''


def perf_mask(w, h, uid, r=None, pitch=None):
    r = r if r is not None else w * 0.016
    pitch = pitch if pitch is not None else r * 2.5
    circles = []
    n_x = int((w - 2 * r) // pitch)
    off_x = (w - (n_x - 1) * pitch) / 2
    for i in range(n_x):
        x = off_x + i * pitch
        circles.append(f'<circle cx="{x:.3f}" cy="0" r="{r}"/>')
        circles.append(f'<circle cx="{x:.3f}" cy="{h}" r="{r}"/>')
    n_y = int((h - 2 * r) // pitch)
    off_y = (h - (n_y - 1) * pitch) / 2
    for i in range(n_y):
        y = off_y + i * pitch
        circles.append(f'<circle cx="0" cy="{y:.3f}" r="{r}"/>')
        circles.append(f'<circle cx="{w}" cy="{y:.3f}" r="{r}"/>')
    return (f'<mask id="perf{uid}" maskUnits="userSpaceOnUse" x="{-r}" y="{-r}" '
            f'width="{w+2*r}" height="{h+2*r}">'
            f'<rect x="{-r}" y="{-r}" width="{w+2*r}" height="{h+2*r}" fill="#fff"/>'
            + "".join(circles) + "</mask>")


def _lum(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5))


def ink_of(hexcolor, ground=PAPER, need=4.5):
    """把城市色压到能在纸色上读清为止；判据是 WCAG 对比度，不是眼估。"""
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    for k in range(0, 101, 2):
        t = k / 100.0
        c = (round(r * (1 - t)), round(g * (1 - t)), round(b * (1 - t)))
        if _contrast(tuple(v / 255 for v in c), _rgb(ground)) >= need:
            return "#%02X%02X%02X" % c
    return "#000000"


def mix(hex_a, hex_b, t):
    a = [int(hex_a[i:i+2], 16) for i in (1, 3, 5)]
    b = [int(hex_b[i:i+2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i]*(1-t)+b[i]*t):02X}" for i in range(3))


def figure(city, x, y, w, h, opacity=1.0):
    return (f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" opacity="{opacity}" '
            f'preserveAspectRatio="xMidYMax meet" href="{art_b64(city["id"])}"/>')


def stamp(city, S=60.0, uid="s", fill=None):
    """一枚票：上图下文。S 为宽度，高度 1.25S。"""
    u = S / 60.0
    w, h = S, S * 1.25
    fill = fill or PAPER
    panel_h = 39.6 * u
    tint = mix(PAPER_2, city["color"], 0.13)
    return f'''<g class="stamp" data-city="{city["id"]}">
  <g mask="url(#perf{uid})">
    <rect x="0" y="0" width="{w}" height="{h}" fill="{fill}"/>
    <clipPath id="cw{uid}"><rect x="0" y="0" width="{w}" height="{panel_h}"/></clipPath>
    <rect x="0" y="0" width="{w}" height="{panel_h}" fill="{tint}"/>
    <g clip-path="url(#cw{uid})">
      {figure(city, 0, -panel_h*0.015, w, panel_h * 1.0)}
      <path d="M0,{panel_h-1.6*u} q{3.2*u},{-1.7*u} {6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0 t{6.4*u},0"
            fill="none" stroke="{city["color"]}" stroke-width="{0.3*u}" opacity="0.4"/>
    </g>
    <rect x="{2.4*u}" y="{2.4*u}" width="{w-4.8*u}" height="{panel_h-4.8*u}" fill="none" stroke="{INK}" stroke-width="{0.12*u}" opacity="0.45"/>
    <line x1="0" y1="{panel_h}" x2="{w}" y2="{panel_h}" stroke="{INK}" stroke-width="{0.16*u}" opacity="0.55"/>
    <text x="{2.6*u}" y="{54.0*u}" font-family="{SERIF}" font-size="{12.6*u}" fill="{INK}" letter-spacing="{0.9*u}">{city["name"]}</text>
    <text x="{2.8*u}" y="{57.6*u}" font-family="{SANS_M}" font-size="{2.8*u}" fill="{INK_SOFT}" letter-spacing="{0.66*u}">{city["pinyin"]}</text>
    {seal(w-13.4*u, 44.6*u, 9.8*u, ABBR[city["id"]])}
    <text x="{2.6*u}" y="{64.6*u}" font-family="{SERIF}" font-size="{5.2*u}" fill="{ink_of(city["color"])}" letter-spacing="{0.6*u}">{city["slogan"]}</text>
    <line x1="{2.4*u}" y1="{67.4*u}" x2="{w-2.4*u}" y2="{67.4*u}" stroke="{INK}" stroke-width="{0.1*u}" opacity="0.28"/>
    <text x="{2.6*u}" y="{71.9*u}" font-family="{SANS_M}" font-size="{2.35*u}" fill="{INK_SOFT}">{city["dudu"]} · {city["totem"]}</text>
    <text x="{w-2.6*u}" y="{71.9*u}" font-family="{SANS}" font-size="{2.35*u}" fill="{INK_SOFT}" text-anchor="end">{city["no"]:02d}/13</text>
  </g>
</g>'''


def html_page(body, w_mm, h_mm):
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  @page {{ size: {w_mm}mm {h_mm}mm; margin: 0 }}
  html,body {{ margin:0; padding:0; }}
  svg {{ display:block }}
</style></head><body>{body}</body></html>'''


def svg_open(W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">')


# ---------------------------------------------------------------- 作品一：小版张 A3

def sheet():
    W, H = 297.0, 420.0
    S, GAP = 60.0, 6.0
    cols, rows = 4, 4
    grid_w = cols * S + (cols - 1) * GAP
    grid_h = rows * S * 1.25 + (rows - 1) * GAP
    x0 = (W - grid_w) / 2
    y0 = 78.0

    parts = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>',
             f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="{INK}" stroke-width="0.25" opacity="0.3"/>']

    # 抬头：标题宽度先量后放，避免与副标相撞
    import textfit as tf
    title = "一城一票"
    t_pt = 44.0
    t_w = tf.width_mm(title, tf.F_SERIF, t_pt, 1.2)
    right = x0 + grid_w
    parts += [
        f'<text x="{x0}" y="18" font-family="{SANS_M}" font-size="3.6" fill="{INK_SOFT}" letter-spacing="1.4">JIANGSU CITY FOOTBALL LEAGUE　·　2026</text>',
        f'<text x="{x0}" y="58" font-family="{SERIF}" font-size="{t_pt}" fill="{INK}" letter-spacing="1.2">一城一票</text>',
        f'<text x="{right}" y="43" font-family="{SERIF}" font-size="7.4" fill="{INK}" text-anchor="end">十三枚 · 小版张</text>',
        f'<text x="{right}" y="50.4" font-family="{SANS}" font-size="2.9" fill="{INK_SOFT}" letter-spacing="0.3" text-anchor="end">ONE CITY, ONE TICKET</text>',
        f'<text x="{right}" y="55.2" font-family="{SANS}" font-size="2.9" fill="{INK_SOFT}" letter-spacing="0.3" text-anchor="end">SHEET OF THIRTEEN · 300 DPI</text>',
        f'<line x1="{x0}" y1="66" x2="{right}" y2="66" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>',
    ]

    masks = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            cell = r * cols + c
            x = x0 + c * (S + GAP)
            y = y0 + r * (S * 1.25 + GAP)
            if idx < len(CITIES):
                masks.append(perf_mask(S, S * 1.25, f"sh{idx}"))
                parts.append(f'<g transform="translate({x},{y})">{stamp(CITIES[idx], S, f"sh{idx}")}</g>')
                idx += 1
                continue
            parts.append(_bridge(cell - 13, x, y, S))

    fy = y0 + grid_h + 12
    parts += [
        f'<line x1="{x0}" y1="{fy-6}" x2="{x0+grid_w}" y2="{fy-6}" stroke="{INK}" stroke-width="0.3" opacity="0.35"/>',
        f'<text x="{x0}" y="{fy}" font-family="{SANS_M}" font-size="3.3" fill="{INK_SOFT}">江苏省城市足球联赛 AIGC 创作大赛　IP 形象与设计赛道　系列套图（一）</text>',
        f'<text x="{x0+grid_w}" y="{fy}" font-family="{SANS}" font-size="3.3" fill="{INK_SOFT}" text-anchor="end">JSCL-2026-IP-01　300dpi　SPECIMEN</text>',
    ]
    return html_page(svg_open(W, H) + "<defs>" + "".join(masks) + "</defs>" + "".join(parts) + "</svg>", W, H)


def _bridge(i, x, y, S):
    """三块过桥：说票 / 十三印 / 声明。"""
    W, H = S, S * 1.25
    head = f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER_2}"/><rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="0.12" opacity="0.35"/>'
    if i == 0:
        body = f'''<text x="5" y="16" font-family="{SERIF}" font-size="9.0" fill="{INK}" letter-spacing="1.2">一城</text>
<text x="5" y="27" font-family="{SERIF}" font-size="9.0" fill="{INK}" letter-spacing="1.2">一票</text>
<line x1="5" y1="33" x2="34" y2="33" stroke="{RED}" stroke-width="0.5"/>
<text x="5" y="41" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">球票与邮票是同一件东西：</text>
<text x="5" y="45.6" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">打孔边、编号、日期、副券。</text>
<text x="5" y="52" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">一场一城，一城一票；</text>
<text x="5" y="56.6" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">十三枚齐，走遍江苏。</text>'''
    elif i == 1:
        seals = "".join(seal(4.6 + (k % 4) * 12.2, 14 + (k // 4) * 12.2, 9.6, ABBR[c["id"]])
                        for k, c in enumerate(CITIES))
        body = f'<text x="4.6" y="8.6" font-family="{SANS}" font-size="2.6" fill="{INK_SOFT}" letter-spacing="0.4">十三城 · 十三印</text>' + seals
    else:
        body = f'''<text x="5" y="8.6" font-family="{SANS}" font-size="2.6" fill="{INK_SOFT}" letter-spacing="0.6">SPECIMEN · 非邮资凭证</text>
<text x="5" y="16" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">本版为赛事文创设计样张，</text>
<text x="5" y="20.6" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">不具邮资效力，不作寄递使用。</text>
<text x="5" y="28" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">形象：苏嘟嘟 · 十三太保家族</text>
<text x="5" y="32.6" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">原型长江江豚；鳍为昆曲水袖，</text>
<text x="5" y="37.2" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">肩为倒置茉莉云肩，足踏水波。</text>
<text x="5" y="44.6" font-family="{SANS_M}" font-size="2.9" fill="{INK_SOFT}">简称：宁锡徐常苏通连淮盐扬镇泰宿</text>'''
    return f'<g transform="translate({x},{y})">{head}{body}</g>'
