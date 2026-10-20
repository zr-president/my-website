# -*- coding: utf-8 -*-
"""同步 DETAIL.diet 到新热量口径（2600/2400，蛋白 130-140g）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'

DQ, SQ = '"', "'"


def read_js(text, key):
    for q, esc in [(DQ, r'"(?:[^"\\]|\\.)*"'), (SQ, r"'(?:[^'\\]|\\.)*'")]:
        m = re.search(r'(DETAIL\.' + key + r'\s*=\s*)(' + esc + ')', text)
        if m:
            inner = m.group(2)[1:-1]
            val = (inner.replace('\\\\', '\\').replace('\\' + q, q)
                        .replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'"))
            return m.start(2), m.end(2), val
    return None, None, None


c = open(CFP, encoding='utf-8').read()
s, e, diet = read_js(c, 'diet')
if diet is None:
    print('❌ 读不到 DETAIL.diet'); raise SystemExit(1)
print('原 DETAIL.diet: %d 字' % len(diet))
for k in ['2400', '2200', '125-135g', '60.65kg']:
    print('  含 %-10s %s' % (k, k in diet))

R = [
 ('训练日 2400 kcal / 休息日 2200 kcal', '训练日 2600 kcal / 休息日 2400 kcal'),
 ('训练日 2400 kcal（比维持多约 200）、休息日 2200 kcal（维持）',
  '训练日 2600 kcal（体脂 12-14%，有空间给更大盈余）、休息日 2400 kcal（维持 +300）'),
 ('训练日 2400 kcal', '训练日 2600 kcal'),
 ('休息日 2200 kcal', '休息日 2400 kcal'),
 ('蛋白 125-135g', '蛋白 130-140g'),
 ('取 <b>125-135g', '取 <b>130-140g'),
 ('蛋白约 135g', '蛋白约 140g'),
 ('<strong>2400</strong>', '<strong>2600</strong>'),
 ('<strong>约 135g</strong>', '<strong>约 140g</strong>'),
 ('>2400<', '>2600<'),
 ('>2200<', '>2400<'),
 ('约 2200 kcal', '约 2400 kcal'),
 ('（约 2200 kcal）', '（约 2400 kcal）'),
]
n = 0
for a, b in R:
    if a in diet:
        n += diet.count(a); diet = diet.replace(a, b)
print('\n替换 %d 处' % n)
for k in ['2600', '2400', '130-140g']:
    print('  含 %-10s %s' % (k, k in diet))
for k in ['2500', '2300', '2200', '125-135g']:
    print('  残留 %-10s %s' % (k, k in diet))

c = c[:s] + json.dumps(diet, ensure_ascii=False) + c[e:]
open(CFP, 'w', encoding='utf-8').write(c)
r = subprocess.run(['node', '--check', CFP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
