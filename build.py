"""构建全部版面：生成 HTML -> Chromium 按 300dpi 截图。"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
import design
import design2

BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "out")
DPI = 300
SHOT = os.path.join(ROOT, "src", "shot.mjs")
NODE = "node"


def render(name, html, w_mm, h_mm):
    os.makedirs(BUILD, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    hp = os.path.join(BUILD, name + ".html")
    open(hp, "w", encoding="utf-8").write(html)
    w_px = round(w_mm / 25.4 * 96)
    h_px = round(h_mm / 25.4 * 96)
    scale = DPI / 96.0
    png = os.path.join(OUT, name + ".png")
    url = "file:///" + hp.replace("\\", "/")
    subprocess.run([NODE, SHOT, url, png, str(w_px), str(h_px), f"{scale:.6f}"], check=True)
    print(f"  {name}: {w_px*scale:.0f}x{h_px*scale:.0f}px @{DPI}dpi")
    return png


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = {}
    if which in ("all", "sheet"):
        jobs["01-sheet"] = (design.sheet, 297, 420)
    if which in ("all", "poster"):
        jobs["02-poster"] = (design2.poster, 420, 594)
    if which in ("all", "passport"):
        jobs["03-passport"] = (design2.passport, 297, 210)
    if which in ("all", "cards"):
        jobs["04-cards"] = (design2.cards, 297, 210)
    if which in ("all", "postcard"):
        jobs["05-postcard"] = (design2.postcards, 297, 210)
    for name, (fn, w, h) in jobs.items():
        print("render", name)
        render(name, fn(), w, h)


if __name__ == "__main__":
    main()
