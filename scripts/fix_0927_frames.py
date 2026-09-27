# -*- coding: utf-8 -*-
"""补 stock 与 ai-track 的 9/27（周日）框架"""
import io, sys, re, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
assert TODAY == '2026-09-27'

fixes = [
    # stock：周日休市框架
    ('9/14-9/18 A股周复盘：', '9/22-9/26 A股周复盘（9/27 周日更新·周末休市）：'),
    ('9月11日（周五）A股三大指数放量收跌', '9月11日（周五）A股三大指数放量收跌'),
    ('🎯 本周结论（小白版）：① 9/14-9/18 这一周',
     '🎯 本周结论（小白版·截至 9/26 收盘）：① 9/22-9/26 这一周'),
    ('下周（本周）操作预案', '下周（9/28-9/29 两个交易日）操作预案'),
    ('本周（9/22-9/26）操作预案', '9/28-9/29（节前最后两个交易日）操作预案'),
    # ai-track：补 9/27 框架
    ('🎯 今日两条结论（9/26 更新）：', '🎯 今日两条结论（9/27 更新）：'),
    ('<b>一、DSH 桌面端（官方预览版，9/26 跟踪）</b>',
     '<b>一、DSH 桌面端（官方预览版，9/27 跟踪）</b>'),
    ('<b>二、Jev 决策模型（9/26 接入决策）</b>',
     '<b>二、Jev 决策模型（9/27 接入决策）</b>'),
]
c = 0
for a, b in fixes:
    if a in d and a != b:
        c += d.count(a); d = d.replace(a, b)
        print('  ✅ %s…' % a[:36])

# 兜底：给 stock/ai-track 的 summary 加当日标记
d = d.replace('9/14-9/18 A股周复盘', '9/22-9/26 A股周复盘')
n = d.count('9/14-9/18')
if n:
    d = d.replace('9/14-9/18', '9/22-9/26')
    print('  ✅ 兜底替换 9/14-9/18 → 9/22-9/26（%d 处）' % n)

print('共修正 %d 处' % c)
open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
