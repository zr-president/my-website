# -*- coding: utf-8 -*-
"""UI V01：Emoji 从「主要导航」与「区块标题」退出
   依据方案 V01：「Emoji 从主要导航和所有标题中退出，改用同一套线性图标；
   保留少量在个人兴趣内容里的表达」
   本次只处理结构性 chrome（侧栏导航 + section-header 的 h2），
   内容卡片里的 emoji 保留（它们承担扫读提示作用）。
"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()

# 匹配 emoji（含变体选择符与 ZWJ 组合）
EMOJI = (r'[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF'
         r'\U0001F1E6-\U0001F1FF\uFE0F\u200D\u2190-\u21FF\u2300-\u23FF]')

changed = {'nav': 0, 'h2': 0}


def strip_leading_emoji(text):
    """去掉开头连续的 emoji 与空白"""
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r'^\s*(?:' + EMOJI + r')+\s*', '', text)
    return text


# ---------- 1) 侧栏导航：<a href="#xxx">emoji 文本</a> ----------
def fix_nav(m):
    inner = m.group(2)
    new = strip_leading_emoji(inner)
    if new != inner and new.strip():
        changed['nav'] += 1
        return m.group(1) + new + m.group(3)
    return m.group(0)


h = re.sub(r'(<a href="#[A-Za-z0-9_-]+"[^>]*>)([^<]+)(</a>)', fix_nav, h)

# ---------- 2) 区块标题：<div class="section-header"><h2>emoji 文本</h2> ----------
def fix_h2(m):
    inner = m.group(2)
    new = strip_leading_emoji(inner)
    if new != inner and new.strip():
        changed['h2'] += 1
        return m.group(1) + new + m.group(3)
    return m.group(0)


h = re.sub(r'(<div class="section-header"><h2>)([^<]+)(</h2>)', fix_h2, h)

open(FP, 'w', encoding='utf-8').write(h)
print('✅ 导航去 emoji：%d 处' % changed['nav'])
print('✅ 区块标题去 emoji：%d 处' % changed['h2'])

# ---------- 校验 ----------
h2 = open(FP, encoding='utf-8').read()
nav_left = re.findall(r'<a href="#[A-Za-z0-9_-]+"[^>]*>\s*' + EMOJI, h2)
h2_left = re.findall(r'<div class="section-header"><h2>\s*' + EMOJI, h2)
print()
print('残留检查：')
print('  导航仍带 emoji: %d' % len(nav_left))
print('  区块标题仍带 emoji: %d' % len(h2_left))
print()
print('抽样（导航）:')
for m in list(re.finditer(r'<a href="#([A-Za-z0-9_-]+)"[^>]*>([^<]+)</a>', h2))[:8]:
    print('  #%-16s %s' % (m.group(1), m.group(2).strip()))
print()
print('抽样（区块标题）:')
for m in list(re.finditer(r'<div class="section-header"><h2>([^<]+)</h2>', h2))[:8]:
    print('  ' + m.group(1).strip())
