"""《一城一票》其余三件：主海报、观赛护照、收藏卡牌。"""
import design as D

CITIES, ABBR = D.CITIES, D.ABBR
PAPER, PAPER_2, INK, INK_SOFT, RED, DEEP = D.PAPER, D.PAPER_2, D.INK, D.INK_SOFT, D.RED, D.DEEP
SERIF, SANS, SANS_M = D.SERIF, D.SANS, D.SANS_M


def poster():
    """A2 主视觉：左一张主票，右一段设计说明，底部十三印排成一条带。"""
    import textfit as tf
    W, H = 420.0, 594.0
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{DEEP}"/>']
    for i in range(16):
        if i % 2 == 0:
            p.append(f'<rect x="{i*26.5}" y="0" width="26.5" height="{H}" fill="#FFFFFF" opacity="0.018"/>')

    title, t_pt = "一城一票", 70.0
    t_w = tf.width_mm(title, tf.F_SERIF, t_pt, 3.0)
    p += [
        f'<text x="34" y="44" font-family="{SANS_M}" font-size="4.6" fill="#D8D2C2" letter-spacing="2.2" opacity="0.85">江苏省城市足球联赛　AIGC 创作大赛　IP 形象与设计</text>',
        f'<text x="32" y="{44 + t_pt * 0.92 + 34}" font-family="{SERIF}" font-size="{t_pt}" fill="{PAPER}" letter-spacing="3">一城一票</text>',
        f'<text x="36" y="{44 + t_pt * 0.92 + 34 + 26}" font-family="{SANS}" font-size="8.4" fill="#C9C3B2" letter-spacing="6.4">ONE CITY, ONE TICKET</text>',
        f'<line x1="34" y1="{44 + t_pt * 0.92 + 34 + 44}" x2="386" y2="{44 + t_pt * 0.92 + 34 + 44}" stroke="{PAPER}" stroke-width="0.6" opacity="0.35"/>',
    ]
    base = 44 + t_pt * 0.92 + 34 + 44
    p += [
        f'<text x="36" y="{base + 24}" font-family="{SERIF}" font-size="9.6" fill="{PAPER}">十三座城市，十三张票。球票与邮票本是同一件东西——打孔边、编号、日期、副券。</text>',
        f'<text x="36" y="{base + 40}" font-family="{SERIF}" font-size="9.6" fill="{PAPER}">每赴一城，得一枚；十三枚齐，即为通关。</text>',
    ]

    # 主票
    top = base + 60
    p.append(f'<g transform="translate(34,{top}) rotate(-2.5)">'
             '<rect x="2" y="3" width="150" height="187.5" fill="#000" opacity="0.42" filter="url(#soft)"/>'
             f'{D.stamp(CITIES[0], 150, "ph", fill=PAPER)}</g>')

    # 右栏：设计说明
    x0 = 212
    p += [
        f'<text x="{x0}" y="{top + 6}" font-family="{SANS_M}" font-size="3.6" fill="#A9A392" letter-spacing="1.4">设计说明 / NOTE</text>',
        f'<line x1="{x0}" y1="{top + 12}" x2="386" y2="{top + 12}" stroke="{PAPER}" stroke-width="0.4" opacity="0.3"/>',
    ]
    note = [
        ("一票两读", "球票是进场，邮票是寄出。同一个物件，两种抵达。"),
        ("十三城", "十三座主场城市，十三位「嘟嘟」；同一只江豚，各戴各的冠。"),
        ("影青一色", "人偶统一为影青釉，只让朱印与口号带出城市色。"),
        ("可收集", "打孔边、编号、副券俱全；十三枚成册，即观赛护照。"),
    ]
    ny = top + 24
    for head, body in note:
        p.append(f'<text x="{x0}" y="{ny}" font-family="{SERIF}" font-size="6.2" fill="{PAPER}" letter-spacing="0.8">{head}</text>')
        p.append(f'<text x="{x0}" y="{ny+7.8}" font-family="{SANS_M}" font-size="4.0" fill="#B9B3A2">{body}</text>')
        ny += 21
    # 系列其余三张，横排做样本
    for k, idx in enumerate([4, 8, 12]):
        p.append(f'<g transform="translate({x0 + k*58},{top + 120}) rotate({[-2,0,2][k]})">'
                 f'<g transform="scale(0.9)">{D.stamp(CITIES[idx], 60, f"ps{k}", fill=PAPER)}</g></g>')
    p.append(f'<text x="{x0}" y="{top + 192}" font-family="{SANS_M}" font-size="3.6" fill="#A9A392">苏州 · 盐城 · 宿迁　（同版式延展样本）</text>')

    # 底部十三印
    by = 470
    p.append(f'<line x1="34" y1="{by-14}" x2="386" y2="{by-14}" stroke="{PAPER}" stroke-width="0.4" opacity="0.28"/>')
    for i, c in enumerate(CITIES):
        cx = 36 + i * 27.2
        p.append(D.seal(cx, by, 15.4, ABBR[c["id"]], color="#C0473C", opacity=1.0))
        p.append(f'<text x="{cx+7.7}" y="{by+21.4}" font-family="{SANS_M}" font-size="3.4" fill="#CFC9B8" text-anchor="middle">{c["name"]}</text>')
    p += [
        f'<line x1="34" y1="546" x2="386" y2="546" stroke="{PAPER}" stroke-width="0.4" opacity="0.3"/>',
        f'<text x="36" y="562" font-family="{SANS_M}" font-size="4.8" fill="#A9A392">系列套图（二）　主视觉海报　A2 / 420×594mm / 300dpi</text>',
        f'<text x="384" y="562" font-family="{SANS}" font-size="4.8" fill="#A9A392" text-anchor="end">JSCL-2026-IP-02</text>',
    ]
    defs = ("<defs>"
            + "".join(D.perf_mask(60, 75, f"ps{i}") for i in range(3))
            + D.perf_mask(150, 187.5, "ph")
            + '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>'
            + "</defs>")
    return D.html_page(D.svg_open(W, H) + defs + "".join(p) + "</svg>", W, H)


def passport():
    W, H = 297.0, 210.0
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>']
    p.append(f'<rect x="146" y="0" width="5" height="{H}" fill="#000" opacity="0.05"/>')
    p.append(f'<line x1="148.5" y1="0" x2="148.5" y2="{H}" stroke="{INK}" stroke-width="0.15" opacity="0.25"/>')
    p += [
        f'<text x="22" y="26" font-family="{SANS_M}" font-size="3.4" fill="{INK_SOFT}" letter-spacing="1.6">JIANGSU CITY FOOTBALL LEAGUE</text>',
        f'<text x="20" y="58" font-family="{SERIF}" font-size="24" fill="{INK}" letter-spacing="2.2">觀賽護照</text>',
        f'<text x="22" y="70" font-family="{SANS}" font-size="4.0" fill="{INK_SOFT}" letter-spacing="3.0">MATCH PASSPORT</text>',
        f'<line x1="22" y1="78" x2="128" y2="78" stroke="{RED}" stroke-width="0.7"/>',
        f'<text x="22" y="88" font-family="{SANS_M}" font-size="3.4" fill="{INK_SOFT}">持照人 / HOLDER</text>',
        f'<line x1="22" y1="98" x2="128" y2="98" stroke="{INK}" stroke-width="0.3" opacity="0.45"/>',
        f'<text x="22" y="108" font-family="{SANS_M}" font-size="3.4" fill="{INK_SOFT}">编号 / NO.</text>',
        f'<line x1="60" y1="109" x2="128" y2="109" stroke="{INK}" stroke-width="0.25" opacity="0.4"/>',
        f'<text x="22" y="120" font-family="{SANS_M}" font-size="3.3" fill="{INK_SOFT}">本护照用于收集十三座主场城市之邮戳。</text>',
        f'<text x="22" y="126" font-family="{SANS_M}" font-size="3.3" fill="{INK_SOFT}">每赴一城，盖一印；十三枚齐，即为通关。</text>',
    ]
    for i, c in enumerate(CITIES):
        col, row = i % 5, i // 5
        x = 22 + col * 25.4
        y = 142 + row * 25
        p.append(f'<circle cx="{x+9}" cy="{y+8}" r="8.6" fill="none" stroke="{c["color"]}" stroke-width="0.45" opacity="0.85"/>')
        p.append(f'<text x="{x+9}" y="{y+5.2}" font-family="{SANS_M}" font-size="2.1" fill="{c["color"]}" text-anchor="middle">{c["name"]}</text>')
        p.append(f'<text x="{x+9}" y="{y+9.4}" font-family="{SERIF}" font-size="5.6" fill="{c["color"]}" text-anchor="middle">{ABBR[c["id"]]}</text>')
        p.append(f'<line x1="{x+3}" y1="{y+12.6}" x2="{x+15}" y2="{y+12.6}" stroke="{c["color"]}" stroke-width="0.25" opacity="0.55"/>')
    p += [
        f'<text x="168" y="26" font-family="{SERIF}" font-size="9.4" fill="{INK}" letter-spacing="1.4">十三輪 · 觀賽記錄</text>',
        f'<text x="168" y="34" font-family="{SANS}" font-size="3.1" fill="{INK_SOFT}" letter-spacing="1.4">THIRTEEN MATCHDAYS</text>',
        f'<line x1="168" y1="42" x2="276" y2="42" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>',
    ]
    for t, x in [("輪次", 168), ("主場", 182), ("日期", 214), ("比分", 240), ("蓋章", 262)]:
        p.append(f'<text x="{x}" y="50" font-family="{SANS_M}" font-size="3.0" fill="{INK_SOFT}">{t}</text>')
    for i, c in enumerate(CITIES):
        y = 60 + i * 10.4
        if i % 2 == 0:
            p.append(f'<rect x="166" y="{y-4.2}" width="112" height="10.4" fill="#000" opacity="0.022"/>')
        p.append(f'<text x="168" y="{y}" font-family="{SANS}" font-size="3.0" fill="{INK_SOFT}">{c["no"]:02d}</text>')
        p.append(f'<text x="182" y="{y}" font-family="{SANS_M}" font-size="3.3" fill="{INK}">{c["name"]}</text>')
        p.append(f'<text x="195" y="{y}" font-family="{SANS}" font-size="2.4" fill="{INK_SOFT}">{c["dudu"]}</text>')
        p.append(f'<line x1="214" y1="{y-0.7}" x2="236" y2="{y-0.7}" stroke="{INK}" stroke-width="0.2" opacity="0.3"/>')
        p.append(f'<line x1="240" y1="{y-0.7}" x2="256" y2="{y-0.7}" stroke="{INK}" stroke-width="0.2" opacity="0.3"/>')
        p.append(D.seal(262, y - 6.2, 6.2, ABBR[c["id"]], opacity=0.3))
    p.append(f'<text x="168" y="202" font-family="{SANS_M}" font-size="2.8" fill="{INK_SOFT}">观赛护照内页样张 · 非卖品 · 形象：苏嘟嘟 · 十三太保家族</text>')
    return D.html_page(D.svg_open(W, H) + "".join(p) + "</svg>", W, H)


def cards():
    W, H = 297.0, 210.0
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{DEEP}"/>']
    for i in range(12):
        if i % 2 == 0:
            p.append(f'<rect x="{i*26}" y="0" width="26" height="{H}" fill="#FFFFFF" opacity="0.016"/>')
    p += [
        f'<text x="20" y="24" font-family="{SANS_M}" font-size="3.4" fill="#CFC9B8" letter-spacing="1.8">CITY CARD SERIES　·　十三城收藏卡</text>',
        f'<text x="20" y="41" font-family="{SERIF}" font-size="9.0" fill="{PAPER}" letter-spacing="1.4">一城一票 · 城市卡</text>',
    ]
    cw, ch = 63.0, 88.0
    for k, idx in enumerate([0, 4, 8]):
        c = CITIES[idx]
        p.append(f'<g transform="translate({22 + k * 88},{56})">')
        p.append(f'<rect x="1.6" y="2.4" width="{cw}" height="{ch}" rx="2.2" fill="#000" opacity="0.35"/>')
        p.append(f'<rect x="0" y="0" width="{cw}" height="{ch}" rx="2.2" fill="{PAPER}"/>')
        p.append(f'<path d="M0,2.2 a2.2,2.2 0 0 1 2.2,-2.2 h{cw-4.4} a2.2,2.2 0 0 1 2.2,2.2 v49.8 h{-cw} z" fill="{D.mix(PAPER_2, c["color"], 0.16)}"/>')
        p.append(f'<g clip-path="url(#cc{k})">{D.figure(c, 0, 1.2, cw, 50.5)}</g>')
        p.append(f'<rect x="3.2" y="3.2" width="{cw-6.4}" height="45.4" fill="none" stroke="{INK}" stroke-width="0.2" opacity="0.45"/>')
        p.append(f'<text x="3.6" y="60.8" font-family="{SERIF}" font-size="11.4" fill="{INK}" letter-spacing="0.8">{c["name"]}</text>')
        p.append(f'<text x="3.8" y="64.6" font-family="{SANS_M}" font-size="2.6" fill="{INK_SOFT}" letter-spacing="0.5">{c["pinyin"]}</text>')
        p.append(D.seal(cw - 12.4, 49.6, 9.2, ABBR[c["id"]]))
        p.append(f'<text x="3.6" y="70.8" font-family="{SERIF}" font-size="4.5" fill="{D.ink_of(c["color"])}" letter-spacing="0.5">{c["slogan"]}</text>')
        p.append(f'<line x1="3.2" y1="74.2" x2="{cw-3.2}" y2="74.2" stroke="{INK}" stroke-width="0.2" opacity="0.3"/>')
        p.append(f'<text x="3.6" y="78.2" font-family="{SANS_M}" font-size="2.5" fill="{INK_SOFT}">{c["dudu"]} · {c["totem"]}</text>')
        p.append(f'<text x="{cw-3.6}" y="78.2" font-family="{SANS}" font-size="2.5" fill="{INK_SOFT}" text-anchor="end">{c["no"]:02d}/13</text>')
        p.append(f'<text x="3.6" y="83.6" font-family="{SANS}" font-size="2.1" fill="{INK_SOFT}" opacity="0.75">CITY CARD · 2026 · NON-SALE SAMPLE</text>')
        p.append('</g>')
    p += [
        f'<text x="20" y="168" font-family="{SERIF}" font-size="4.8" fill="#CFC9B8" letter-spacing="0.6">统一版式：上为影青釉人偶，下为城市名、朱印与口号；同一套栅格可延展至明信片、杯壶与毛绒吊牌。</text>',
        f'<text x="20" y="180" font-family="{SANS_M}" font-size="3.3" fill="#A9A392" letter-spacing="0.4">系列套图（三）　收藏卡牌 63×88mm（标准扑克尺寸）　300dpi　JSCL-2026-IP-03</text>',
    ]
    defs = "<defs>" + "".join(f'<clipPath id="cc{k}"><rect x="0" y="0" width="63" height="52"/></clipPath>' for k in range(3)) + "</defs>"
    return D.html_page(D.svg_open(W, H) + defs + "".join(p) + "</svg>", W, H)
