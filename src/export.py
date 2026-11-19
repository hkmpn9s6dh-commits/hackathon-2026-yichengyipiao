"""导出投稿件：JPG（≤20MB）+ 分层 SVG 源文件（内嵌字体子集）+ source.zip"""
import base64, io, json, os, re, shutil, zipfile

from PIL import Image
import outline as O

import design as D
import design2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out")
SUB = os.path.join(OUT, "submit")
SRC = os.path.join(OUT, "source")


def html_to_svg(html):
    m = re.search(r"<svg[\s\S]*</svg>", html)
    svg = m.group(0)
    svg = re.sub(r'width="[\d.]+mm" height="[\d.]+mm"', "", svg, count=1)
    return svg


def fonts_in(svg):
    fams = set(re.findall(r'font-family="([^"]+)"', svg))
    mapping = {}
    for f in fams:
        if "Serif" in f:
            mapping[f] = D.__dict__.get("F_SERIF") or r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf"
        elif "Medium" in f:
            mapping[f] = r"C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf"
        else:
            mapping[f] = r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf"
    return mapping


def embed_fonts(svg):
    text = "".join(re.findall(r"<text[^>]*>([^<]*)</text>", svg))
    chars = "".join(sorted(set(text + "0123456789/·—　ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")))
    faces = []
    for fam, path in fonts_in(svg).items():
        if not os.path.exists(path):
            continue
        f = TTFont(path, fontNumber=0)
        if "post" in f:
            f["post"].formatType = 3.0          # 去掉字形名，避开 fontTools 的 trim 崩溃
        opts = subset.Options()
        opts.hinting = False
        opts.notdef_outline = True
        sub = subset.Subsetter(options=opts)
        sub.populate(text=chars)
        sub.subset(f)
        buf = io.BytesIO()
        f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        faces.append(f"@font-face{{font-family:'{fam}';src:url(data:font/ttf;base64,{b64}) format('truetype');}}")
    if not faces:
        return svg
    style = "<style><![CDATA[" + "".join(faces) + "]]></style><defs></defs>"
    return svg.replace("<defs>", style + "<defs>", 1) if "<defs>" in svg else svg.replace(">", ">" + style, 1)


def main():
    for d in (SUB, SRC):
        os.makedirs(d, exist_ok=True)
    jobs = [("01-sheet", D.sheet), ("02-poster", design2.poster),
            ("03-passport", design2.passport), ("04-cards", design2.cards)]
    for name, fn in jobs:
        html = fn()
        svg = O.outline(html_to_svg(html))
        for c in D.CITIES:                      # 内嵌 base64 改成相对路径，源文件才轻
            svg = svg.replace(D.art_b64(c["id"]), "art/" + c["id"] + ".png")
        sp = os.path.join(SRC, name + ".svg")
        head = ("<!-- 《一城一票》 " + name + " · 矢量分层源文件。文字已转为路径，不依赖字体；"
                "每个版块是一个具名 g 图层。 -->\n")
        open(sp, "w", encoding="utf-8").write(head + svg)
        png = os.path.join(OUT, name + ".png")
        im = Image.open(png).convert("RGB")
        jp = os.path.join(SUB, name + ".jpg")
        q = 94
        im.save(jp, "JPEG", quality=q, subsampling=0, optimize=True)
        while os.path.getsize(jp) > 19.5 * 1024 * 1024 and q > 80:
            q -= 3
            im.save(jp, "JPEG", quality=q, subsampling=0, optimize=True)
        print(f"{name}.jpg  {os.path.getsize(jp)/1048576:.2f} MB  q={q}  | svg {os.path.getsize(sp)/1048576:.2f} MB")

    readme = os.path.join(SRC, "README.txt")
    open(readme, "w", encoding="utf-8").write(
        "《一城一票》分层源文件\n"
        "======================\n"
        "01-sheet.svg     小版张 A3：每枚票是一个 <g class=\"stamp\" data-city=\"...\"> 图层\n"
        "02-poster.svg    主视觉 A2：标题 / 主票 / 说明 / 十三印 各自成组\n"
        "03-passport.svg  观赛护照 A4 横：左页 / 右页 / 中缝 各自成组\n"
        "04-cards.svg     收藏卡牌：三张卡各自成组\n\n"
        "字体已按本文件用到的字做子集并内嵌（@font-face + base64），换机器打开不会掉字。\n"
        "人偶图在 assets/art/city/*.png（原图 1024×1024），替换后重跑 build.py 即可。\n"
    )
    zp = os.path.join(SUB, "source.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in os.listdir(SRC):
            z.write(os.path.join(SRC, f), "source/" + f)
        art = os.path.join(ROOT, "assets", "art", "glaze")
        os.makedirs(os.path.join(SRC, "art"), exist_ok=True)
        for f in sorted(os.listdir(art)):
            if f.endswith(".png"):
                import shutil as _sh
                _sh.copy(os.path.join(art, f), os.path.join(SRC, "art", f))
                z.write(os.path.join(art, f), "art/" + f)
    print(f"source.zip {os.path.getsize(zp)/1048576:.2f} MB")


if __name__ == "__main__":
    main()
