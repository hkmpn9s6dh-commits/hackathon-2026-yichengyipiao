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
        p.append(f'<g transform="translate({x0 + k*60},{top + 116}) rotate({[-2,0,2][k]})">'
                 f'<g transform="scale(0.94)">{D.stamp(CITIES[idx], 60, f"ps{k}", fill=PAPER)}</g></g>')
    p.append(f'<text x="{x0}" y="{top + 196}" font-family="{SANS_M}" font-size="4.4" fill="#BDB6A4" letter-spacing="0.3">苏州 · 盐城 · 宿迁　同版式延展样本</text>')

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
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" filter="url(#grain)" opacity="0.05"/>')
    defs = ("<defs>"
            + "".join(D.perf_mask(60, 75, f"ps{i}") for i in range(3))
            + D.perf_mask(150, 187.5, "ph")
            + '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.2"/></filter>'
            + '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>'
            + "</defs>")
    return D.html_page(D.svg_open(W, H) + defs + "".join(p) + "</svg>", W, H)


def passport():
    W, H = 297.0, 210.0
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>']
    p.append(f'<rect x="146" y="0" width="5" height="{H}" fill="#000" opacity="0.05"/>')
    p.append(f'<line x1="148.5" y1="0" x2="148.5" y2="{H}" stroke="{INK}" stroke-width="0.15" opacity="0.25"/>')
    p += [
        f'<text x="22" y="26" font-family="{SANS_M}" font-size="3.4" fill="{INK_SOFT}" letter-spacing="1.6">JIANGSU CITY FOOTBALL LEAGUE</text>',
        f'<text x="20" y="58" font-family="{SERIF}" font-size="24" fill="{INK}" letter-spacing="2.2">观赛护照</text>',
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
        row = i // 5
        n_in_row = min(5, len(CITIES) - row * 5)
        col = i % 5
        row_w = (n_in_row - 1) * 25.4 + 17.2
        x = 22 + (144 - row_w) / 2 + col * 25.4
        y = 142 + row * 25
        p.append(f'<circle cx="{x+9}" cy="{y+8}" r="8.6" fill="none" stroke="{RED}" stroke-width="0.5" opacity="0.8"/>')
        p.append(f'<circle cx="{x+9}" cy="{y+8}" r="7.4" fill="none" stroke="{RED}" stroke-width="0.22" opacity="0.5"/>')
        p.append(f'<text x="{x+9}" y="{y+5.6}" font-family="{SANS_M}" font-size="2.0" fill="{RED}" text-anchor="middle" opacity="0.9">{c["name"]}</text>')
        p.append(f'<text x="{x+9}" y="{y+10.4}" font-family="{SERIF}" font-size="5.8" fill="{RED}" text-anchor="middle">{ABBR[c["id"]]}</text>')
        p.append(f'<text x="{x+9}" y="{y+14.2}" font-family="{SANS}" font-size="1.7" fill="{RED}" text-anchor="middle" opacity="0.75">2026</text>')
    p += [
        f'<text x="168" y="26" font-family="{SERIF}" font-size="9.4" fill="{INK}" letter-spacing="1.4">十三轮 · 观赛记录</text>',
        f'<text x="168" y="34" font-family="{SANS}" font-size="3.1" fill="{INK_SOFT}" letter-spacing="1.4">THIRTEEN MATCHDAYS</text>',
        f'<line x1="168" y1="42" x2="276" y2="42" stroke="{INK}" stroke-width="0.5" opacity="0.55"/>',
    ]
    for t, x in [("轮次", 168), ("主场", 182), ("日期", 214), ("比分", 240), ("盖章", 262)]:
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
        p.append(D.seal(262, y - 6.2, 6.2, ABBR[c["id"]], opacity=0.32))
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
        p.append(f'<rect x="1.2" y="1.8" width="{cw}" height="{ch}" rx="2.2" fill="#000" opacity="0.22"/>')
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
        f'<text x="20" y="180" font-family="{SANS_M}" font-size="3.3" fill="#A9A392" letter-spacing="0.4">系列套图（四）　收藏卡牌 63×88mm（标准扑克尺寸）　300dpi　JSCL-2026-IP-04</text>',
    ]
    defs = "<defs>" + "".join(f'<clipPath id="cc{k}"><rect x="0" y="0" width="63" height="52"/></clipPath>' for k in range(3)) + "</defs>"
    return D.html_page(D.svg_open(W, H) + defs + "".join(p) + "</svg>", W, H)


def postcards():
    """A4 横：一张明信片的正面与背面（105×148mm，标准 10×15）。"""
    W, H = 297.0, 210.0
    cw, ch = 105.0, 148.0
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{PAPER}"/>']
    # ---- 正面
    fx, fy = 26.0, 30.0
    c = CITIES[0]
    p.append(f'<g transform="translate({fx},{fy})">')
    p.append(f'<rect x="1.4" y="2.0" width="{cw}" height="{ch}" fill="#000" opacity="0.16"/>')
    p.append(f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="{D.mix(PAPER_2, c["color"], 0.16)}"/>')
    p.append(f'<clipPath id="pcf"><rect x="0" y="0" width="{cw}" height="112"/></clipPath>')
    p.append(f'<g clip-path="url(#pcf)">{D.figure(c, 0, 2, cw, 108)}</g>')
    p.append(f'<rect x="4" y="4" width="{cw-8}" height="104" fill="none" stroke="{INK}" stroke-width="0.25" opacity="0.4"/>')
    p.append(f'<text x="6" y="12" font-family="{SANS_M}" font-size="3.0" fill="{INK_SOFT}" letter-spacing="1.2">江苏 · 南京</text>')
    p.append(f'<line x1="0" y1="112" x2="{cw}" y2="112" stroke="{INK}" stroke-width="0.4" opacity="0.6"/>')
    p.append(f'<text x="6" y="126" font-family="{SERIF}" font-size="15.0" fill="{INK}" letter-spacing="1.4">南京</text>')
    p.append(f'<text x="6" y="132" font-family="{SANS_M}" font-size="3.2" fill="{INK_SOFT}" letter-spacing="0.9">NANJING</text>')
    p.append(f'<text x="6" y="142" font-family="{SERIF}" font-size="5.2" fill="{D.ink_of(c["color"])}" letter-spacing="0.6">鸭力全开</text>')
    p.append(D.seal(cw - 15.0, 116.0, 10.0, ABBR[c["id"]]))
    p.append('</g>')
    # ---- 背面
    bx, by = 166.0, 30.0
    p.append(f'<g transform="translate({bx},{by})">')
    p.append(f'<rect x="1.4" y="2.0" width="{cw}" height="{ch}" fill="#000" opacity="0.16"/>')
    p.append(f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="#FBF7EC"/>')
    p.append(f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="none" stroke="{INK}" stroke-width="0.25" opacity="0.35"/>')
    # 邮票位
    p.append(f'<rect x="{cw-26}" y="8" width="20" height="24" fill="none" stroke="{INK}" stroke-width="0.3" stroke-dasharray="1.2 1.0" opacity="0.55"/>')
    p.append(f'<text x="{cw-16}" y="21" font-family="{SANS_M}" font-size="2.4" fill="{INK_SOFT}" text-anchor="middle">贴邮票处</text>')
    # 邮编框
    for i in range(6):
        x = cw - 74 + i * 7.2
        p.append(f'<rect x="{x}" y="8" width="6.2" height="7.4" fill="none" stroke="{RED}" stroke-width="0.25" opacity="0.75"/>')
    p.append(f'<text x="{cw-74}" y="6.4" font-family="{SANS}" font-size="2.2" fill="{INK_SOFT}" letter-spacing="0.3">邮政编码</text>')
    # 分隔竖线
    p.append(f'<line x1="58" y1="8" x2="58" y2="{ch-10}" stroke="{INK}" stroke-width="0.25" opacity="0.35"/>')
    # 收件人
    for i, t in enumerate(["收", "件", "人"]):
        p.append(f'<text x="62" y="{22 + i*11}" font-family="{SANS_M}" font-size="3.0" fill="{INK_SOFT}">{t}</text>')
        p.append(f'<line x1="68" y1="{23 + i*11}" x2="{cw-6}" y2="{23 + i*11}" stroke="{INK}" stroke-width="0.2" opacity="0.28"/>')
    # 左侧：一句话
    p.append(f'<text x="6" y="16" font-family="{SERIF}" font-size="6.0" fill="{INK}" letter-spacing="0.6">一城一票</text>')
    p.append(f'<text x="6" y="22" font-family="{SANS}" font-size="2.4" fill="{INK_SOFT}" letter-spacing="1.0">ONE CITY, ONE TICKET</text>')
    p.append(f'<line x1="6" y1="26" x2="52" y2="26" stroke="{RED}" stroke-width="0.4"/>')
    p.append(f'<text x="6" y="34" font-family="{SANS_M}" font-size="2.7" fill="{INK_SOFT}">十三座城市，十三张票。</text>')
    p.append(f'<text x="6" y="38.4" font-family="{SANS_M}" font-size="2.7" fill="{INK_SOFT}">球票与邮票是同一件东西：</text>')
    p.append(f'<text x="6" y="42.8" font-family="{SANS_M}" font-size="2.7" fill="{INK_SOFT}">打孔边、编号、日期、副券。</text>')
    p.append(D.seal(6, 50, 9.0, "宁"))
    p.append(f'<text x="6" y="{ch-16}" font-family="{SANS_M}" font-size="2.4" fill="{INK_SOFT}">寄件人</text>')
    p.append(f'<line x1="6" y1="{ch-14}" x2="52" y2="{ch-14}" stroke="{INK}" stroke-width="0.2" opacity="0.28"/>')
    p.append(f'<text x="6" y="{ch-8}" font-family="{SANS}" font-size="2.1" fill="{INK_SOFT}" opacity="0.7">JSCL · 2026 · SPECIMEN 非卖品</text>')
    p.append('</g>')
    # 说明
    p += [
        f'<text x="26" y="192" font-family="{SERIF}" font-size="4.6" fill="{INK}" letter-spacing="0.5">明信片 105×148mm（标准 10×15）：正面用同一枚票的画面语言，背面留邮政栏位与邮票位。</text>',
        f'<text x="26" y="200" font-family="{SANS_M}" font-size="3.2" fill="{INK_SOFT}">系列套图（五）　JSCL-2026-IP-05　300dpi　本页为非卖品样张，不具邮资效力。</text>',
    ]
    return D.html_page(D.svg_open(W, H) + "".join(p) + "</svg>", W, H)
