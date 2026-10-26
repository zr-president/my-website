# -*- coding: utf-8 -*-
"""修复个人站结构破损：
   ai-growth 分区里「方向 4」更新为「已落地」时，旧版正文没删除，
   留下 3 段孤儿 <p> + 1 个多余的 </div>。
   这个孤儿 </div> 让浏览器提前关闭 <section>，
   导致「四、」「五、」等内容掉出到 .main 下，任何视图都隐藏不掉。

   修法：精确删除这段孤儿内容（先验证只出现一次）。
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:\Users\ZR\Desktop\钟锐的个人网站'
HP = os.path.join(P, 'index.html')

h = open(HP, encoding='utf-8').read()
orig_len = len(h)

START = '<p style="margin:0 0 8px"><b>现状</b>：我现在的 AI 是「每次都从零开始的助手」'
END = '如果 AI 的回答能指回某个 md 文件和具体段落，说明知识库建对了。</p></div>'

ns = h.count(START)
ne = h.count(END)
print('起点出现 %d 次 · 终点出现 %d 次' % (ns, ne))
if ns != 1 or ne != 1:
    print('❌ 不是唯一匹配，中止（避免误删）')
    raise SystemExit(1)

i = h.index(START)
j = h.index(END) + len(END)
block = h[i:j]
print('将删除 %d 字符' % len(block))
print('--- 删除内容预览（前 200 字）---')
print(block[:200].replace('\n', ' '))
print('--- 预览结束 ---')

# 删除后要留一个换行，避免把前后元素粘在一起
rest_after = h[j:]
h2 = h[:i] + ('\n' if not rest_after.startswith('\n') else '') + rest_after.lstrip('\n')

print()
print('长度变化: %d → %d （少 %d）' % (orig_len, len(h2), orig_len - len(h2)))

# ---------- 验证 div 平衡 ----------
def div_balance(s):
    o = len(re.findall(r'<div\b', s))
    c = len(re.findall(r'</div>', s))
    return o, c

start_i = h2.index('<section id="ai-growth"')
nxt = h2.index('<section ', start_i + 10)
seg = h2[start_i:nxt]
o, c = div_balance(seg)
print('ai-growth 分区 div: %d 开 / %d 闭 → %s' % (o, c, '平衡 ✅' if o == c else '仍不平衡 ❌'))

# 全文（排除 JS 字符串里的）粗查
o2, c2 = div_balance(h2)
print('全文 div: %d 开 / %d 闭 （差值 %+d）' % (o2, c2, o2 - c2))

if o != c:
    print('❌ 分区仍不平衡，不写入')
    raise SystemExit(1)

open(HP, 'w', encoding='utf-8').write(h2)
print()
print('✅ 已写入 index.html')

# ---------- 语法体检 ----------
for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', h2):
    pass
print('内联脚本块数:', len(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>', h2)))
