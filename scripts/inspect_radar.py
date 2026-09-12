# -*- coding: utf-8 -*-
"""查看 OPPORTUNITY_RADAR 结构"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open(r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js', 'r', encoding='utf-8').read()
i = c.find('var OPPORTUNITY_RADAR')
j = c.find('var AI_LIFE_HACKS', i)
blk = c[i:j]
print('长度:', len(blk))
print('emoji 条目数:', blk.count('emoji:'))
print('--- 标题 ---')
for m in re.finditer(r'title:\s*"([^"]{0,50})', blk):
    print(' -', m.group(1))
print('--- 结尾 250 字 ---')
print(blk[-250:])
