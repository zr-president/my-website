# -*- coding: utf-8 -*-
"""按【系统真实日期】更新到 2026-09-14（周一）
   教训：此前更新是拿"上次内容日期+1"推算，从未读系统时钟 —— 永远差一天。
   本脚本从系统时钟取日期，并做周一专属内容调整。
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'

# ---------- 0) 日期来源：系统时钟 ----------
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
MMDD = '%d月%d日' % (now.month, now.day)
print('系统日期：%s（%s）' % (TODAY, WD))

d = open(FP, 'r', encoding='utf-8').read()
OLD_DATES = ['2026-09-13', '2026-09-12']

# ---------- 1) 把所有"当日"日期字段改到 TODAY ----------
# 1a) updated 字段（三种引号风格）
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-09-1[23])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
print('✅ updated 字段 → %s：%d 处' % (TODAY, n1))

# 1b) date 字段（要闻 / 词汇）
d, n2 = re.subn(r'(DAILY_BRIEFING = \{\s*\n\s*date:\s*")([^"]+)(")',
                lambda m: m.group(1) + TODAY + m.group(3), d)
d, n3 = re.subn(r'(DAILY_VOCAB = \{\s*\n\s*date:\s*")([^"]+)(")',
                lambda m: m.group(1) + TODAY + m.group(3), d)
print('✅ 要闻/词汇 date → %s：%d 处' % (TODAY, n2 + n3))

# 1c) update_date（中文格式）
d, n4 = re.subn(r'("update_date":\s*")([^"]+)(")',
                lambda m: m.group(1) + CN + m.group(3), d)
d, n5 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 更新日期/时间 → %s：%d 处' % (CN, n4 + n5))

# 1d) LEARN_PATHS.updated 已在 updated 规则内；DAILY_DATA.movie.updated 同理

# ---------- 2) 摘要里的"当天"表述 ----------
fixes = [
    ('9月13日（周日）学习重点（周末可学3件事）', MMDD + '（' + WD + '）学习重点'),
    ('9月13日（周日）', MMDD + '（' + WD + '）'),
    ('9月13日', MMDD),
    ('2026年9月13日动漫区', str(now.year) + '年' + MMDD + '动漫区'),
]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 摘要日期文本：%d 处' % c)

# ---------- 3) 周一专属内容调整 ----------
mon_fixes = [
    # 周一是交易日：把"周末休市"口径换成"今日开盘观察"
    ('周末休市：把上周五的盘面结论写成一句话，等周一验证', 'A股今日开盘：验证上周五的结论'),
    ('下周一(9/14)看：', '今日(9/14)看：'),
    ('下周一（9/14）看：', '今日（9/14）看：'),
    ('倒计时18天', '倒计时16天'),
    ('倒计时 18 天', '倒计时 16 天'),
    ('倒计时17天', '倒计时16天'),
    ('倒计时 17 天', '倒计时 16 天'),
    ('追番第32天', '追番第33天'),
]
m = 0
for a, b in mon_fixes:
    if a in d:
        m += d.count(a); d = d.replace(a, b)
print('✅ 周一内容调整：%d 处' % m)

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
