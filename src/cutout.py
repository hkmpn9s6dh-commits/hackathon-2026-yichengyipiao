"""剪影化 13 张城市形象：去背、去水印、按「脚底中心」对齐到同一画布。

判据（verify.py 会复核）：
  - 每张 alpha 的连通域只有一个（不许留下孤立碎块）
  - 脚底中心对齐后，13 张的 bbox 底边落在同一行（±2 px）
  - 水印区域（右下角 890,915 起）alpha 全 0
"""
import json, os, sys
import numpy as np, cv2
from PIL import Image
from io_util import read_bgr, write_rgba

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "assets", "art")
OUT = os.path.join(ART, "cut")
CANVAS = 1200
FOOT_Y = 1080
CENTER_X = 600
WM = (885, 905)          # 水印区域左上角 (x, y)


def cut_one(path):
    im = read_bgr(path)
    h, w = im.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE
    seeds = [(3, 3), (3, w - 4), (h - 4, 3), (h - 4, w - 4),
             (3, w // 2), (h - 4, w // 2), (h // 2, 3), (h // 2, w - 4)]
    for y, x in seeds:
        m = mask.copy()
        cv2.floodFill(im.copy(), m, (x, y), 255, (10, 10, 10), (10, 10, 10), flags)
        mask = np.maximum(mask, m)
    bg = mask[1:-1, 1:-1]
    alpha = ((1 - bg) * 255).astype(np.uint8)

    # 水印一律抹掉（背景部分，不属于作品）
    alpha[WM[1]:, WM[0]:] = 0

    # 只保留最大连通域，去掉零星噪点
    n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 20).astype(np.uint8), 8)
    if n > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        alpha = np.where(lab == biggest, alpha, 0).astype(np.uint8)

    # 收 1px 去白边，再羽化 1.2px
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8), iterations=1)
    alpha = cv2.GaussianBlur(alpha, (5, 5), 1.2)
    alpha[WM[1]:, WM[0]:] = 0          # 羽化会把它再洇回来，抹第二次

    ys, xs = np.where(alpha > 20)
    y_bottom = int(ys.max())
    band = xs[(ys > y_bottom - 30)]
    x_center = int(band.mean())

    canvas = np.zeros((CANVAS, CANVAS, 4), np.uint8)
    dy, dx = FOOT_Y - y_bottom, CENTER_X - x_center
    ys2, xs2 = ys + dy, xs + dx
    ok = (ys2 >= 0) & (ys2 < CANVAS) & (xs2 >= 0) & (xs2 < CANVAS)
    canvas[ys2[ok], xs2[ok], :3] = im[ys[ok], xs[ok], :]
    canvas[ys2[ok], xs2[ok], 3] = alpha[ys[ok], xs[ok]]
    return canvas


def main():
    cities = json.load(open(os.path.join(ROOT, "data", "cities.json"), encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    report = []
    for c in cities:
        src = os.path.join(ART, "city", c["id"] + ".png")
        out = os.path.join(OUT, c["id"] + ".png")
        canvas = cut_one(src)
        write_rgba(out, canvas)
        ys, xs = np.where(canvas[:, :, 3] > 20)
        report.append((c["id"], int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    for r in report:
        print("%-12s x[%4d,%4d] y[%4d,%4d]  h=%d" % (r[0], r[1], r[2], r[3], r[4], r[4] - r[3]))
    bottoms = [r[4] for r in report]
    print("bottom spread:", max(bottoms) - min(bottoms), "px")
    return 0 if max(bottoms) - min(bottoms) <= 2 else 1


if __name__ == "__main__":
    sys.exit(main())
