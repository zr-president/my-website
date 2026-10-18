# -*- coding: utf-8 -*-
"""重跑：把分区搜索限制在 var INSIGHTS 段内（避免匹配到 PICKS 里的同名键）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

# ---- 定位 INSIGHTS 段 ----
i_ins = d.find('var INSIGHTS = {')
assert i_ins > 0, '未找到 INSIGHTS'
m_end = re.search(r'\n\};', d[i_ins:])
i_end = i_ins + m_end.end()
print('INSIGHTS 段：%d → %d（%d 字）' % (i_ins, i_end, i_end - i_ins))
head, ins, tail = d[:i_ins], d[i_ins:i_end], d[i_end:]

# 复用上一版脚本里已写好的内容
src = open(BASE + r'\scripts\fix_1018_sections.py', encoding='utf-8').read()
ns = {}
start = src.find('S = {}')
stop = src.find('# ---- 应用')
exec(src[start:stop], ns)
S = ns['S']
print('待写入分区：%d 个' % len(S))

done, skip = [], []
for k, v in S.items():
    pat = re.compile(r'((?:"' + re.escape(k) + r'"|' + re.escape(k) + r')\s*:\s*\{)([\s\S]*?)(\n  \})')
    m = pat.search(ins)
    if not m:
        skip.append(k + '(未匹配)'); continue
    body = m.group(2)
    sm = re.search(r'("?summary"?\s*:\s*)(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', body)
    if not sm:
        skip.append(k + '(无summary)'); continue
    nb = body[:sm.start()] + sm.group(1) + json.dumps(v, ensure_ascii=False) + body[sm.end():]
    ins = ins[:m.start()] + m.group(1) + nb + m.group(3) + ins[m.end():]
    done.append(k)

print('✅ 成功: %d 个 → %s' % (len(done), ', '.join(done)))
if skip:
    print('⚠️  跳过: %s' % ', '.join(skip))

out = head + ins + tail
open(FP, 'w', encoding='utf-8').write(out)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
