import io, os
from fontTools import subset
from fontTools.ttLib import TTFont

paths = [r"C:\Windows\Fonts\Source Han Serif SC Heavy (TrueType).ttf",
         r"C:\Windows\Fonts\Noto Sans SC Medium (TrueType).otf",
         r"C:\Windows\Fonts\Noto Sans SC Bold (TrueType).otf",
         r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"]
for p in paths:
    name = os.path.basename(p)
    ok = False
    for drop in (False, True):
        try:
            f = TTFont(p, fontNumber=0)
            o = subset.Options()
            o.hinting = False
            if drop and "post" in f:
                f["post"].formatType = 3.0
            s = subset.Subsetter(options=o)
            s.populate(text="一城一票南京无锡")
            s.subset(f)
            b = io.BytesIO()
            f.save(b)
            print("OK  ", name, "drop_post" if drop else "", len(b.getvalue()) // 1024, "KB")
            ok = True
            break
        except Exception as e:
            print("FAIL", name, "drop_post" if drop else "", type(e).__name__, str(e)[:70])
    if not ok:
        print("----", name, "两种都失败")
