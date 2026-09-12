# -*- coding: utf-8 -*-
"""删除机会雷达里重复的条目开括号"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()
old = '    },\n    {\n    {\n      emoji: "\U0001F5C4\uFE0F",'
new = '    },\n    {\n      emoji: "\U0001F5C4\uFE0F",'
if old in c:
    c = c.replace(old, new, 1)
    open(FP, 'w', encoding='utf-8').write(c)
    print('OK 已删除重复花括号')
else:
    print('MISS')
