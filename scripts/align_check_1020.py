# -*- coding: utf-8 -*-
"""① 检查脚本常量更新到新计划（2600/2400/130-140g）
   ② INSIGHTS.fitness 补 60.65kg 与「下肢」
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CHK = BASE + r'\scripts\check_consistency.py'
DFP = BASE + r'\daily_data.js'

# ---------- ① 检查脚本 ----------
k = open(CHK, encoding='utf-8').read()
subs = [
 ("CAL = '训练日 2400'", "CAL = '训练日 2600'"),
 ("'训练日 2400' in txt", "'训练日 2600' in txt"),
 ("含热量口径「训练日 2400」", "含热量口径「训练日 2600」"),
 ("缺热量口径「训练日 2400」", "缺热量口径「训练日 2600」"),
 ("if '训练日 2400' in fitness or '训练日 2400' in ins_fit", "if '训练日 2600' in fitness or '训练日 2600' in ins_fit"),
 ("训练日 2400 / +200", "训练日 2600 / +200"),
 ("「训练日 2400」", "「训练日 2600」"),
 ("if '休息日 2200' in diet and '休息日 2200' in ins_diet", "if '休息日 2400' in diet and '休息日 2400' in ins_diet"),
 ("休息日 2200 口径一致", "休息日 2400 口径一致"),
 ("休息日 2200 口径未在两处同时出现", "休息日 2400 口径未在两处同时出现"),
 ("if '125-135g' in diet", "if '130-140g' in diet"),
 ("含蛋白口径 125-135g", "含蛋白口径 130-140g"),
 ("缺蛋白口径 125-135g", "缺蛋白口径 130-140g"),
 ("if '125-135g' in ins_diet", "if '130-140g' in ins_diet"),
]
n = 0
for a, b in subs:
    if a in k:
        k = k.replace(a, b); n += 1
open(CHK, 'w', encoding='utf-8').write(k)
print('✅ 检查脚本常量替换 %d 处' % n)

# ---------- ② INSIGHTS.fitness 补两个口径 ----------
d = open(DFP, encoding='utf-8').read()
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]

fit_start = seg.find('fitness: {')
if fit_start < 0:
    fit_start = seg.find('"fitness": {')
seg_end = seg.find('\n  },', fit_start)
block = seg[fit_start:seg_end]

# 补 60.65kg
if '60.65kg' not in block:
    block = block.replace('BMI 21.0', '体重 60.65kg、BMI 21.0', 1)
    if '60.65kg' not in block:
        block = block.replace('BMI 21.0。', '体重 60.65kg，BMI 21.0。', 1)
# 补「下肢」
if '下肢' not in block:
    block = block.replace('臀桥（补臀', '臀桥（补臀+下肢后链', 1)
    if '下肢' not in block:
        block = block.replace('臀桥', '臀桥（下肢后链）', 1)

seg = seg[:fit_start] + block + seg[seg_end:]
d = d[:i_ins] + seg + d[i_end:]
open(DFP, 'w', encoding='utf-8').write(d)
print('✅ INSIGHTS.fitness 补入：60.65kg=%s  下肢=%s' % ('60.65kg' in block, '下肢' in block))

for p in [DFP, CHK]:
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True) if p.endswith('.js') else None
    if r:
        print('语法 %-18s %s' % (p.split('\\')[-1], 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
