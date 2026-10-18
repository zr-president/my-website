# -*- coding: utf-8 -*-
"""修正 DETAIL.diet 口径 + INSIGHTS.fitness 补「下肢」 + 修 wk 兜底正则"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'
DFP = BASE + r'\daily_data.js'
CHK = BASE + r'\scripts\check_consistency.py'

# ---------- ① DETAIL.diet ----------
c = open(CFP, 'r', encoding='utf-8').read()
m = re.search(r"(DETAIL\.diet\s*=\s*)(\"(?:[^\"\\]|\\.)*\")", c)
diet = json.loads(m.group(2))
before = diet
diet = diet.replace('训练日 2500 kcal / 休息日 2300 kcal', '训练日 2400 kcal / 休息日 2200 kcal')
diet = diet.replace('蛋白 110-130g', '蛋白 125-135g')
diet = diet.replace('你 170cm/59kg、体脂 15-18%', '你 170cm/60.65kg、体脂 15-16%')
diet = diet.replace('训练日 2500 kcal（比维持多约 200）、休息日 2300 kcal（维持）',
                    '训练日 2400 kcal（比维持多约 200）、休息日 2200 kcal（维持）')
diet = diet.replace('蛋白按 1.9-2.2g/kg 取 <b>110-130g', '蛋白按 2.0-2.2g/kg 取 <b>125-135g')
diet = diet.replace('训练日食谱（合计 2500 kcal · 蛋白约 130g）', '训练日食谱（合计 2400 kcal · 蛋白约 135g）')
diet = diet.replace('<td><strong>2500</strong></td><td><strong>约 130g</strong></td>',
                    '<td><strong>2400</strong></td><td><strong>约 135g</strong></td>')
# 剩余 2300（休息日食谱）→ 2200
diet = diet.replace('休息日食谱', '休息日食谱')
diet = re.sub(r'(休息日[^<]{0,40})2300', r'\g<1>2200', diet)
diet = diet.replace('<td><strong>2300</strong></td>', '<td><strong>2200</strong></td>')
# 兜底：仍是 2500/2300 的表格数字
diet = diet.replace('>2500<', '>2400<').replace('>2300<', '>2200<')
c = c[:m.start(2)] + json.dumps(diet, ensure_ascii=False) + c[m.end(2):]
open(CFP, 'w', encoding='utf-8').write(c)
print('✅ DETAIL.diet 已更新（%d 字）' % len(diet))
for k in ['2400', '2200', '125-135g', '60.65kg']:
    print('   含 %-10s %s' % (k, k in diet))
for k in ['2500', '2300', '110-130g', '59kg']:
    print('   残留 %-10s %s' % (k, k in diet))

# ---------- ② INSIGHTS.fitness 补「下肢」 ----------
d = open(DFP, 'r', encoding='utf-8').read()
old = '<b>周三 腿+核心</b>'
new = '<b>周三 下肢（腿）+核心</b>'
if old in d:
    d = d.replace(old, new); print('✅ INSIGHTS.fitness 已补「下肢」')
else:
    print('⚠️  INSIGHTS.fitness 未找到锚点，尝试其他')
    if '周三 腿 + 核心' in d:
        d = d.replace('周三 腿 + 核心', '周三 下肢（腿）+核心'); print('✅ 已用备用锚点')
open(DFP, 'w', encoding='utf-8').write(d)

# ---------- ③ 修 wk 兜底正则（group(1) 必须含全文） ----------
k = open(CHK, 'r', encoding='utf-8').read()
old_fb = "    wk = re.search(r'新周计划.*?(</table>)', fitness, re.S)"
new_fb = "    wk = re.search(r'(新周计划[\\s\\S]*?</table>)', fitness, re.S)"
if old_fb in k:
    k = k.replace(old_fb, new_fb); open(CHK, 'w', encoding='utf-8').write(k)
    print('✅ wk 兜底正则已修正（group(1) 含全文）')
else:
    print('⚠️  未找到 wk 兜底行，检查：')
    for line in k.splitlines():
        if '新周计划' in line: print('   ' + line)

for p in [CFP, DFP]:
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    print('语法 %-18s %s' % (p.split('\\')[-1], 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200]))
