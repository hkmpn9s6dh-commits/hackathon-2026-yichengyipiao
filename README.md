# 《一城一票》— 江苏省城市足球联赛 AIGC 创作大赛 · IP 形象与设计

> 十三座城市，十三张票。球票与邮票是同一件东西：打孔边、编号、日期、副券。

## 这是什么

赛道：IP 形象与设计（2026 苏超 AIGC 创作大赛）｜截止 2026-12-15｜全国、个人可报。
四组成品：小版张（13 枚邮票）、主视觉海报、观赛护照跨页、收藏卡牌。

## 怎么跑

```bash
py -3 src/cutout.py      # 人偶去背 + 按脚底线对齐（读 assets/art/city）
py -3 src/tone.py        # 统一为影青单色釉（写 assets/art/glaze）
py -3 build.py all       # 渲染四张成品到 out/（300dpi）
py -3 verify.py --rebuild  # 146 条断言 + 重建字节一致
py -3 src/export.py      # 投稿件：out/submit/*.jpg + source.zip
```

依赖：Python 3.8（Pillow、numpy、opencv-python、fontTools）、Node 22 + Playwright（Chromium）。
`node_modules` 需有 `playwright`；本机把 `src/shot.mjs` 里的 `CHROME` 指到已安装的 Chromium 即可。

## 文件

| 路径 | 内容 |
|---|---|
| `data/cities.json` | 十三城单一来源：城名／拼音／嘟嘟名／原型／口号／城市色 |
| `src/design.py` | 票面骨架、小版张、打孔 mask、朱印、对比度压暗 |
| `src/design2.py` | 主海报、观赛护照、收藏卡牌 |
| `src/cutout.py` `src/tone.py` | 人偶去背与釉色统一 |
| `src/outline.py` | 把 SVG 里的文字转路径（源文件不依赖字体） |
| `build.py` `verify.py` `src/export.py` | 渲染 / 验收 / 导出投稿件 |
| `out/submit/` | 四张 JPG + `source.zip`（分层 SVG + 人偶 PNG） |
| `docs/` | 尺子、设计说明、AI 使用说明、提交单 |

## 判据

`SPEC.md` 的 AC-01～AC-10，全部由 `verify.py` 判，不靠肉眼：

- 数据完整、十三只脚底线对齐 0 px、主块占比 ≥97%；
- 四张成品 ≥300 dpi、单文件 ≤20 MB；
- 城名／拼音／口号按字宽逐条量，不溢出不压印；
- 口号色对比度 ≥4.5:1（自动压暗到合格，见 `ink_of`）；
- 重建两次 sha256 逐字节一致。
