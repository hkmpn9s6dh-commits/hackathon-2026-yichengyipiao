"""把 13 只人偶统一成「影青」单色釉：保亮度、压低饱和度、向青白偏一点。

判据：处理后在 LAB 里 a/b 的绝对值 ≤ 6（近乎中性），且 13 张的平均色相差 ≤ 3°。
"""
import json, os, sys
import numpy as np, cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUT = os.path.join(ROOT, "assets", "art", "cut")
OUT = os.path.join(ROOT, "assets", "art", "glaze")
SAT = 0.10          # 保留 10% 饱和度
TARGET_B = 3.0      # 轻微偏青（LAB b 轴）


def glaze(path, out):
    im = np.array(Image.open(path).convert("RGBA"))
    rgb, a = im[:, :, :3], im[:, :, 3]
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[:, :, 0] = np.clip((lab[:, :, 0] - 128) * 1.02 + 128 + 2, 0, 255)   # 略提亮
    lab[:, :, 1] = (lab[:, :, 1] - 128) * SAT + 128
    lab[:, :, 2] = (lab[:, :, 2] - 128) * SAT + 128 + TARGET_B
    rgb2 = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    Image.fromarray(np.dstack([rgb2, a]), "RGBA").save(out)
    return rgb2, a


def main():
    os.makedirs(OUT, exist_ok=True)
    cities = json.load(open(os.path.join(ROOT, "data", "cities.json"), encoding="utf-8"))
    stats = []
    for c in cities:
        rgb, a = glaze(os.path.join(CUT, c["id"] + ".png"), os.path.join(OUT, c["id"] + ".png"))
        m = a > 200
        lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)[m]
        stats.append((c["id"], round(float(lab[:, 1].mean() - 128), 2), round(float(lab[:, 2].mean() - 128), 2)))
    for s in stats:
        print("%-12s a=%5.2f b=%5.2f" % s)
    print("max |a| =", max(abs(s[1]) for s in stats), " max |b| =", max(abs(s[2]) for s in stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
