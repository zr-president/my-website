# -*- coding: utf-8 -*-
"""改进的图片主色提取：排除近黑/近白/低饱和灰，只取"有彩色的代表色"
   输出 scripts/_img_style.json（含 accent / accentSoft / objectPosition / darkAdjust）
"""
import io, sys, os, json, colorsys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
from PIL import Image

report = {}
for d in ['assets/img', 'img']:
    p = os.path.join(BASE, d)
    if not os.path.isdir(p):
        continue
    for name in sorted(os.listdir(p)):
        if not name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        im = Image.open(os.path.join(p, name)).convert('RGB')
        w, h = im.size
        small = im.copy(); small.thumbnail((140, 140))
        px = list(small.getdata())

        lum = sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px) / len(px)

        # 候选：排除近黑(v<.15)、近白(v>.92)、低饱和(s<.15)
        cand = []
        for r, g, b in px:
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if vv < 0.15 or vv > 0.92 or ss < 0.15:
                continue
            # 权重：饱和度越高越有代表性；明度居中最好用
            wgt = (0.4 + ss) * (1 - abs(vv - 0.58) * 1.1)
            cand.append((wgt, r, g, b))

        if cand:
            tw = sum(c[0] for c in cand)
            ar = int(sum(c[0] * c[1] for c in cand) / tw)
            ag = int(sum(c[0] * c[2] for c in cand) / tw)
            ab = int(sum(c[0] * c[3] for c in cand) / tw)
            # 提到可用作强调色的明度/饱和度
            hh, ss, vv = colorsys.rgb_to_hsv(ar / 255, ag / 255, ab / 255)
            ss = min(1.0, ss * 1.25 + 0.08)
            vv = min(0.86, max(0.42, vv))
            ar2, ag2, ab2 = colorsys.hsv_to_rgb(hh, ss, vv)
            accent = (int(ar2 * 255), int(ag2 * 255), int(ab2 * 255))
            src = 'hue'
        else:
            # 全灰/全黑图 → 用中性靛蓝兜底
            accent = (99, 102, 241); src = 'fallback'

        def hx(c):
            return '#%02x%02x%02x' % c

        # 主体位置：竖版海报人物多在上部
        pos = 'center 26%' if h > w * 1.15 else ('center 38%' if h > w else 'center 50%')

        report[name] = {
            'dir': d, 'size': [w, h],
            'accent': hx(accent),
            'accentSoft': hx(tuple(int(c * 0.16 + 244 * 0.84) for c in accent)),
            'source': src,
            'luminance': round(lum, 1),
            'darkAdjust': ('brightness(.86) saturate(.92)' if lum > 165 else
                           ('brightness(1.06)' if lum < 70 else 'none')),
            'objectPosition': pos,
        }
        print('  %-44s 主色 %s (%s)  亮度 %5.1f  暗色调整 %s' % (
            name[:44], report[name]['accent'], src, lum, report[name]['darkAdjust']))

json.dump(report, open(os.path.join(BASE, 'scripts', '_img_style.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('共 %d 张' % len(report))
print('按色相取色成功：%d 张；兜底：%d 张' % (
    sum(1 for v in report.values() if v['source'] == 'hue'),
    sum(1 for v in report.values() if v['source'] == 'fallback')))
