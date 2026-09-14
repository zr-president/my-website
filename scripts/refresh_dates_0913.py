# -*- coding: utf-8 -*-
"""全站日期刷新到 2026-09-13（周日）
   问题：之前只更新了 4 个"当日"字段，站内 15 个分区 + 多个对象的 updated 仍停在 9/12
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
OLD, NEW = '2026-09-12', '2026-09-13'
log = []

# ============ 1) 所有 updated 字段 ============
n = len(re.findall(r'updated:\s*"' + OLD + '"', d))
d = re.sub(r'updated:\s*"' + OLD + '"', 'updated: "' + NEW + '"', d)
log.append('updated 字段：%d 处 → %s' % (n, NEW))

# ============ 2) DAILY_DATA.update_time ============
d, k = re.subn(r'"update_time":\s*"' + OLD + r'T[\d:+]+\"', '"update_time": "' + NEW + 'T10:20:00+08:00"', d)
log.append('update_time：%d 处' % k)

# ============ 3) 摘要里的"本区当天日期"前缀 ============
prefix_fixes = [
    ('9月12日（周六）学习重点', '9月13日（周日）学习重点'),
    ('2026年9月12日动漫区', '2026年9月13日动漫区'),
    ('9月12日 AI 行业焦点', '9月13日 AI 行业焦点'),
    ('9月12日（周六）', '9月13日（周日）'),
    ('9月12日', '9月13日'),
]
cnt = 0
for a, b in prefix_fixes:
    if a in d:
        c = d.count(a)
        d = d.replace(a, b)
        cnt += c
log.append('摘要日期文本：%d 处 9月12日 → 9月13日' % cnt)

# ============ 4) 时间敏感的数字刷新 ============
num_fixes = [
    ('追番第31天', '追番第32天'),
    ('还剩18天', '还剩17天'),
    ('剩余约 3 话', '剩余约 3 话'),
    ('完结倒计时 17 天', '完结倒计时 17 天'),
]
nc = 0
for a, b in num_fixes:
    if a in d:
        nc += d.count(a)
        d = d.replace(a, b)
log.append('倒计时/天数刷新：%d 处' % nc)

open(FP, 'w', encoding='utf-8').write(d)
print('=== 日期刷新 ===')
for x in log:
    print('  ✅ ' + x)
