# -*- coding: utf-8 -*-
"""补 fitness 与 ai-track 的当日（9/26）框架"""
import io, sys, re, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
assert TODAY == '2026-09-26'

fixes = [
    # fitness：补 9/26 第2周收官框架
    ('🎯 目标调整（9/23）', '🎯 目标调整（9/19）｜9/26 第 2 周收官'),
    ('目标调整（9/23）', '目标调整（9/19）· 9/26 第2周收官'),
    ('12 周目标：62-63kg、体脂 13-14%、腹肌清晰。',
     '12 周目标：62-63kg、体脂 13-14%、腹肌清晰。<br><br><b>9/26 进展</b>：增肌版计划执行满 2 周（9/14 起）。第 1 周建立动作模式与负重基线，第 2 周按【每周只推一项】推进。第 2 周收官检查两件事：① 各动作训练容量（组×次×负重）是否较第 1 周上升 ② 体重是否按 0.25-0.5kg/周 增长。下周进入第 3 周，继续单变量推进。'),
    # ai-track：补 9/26 当日框架
    ('🎯 今日两条结论：', '🎯 今日两条结论（9/26 更新）：'),
    ('<b>一、DSH 桌面端（官方预览版）</b>：9 月 25 日晚，',
     '<b>一、DSH 桌面端（官方预览版，9/26 跟踪）</b>：9 月 25 日晚，'),
    ('<b>二、Jev 决策模型</b>：TypeSafe 9/15 发布的首个 System One Model。',
     '<b>二、Jev 决策模型（9/26 接入决策）</b>：TypeSafe 9/15 发布的首个 System One Model。'),
]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
        print('  ✅ %s…' % a[:34])
print('共修正 %d 处' % c)

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
