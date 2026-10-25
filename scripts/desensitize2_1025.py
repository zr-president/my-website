# -*- coding: utf-8 -*-
"""隐私脱敏 第二轮：把「肾结石」这个诊断名软化为中性的风险描述
   保留全部实用建议（饮水、草酸、复查），只去掉诊断标签
"""
import io, sys, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FILES = ['daily_data.js', 'detail_content.js', 'index.html', 'knowledge_index.js', 'knowledge_index.json']

REPL = [
 ('肾结石患者夏天怎么喝水？', '易结石体质夏天怎么喝水？'),
 ('🪨 肾结石（增肌期更要严格执行）：', '🪨 防结石（增肌期更要严格执行）：'),
 ('健康提醒：肾结石与你', '健康提醒：饮水与结石风险'),
 ('约占肾结石的80%', '约占结石的80%'),
 ('不一定会得肾结石', '不一定会形成结石'),
 ('结石病史或家族史（比如我）', '结石风险或家族史（比如我）'),
 ('data-search="饮食 食谱 营养 肾结石"', 'data-search="饮食 食谱 营养 低草酸"'),
 ('核心原则：充足饮', '核心原则：充足饮'),
 ('肾结石倾向者', '易结石体质者'),
 ('肾结石饮食', '低草酸饮食'),
 ('肾结石', '结石风险'),
]

total = 0
for fn in FILES:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        continue
    c = open(p, encoding='utf-8').read()
    orig = c
    for a, b in REPL:
        if a in c and a != b:
            c = c.replace(a, b)
    if c != orig:
        open(p, 'w', encoding='utf-8').write(c)
        total += 1
        print('  ✅ %s 已处理' % fn)

print()
print('=== 残留诊断名检查 ===')
left = 0
for fn in FILES + ['personal_config.js']:
    p = os.path.join(BASE, fn)
    if not os.path.exists(p):
        continue
    c = open(p, encoding='utf-8').read()
    for kw in ['甲状腺', '肾结石']:
        cnt = c.count(kw)
        if cnt:
            left += cnt
            for m in re.finditer(kw, c):
                s = max(0, m.start() - 35); e = min(len(c), m.start() + 35)
                print('  ⚠️ %s：…%s…' % (fn, c[s:e].replace('\n', ' ')))
print('  残留合计: %d 处' % left)

print()
for fn in ['personal_config.js', 'daily_data.js', 'detail_content.js', 'knowledge_index.js']:
    p = os.path.join(BASE, fn)
    if os.path.exists(p):
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        print('  语法 %-22s %s' % (fn, 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:150]))
