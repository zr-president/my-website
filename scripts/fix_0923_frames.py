# -*- coding: utf-8 -*-
"""修正 stock 与 ai-track 的当日框架，让内容日期不落后"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
assert TODAY == '2026-09-23'

fixes = [
    # ai-track：补当日框架
    ('9月15日 TypeSafe 发布 Jev，定义为第一个【System One Model】。',
     '截至 9 月 23 日，TypeSafe 于 9 月 15 日发布的 Jev 已发酵一周。它被定义为第一个【System One Model】。'),
    ('<b>对你（AI 产品方向）的三个实际用法</b>',
     '（9/23 跟踪）<b>对你（AI 产品方向）的三个实际用法</b>'),
    # stock：把"下周(9/21起)"改为本周口径
    ('下周（9/21 起）操作预案', '本周（9/22-9/26）操作预案'),
    ('9/21 起的预案继续有效', '本周预案继续有效'),
    ('下周关注：能否有效站稳 3900', '本周（9/23）关注：能否有效站稳 3900'),
    ('下周关注点与操作纪律', '本周关注点与操作纪律'),
]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
        print('  ✅ %s…' % a[:30])
print('共修正 %d 处' % c)

# 兜底：若 stock 仍含 9/21，替换为 9/23 语境
n = d.count('9/21')
if n:
    d = d.replace('（9/21 起）', '（本周）').replace('9/21 起', '本周起').replace('9/21', '9/23')
    print('  兜底替换 9/21：%d 处' % n)

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
