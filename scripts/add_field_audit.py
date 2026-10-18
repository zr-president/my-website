# -*- coding: utf-8 -*-
"""给 audit_freshness.py 增加「逐字段检查」，防止新 summary 掩盖旧 tip/trend"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\ZR\Desktop\钟锐的个人网站\scripts\audit_freshness.py'
c = open(P, encoding='utf-8').read()

anchor = """print()
print('=== 今日常规内容（要闻/待办）是否含过期表述 ===')"""

block = """print()
print('=== 逐字段检查：summary / trend / tip 各自的最新日期 ===')
print('    （防止新的 summary 掩盖旧的 tip ——「⚡ 今日行动」渲染的就是 tip）')
field_stale = []
for k, s in data['sections'].items():
    for f in ('summary', 'trend', 'tip'):
        txt = s.get(f) or ''
        if not txt.strip():
            continue
        ds = dates_in(txt)
        valid = [(mo, dy) for mo, dy, _ in ds if 1 <= mo <= 12]
        if not valid:
            continue
        newest = max(valid, key=lambda x: datetime.date(2026, x[0], x[1]))
        lag = (today_dt - datetime.date(2026, newest[0], newest[1])).days
        if lag > 2:
            field_stale.append((k, f, '%d月%d日' % newest, lag))
if field_stale:
    for k, f, dd, lag in sorted(field_stale, key=lambda x: -x[3]):
        print('  ❌ %-11s %-8s 最新只到 %s（落后 %d 天）' % (k, f, dd, lag))
else:
    print('  ✅ 三个字段的内容日期均不落后')

print()
print('=== 今日常规内容（要闻/待办）是否含过期表述 ===')"""

if '逐字段检查' in c:
    print('ℹ️  已有逐字段检查，跳过')
elif anchor in c:
    c = c.replace(anchor, block, 1)
    open(P, 'w', encoding='utf-8').write(c)
    print('✅ audit_freshness.py 已加入逐字段检查')
else:
    print('❌ 未找到锚点')
    print('   尾部内容：', repr(c[-300:]))
