# -*- coding: utf-8 -*-
"""补全日期刷新：兼容 "updated": "..." / updated: '...' / updated: "..." 三种写法"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
OLD, NEW = '2026-09-12', '2026-09-13'

# 匹配 updated / "updated" / 'updated' 键，保留原有引号风格
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])' + re.escape(OLD) + r'\2')
d, n = pat.subn(lambda m: m.group(1) + m.group(2) + NEW + m.group(2), d)
print('✅ updated 字段替换：%d 处 → %s' % (n, NEW))

# 剩余出现处（需要人工判断是"当日字段"还是"历史事实"）
rest = [m.start() for m in re.finditer(re.escape(OLD), d)]
print()
print('=== 剩余 %d 处 %s（逐条判断）===' % (len(rest), OLD))
for i, pos in enumerate(rest, 1):
    line_no = d[:pos].count('\n') + 1
    line = d.split('\n')[line_no - 1].strip()
    print('  %2d. L%-5d %s' % (i, line_no, line[:120]))

# 非 updated 字段里的日期也一并更新（摘要/备注里的"当天"表述）
fixed = 0
for a, b in [
    ('"2026-09-12"', '"2026-09-13"'),   # 其它对象的日期字段
    ("'2026-09-12'", "'2026-09-13'"),
]:
    if a in d:
        fixed += d.count(a)
        d = d.replace(a, b)
print()
print('✅ 其它日期字段替换：%d 处' % fixed)

open(FP, 'w', encoding='utf-8').write(d)
