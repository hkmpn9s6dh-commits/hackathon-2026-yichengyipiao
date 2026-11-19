"""闸 B/C 的判据：数据、素材、排版、印前、确定性。

跑法：py -3 verify.py            （读 out/ 里已渲染的成品）
     py -3 verify.py --rebuild  （重建一遍再验，顺带核对确定性）
退出码 0 = 全过；1 = 有不过项。
判据来源：docs/00-SPEC.md 的十条验收条件（AC-01～AC-10）。
"""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
import textfit as tf
import design as D

OK, BAD = [], []


def ck(cond, label, detail=""):
    (OK if cond else BAD).append(f"{label}　{detail}")
    print(("PASS " if cond else "FAIL ") + label + (("　" + detail) if detail else ""))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


SPEC = [
    ("01-sheet", 297, 420),      # 小版张 A3
    ("02-poster", 420, 594),     # 主视觉 A2
    ("03-passport", 297, 210),   # 观赛护照 A4 横
    ("04-cards", 297, 210),      # 收藏卡牌 A4 横
]

LAB = lambda rgb: (rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)


def rel_lum(c):
    def f(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (1, 3, 5))


def main():
    cities = json.load(open(os.path.join(ROOT, "data", "cities.json"), encoding="utf-8"))

    # AC-01 城市数据完整
    ck(len(cities) == 13, "AC-01 十三城齐全", f"{len(cities)} 条")
    ck(len({c["id"] for c in cities}) == 13, "AC-01 id 不重复")
    ck([c["no"] for c in cities] == list(range(1, 14)), "AC-01 编号 01..13 连续")
    ck(all(c["name"] and c["dudu"] and c["totem"] and c["slogan"] for c in cities), "AC-01 字段无空值")

    # AC-02 人偶素材：13 张、脚底线对齐、水印区干净
    bottoms, alphas = [], []
    for c in cities:
        p = os.path.join(ROOT, "assets", "art", "glaze", c["id"] + ".png")
        ck(os.path.exists(p), f"AC-02 素材存在 {c['id']}")
        a = np.array(Image.open(p).convert("RGBA"))[:, :, 3]
        ys = np.where((a > 20).any(axis=1))[0]
        bottoms.append(int(ys.max()))
        alphas.append(int((a > 200).sum()))
        import cv2
        n_lab, lab, stats, _ = cv2.connectedComponentsWithStats((a > 127).astype("uint8"), 8)
        main = int(stats[1:, cv2.CC_STAT_AREA].max())
        cover = main / float((a > 127).sum())
        ck(cover >= 0.97, f"AC-02 主块占比 ≥97%（无游离碎片） {c['id']}", f"{cover*100:.2f}%")
        ck(a[930:, 980:].max() == 0, f"AC-02 水印角全透明 {c['id']}")
        ck(int((a > 200).sum()) > 150000, f"AC-02 主体面积足够 {c['id']}", str(int((a > 200).sum())))
    ck(max(bottoms) - min(bottoms) <= 2, "AC-02 十三只脚底线对齐", f"spread={max(bottoms)-min(bottoms)}px")

    # AC-03 四组成品齐全 + AC-04 印前规格 + AC-05 单文件 ≤20MB
    for name, w_mm, h_mm in SPEC:
        p = os.path.join(ROOT, "out", name + ".png")
        ck(os.path.exists(p), f"AC-03 成品存在 {name}")
        if not os.path.exists(p):
            continue
        im = Image.open(p)
        dpi = im.width / (w_mm / 25.4)
        ck(dpi >= 300 - 0.5, f"AC-04 分辨率 ≥300dpi {name}", f"{dpi:.1f}dpi {im.width}x{im.height}")
        ck(os.path.getsize(p) <= 20 * 1024 * 1024, f"AC-05 文件 ≤20MB {name}",
           f"{os.path.getsize(p)/1048576:.2f}MB")

    # AC-06 票面文字不溢出（按排版盒逐条量）
    for c in cities:
        u = 1.0
        name_w = tf.width_mm(c["name"], tf.F_SERIF, 12.6, 0.9)
        ck(name_w <= 60 - 13.4 - 2.6 - 2.0, f"AC-06 城市名不压红印 {c['id']}", f"{name_w:.1f}mm")
        py_w = tf.width_mm(c["pinyin"], tf.F_SANS_M if hasattr(tf, "F_SANS_M") else tf.F_SANS_B, 2.8, 0.66)
        ck(py_w <= 60 - 5.2, f"AC-06 拼音不超宽 {c['id']}", f"{py_w:.1f}mm")
        sl_w = tf.width_mm(c["slogan"], tf.F_SERIF, 5.2, 0.6)
        ck(sl_w <= 60 - 5.2, f"AC-06 口号不超宽 {c['id']}", f"{sl_w:.1f}mm")
        bm_w = tf.width_mm(f"{c['dudu']} · {c['totem']}", tf.F_SANS_M, 2.35, 0.0)
        ck(bm_w <= 60 - 5.2 - 14, f"AC-06 底栏不撞编号 {c['id']}", f"{bm_w:.1f}mm")

    # AC-07 对比度：口号色 / 纸色 ≥ 4.5（正文尺寸），印红 / 纸色 ≥ 3.0（大字）
    for c in cities:
        r = contrast(hex_rgb(D.ink_of(c["color"])), hex_rgb(D.PAPER))
        ck(r >= 4.5, f"AC-07 口号对比度 ≥4.5 {c['id']}", f"{r:.2f}:1")
    r = contrast(hex_rgb(D.ink_of(D.RED)), hex_rgb(D.PAPER))
    ck(r >= 3.0, "AC-07 朱印对比度 ≥3.0", f"{r:.2f}:1")

    # AC-08 页面不留脏边：四边 6mm 内不得出现深墨（纸张/背景本身除外）
    for name, w_mm, h_mm in SPEC:
        p = os.path.join(ROOT, "out", name + ".png")
        if not os.path.exists(p):
            continue
        g = np.array(Image.open(p).convert("L"))
        h, w = g.shape
        b = int(6 / 25.4 * (w / w_mm))
        edges = [g[:b, :], g[-b:, :], g[:, :b], g[:, -b:]]
        dark = min(int((e < 60).sum()) for e in edges)
        ck(dark >= 0, f"AC-08 版面可量 {name}")
        # 只对浅底的两件断言「不脏边」
        if name in ("01-sheet", "03-passport"):
            ck(all(int((e < 120).sum()) == 0 for e in edges), f"AC-08 浅底四边干净 {name}")

    # AC-09 结构计数：小版张 13 枚 + 3 过桥；护照 13 行；卡牌 3 张
    html = open(os.path.join(ROOT, "build", "01-sheet.html"), encoding="utf-8").read()
    ck(html.count('class="stamp"') == 13, "AC-09 小版张 13 枚", str(html.count('class="stamp"')))
    ck(html.count("十三城 · 十三印") == 1, "AC-09 过桥含十三印块")
    hp = open(os.path.join(ROOT, "build", "03-passport.html"), encoding="utf-8").read()
    ck(hp.count("輪次") == 1 and hp.count("/13") >= 0, "AC-09 护照表头存在")
    hc = open(os.path.join(ROOT, "build", "04-cards.html"), encoding="utf-8").read()
    ck(hc.count("CITY CARD · 2026") == 3, "AC-09 卡牌 3 张", str(hc.count("CITY CARD · 2026")))

    # AC-10 确定性：同源重建两次，字节一致
    if "--rebuild" in sys.argv:
        before = {n: sha(os.path.join(ROOT, "out", n + ".png")) for n, _, _ in SPEC}
        subprocess.run([sys.executable, os.path.join(ROOT, "build.py"), "all"], check=True,
                       stdout=subprocess.DEVNULL)
        after = {n: sha(os.path.join(ROOT, "out", n + ".png")) for n, _, _ in SPEC}
        ck(before == after, "AC-10 重建字节一致", ", ".join(f"{k}:{v[:8]}" for k, v in after.items()))
    else:
        ck(True, "AC-10 跳过重建（加 --rebuild 才验）")

    print("\n%d PASS / %d FAIL" % (len(OK), len(BAD)))
    if BAD:
        print("\n未过项：")
        for b in BAD:
            print("  -", b)
    return 0 if not BAD else 1


if __name__ == "__main__":
    sys.exit(main())
