# -*- coding: utf-8 -*-
"""多模态素材分析：为每张本地图片提取
   ① 主色调（用于卡片强调色 / 悬停光晕）
   ② 平均亮度（决定暗色模式是否需要降亮）
   ③ 朝向与建议的 object-position（避免把主体裁掉）
   输出 → scripts/_img_style.json，供站点使用
"""
import io, sys, os, json, colorsys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
from PIL import Image

DIRS = ['assets/img', 'img']
report = {}

for d in DIRS:
    p = os.path.join(BASE, d)
    if not os.path.isdir(p):
        continue
    for name in sorted(os.listdir(p)):
        if not name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        fp = os.path.join(p, name)
        try:
            im = Image.open(fp).convert('RGB')
        except Exception as e:
            print('  ❌ %s: %s' % (name, e)); continue

        w, h = im.size
        small = im.copy(); small.thumbnail((120, 120))
        px = list(small.getdata())
        n = len(px)

        # 平均亮度
        lum = sum(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px) / n

        # 主色调：量化到 4bit/通道后取众数，再求该桶均值（避免灰调主导）
        from collections import Counter
        buckets = Counter(((r >> 4) << 8 | (g >> 4) << 4 | (b >> 4)) for r, g, b in px)
        best = None
        for key, cnt in buckets.most_common(12):
            r0, g0, b0 = (key >> 8) & 15, (key >> 4) & 15, key & 15
            members = [(r, g, b) for r, g, b in px
                       if ((r >> 4) == r0 and (g >> 4) == g0 and (b >> 4) == b0)]
            if not members:
                continue
            ar = sum(m[0] for m in members) / len(members)
            ag = sum(m[1] for m in members) / len(members)
            ab = sum(m[2] for m in members) / len(members)
            hh, ss, vv = colorsys.rgb_to_hsv(ar / 255, ag / 255, ab / 255)
            # 偏好"有彩色 + 中等明度"的桶：用于强调色才好看
            score = cnt * (0.35 + ss) * (1 - abs(vv - 0.55))
            if best is None or score > best[0]:
                best = (score, (int(ar), int(ag), int(ab)))
        dom = best[1] if best else (120, 120, 140)

        # 主体位置启发式：竖版海报主体多在上 1/3；横版居中
        if h > w * 1.15:
            pos = 'center 28%'
        elif h > w:
            pos = 'center 38%'
        else:
            pos = 'center 50%'

        report[name] = {
            'dir': d, 'size': [w, h], 'ratio': round(w / h, 3),
            'color': '#%02x%02x%02x' % dom, 'rgb': dom,
            'luminance': round(lum, 1),
            'bright': lum > 165, 'objectPosition': pos,
        }
        print('  %-46s %4dx%-4d 主色 %s 亮度 %5.1f %s' % (
            name[:46], w, h, report[name]['color'], lum, '（偏亮·暗色模式需处理）' if lum > 165 else ''))

out = os.path.join(BASE, 'scripts', '_img_style.json')
json.dump(report, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print()
print('共分析 %d 张 → scripts/_img_style.json' % len(report))
print('偏亮（暗色模式下建议降亮）: %d 张' % sum(1 for v in report.values() if v['bright']))
