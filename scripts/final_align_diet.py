# -*- coding: utf-8 -*-
"""最终清理：DETAIL.diet 残留 2300 + DETAIL.fitness/INSIGHTS.fitness 补「训练日 2400」"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'
DFP = BASE + r'\daily_data.js'

DQ = '"'   # 双引号
SQ = "'"   # 单引号


def read_js_str(text, key):
    """读 DETAIL.<key> = '...' 或 "..."，返回 (start, end, value)"""
    for q, esc in [(DQ, r'"(?:[^"\\]|\\.)*"'), (SQ, r"'(?:[^'\\]|\\.)*'")]:
        pat = re.compile(r'(DETAIL\.' + key + r'\s*=\s*)(' + esc + ')')
        m = pat.search(text)
        if m:
            raw = m.group(2)
            inner = raw[1:-1]
            # 还原 JS 转义
            val = (inner.replace('\\\\', '\\')
                        .replace('\\' + q, q)
                        .replace('\\n', '\n')
                        .replace('\\"', '"')
                        .replace("\\'", "'"))
            return m.start(2), m.end(2), val
    return None, None, None


def write_js_str(text, key, val):
    s, e, _ = read_js_str(text, key)
    if s is None:
        return text, False
    return text[:s] + json.dumps(val, ensure_ascii=False) + text[e:], True


c = open(CFP, 'r', encoding='utf-8').read()

# ---------- DETAIL.diet ----------
_, _, diet = read_js_str(c, 'diet')
if diet is None:
    print('❌ 读不到 DETAIL.diet'); raise SystemExit(1)
n2300 = diet.count('2300')
diet = diet.replace('休息日怎么调（约 2300 kcal）', '休息日怎么调（约 2200 kcal）')
diet = diet.replace('约 2300 kcal', '约 2200 kcal')
diet = diet.replace('2300', '2200')
c, ok = write_js_str(c, 'diet', diet)
print('✅ DETAIL.diet：清掉 %d 处 2300 → 2200' % n2300)

# ---------- DETAIL.fitness ----------
_, _, fit = read_js_str(c, 'fitness')
if fit is None:
    print('❌ 读不到 DETAIL.fitness'); raise SystemExit(1)
old_row = '<td>训练日 2500 / 休息日 2300</td>'
if old_row in fit:
    fit = fit.replace(old_row, '<td>训练日 2400 / 休息日 2200</td>')
    print('✅ DETAIL.fitness 营养表已更新为 2400/2200')
elif '训练日 2500' in fit:
    fit = fit.replace('训练日 2500', '训练日 2400').replace('休息日 2300', '休息日 2200')
    print('✅ DETAIL.fitness 热量口径已更新')
else:
    print('ℹ️  DETAIL.fitness 未出现 训练日 2500')

# 确保出现「训练日 2400」（检查项要求）
if '训练日 2400' not in fit:
    fit = fit.replace('<h3>七、营养微调（按 60.65kg 重算）</h3>',
                      '<h3>七、营养微调（按 60.65kg 重算 · 训练日 2400 / 休息日 2200 kcal）</h3>')
    print('✅ DETAIL.fitness 已在标题补入「训练日 2400」')
c, ok = write_js_str(c, 'fitness', fit)
open(CFP, 'w', encoding='utf-8').write(c)
print('   含 训练日 2400:', '训练日 2400' in fit)

# ---------- INSIGHTS.fitness（daily_data）----------
d = open(DFP, 'r', encoding='utf-8').read()
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]
if '训练日 2400' not in seg:
    old = '热量 2500/2300 → <b>2400/2200</b>'
    if old in seg:
        seg = seg.replace(old, '热量 → <b>训练日 2400 / 休息日 2200</b>')
    else:
        seg = seg.replace('热量 2500/2300', '训练日 2400 / 休息日 2200')
    d = d[:i_ins] + seg + d[i_end:]
    print('✅ INSIGHTS.fitness 已补「训练日 2400」')
else:
    print('ℹ️  INSIGHTS.fitness 已含 训练日 2400')
open(DFP, 'w', encoding='utf-8').write(d)

for p in [CFP, DFP]:
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    print('语法 %-18s %s' % (p.split('\\')[-1], 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200]))
print('   含 训练日 2400 (INSIGHTS):', '训练日 2400' in d)
