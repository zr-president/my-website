# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open(r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js', 'r', encoding='utf-8').read()

i = c.find('var LEARN_PATHS')
j = c.find('var AGENT_STACKS', i)
blk = c[i:j]
print('LEARN_PATHS 长度:', len(blk))
print('--- items 区(前600字) ---')
k = blk.find('items: [')
print(blk[k:k+600])
print()
print('--- archive 键 ---')
for m in re.finditer(r'"(20\d\d-\d\d-\d\d)":\s*\[', blk):
    print(' -', m.group(1))
print()
print('--- items 标题 ---')
items_m = re.search(r'items:\s*\[(.*?)\n  \],', blk, re.S)
if items_m:
    for m in re.finditer(r'title:"([^"]{0,45})', items_m.group(1)):
        print('  ·', m.group(1))
print()
v = c.find('var DAILY_VOCAB')
vj = c.find('var AI_MODEL_COMPARISON', v)
vblk = c[v:vj]
print('DAILY_VOCAB 长度:', len(vblk), '| 词数:', vblk.count('word:"'))
print('--- 当前词 ---')
for m in re.finditer(r'word:"([^"]{0,40})', vblk):
    print('  ·', m.group(1))
