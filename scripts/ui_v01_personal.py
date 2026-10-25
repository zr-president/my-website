# -*- coding: utf-8 -*-
"""UI V01 设计规范：个人站
   1) 注入共用 token（间距 4/8 · 圆角 8-12 · 字号阶梯 · 边框两级 · 语义色）
   2) body 显式字号 15px
   3) 微字号上调：8→10 / 9→11 / 10→12 / 11→12（辅助信息进入 12px+ 区间）
   4) 标题阶梯上调：页面标题进 28-36px 区间
   5) 6px 圆角 → 8px（V01: 圆角 8-12px）
"""
import io, sys, re, subprocess, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\index.html'
h = open(FP, encoding='utf-8').read()
orig_len = len(h)

# ============ 1) 注入 token ============
TOKENS = '''  /* ===== V01 设计规范 token（两站共用契约）===== */
  /* 间距：4/8 基础网格 */
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px; --sp-8:48px;
  /* 圆角：8-12px 三档 */
  --r-sm:8px; --r-md:10px; --r-lg:12px; --r-pill:999px;
  /* 字号阶梯：辅助 12-14 / 正文 15-16 / 标题阶梯 */
  --fs-aux:12px; --fs-sm:13px; --fs-body:15px; --fs-lg:16px;
  --fs-h3:18px; --fs-h2:22px; --fs-h1:30px; --fs-display:34px;
  /* 行高 */
  --lh-tight:1.35; --lh-body:1.7;
  /* 边框：只有两级（V01: 有限边框层级） */
  --line-1:var(--border); --line-2:var(--border2);
  /* 语义色：青绿只表示完成/可用（V01: 一种主要强调色） */
  --c-accent:var(--accent); --c-done:var(--green); --c-warn:var(--orange); --c-danger:var(--red);
'''
# 深色主题也要有（border2 在深色里存在）
TOKENS_DARK = '''  --line-1:var(--border); --line-2:var(--border2);
  --c-accent:var(--accent); --c-done:var(--green); --c-warn:var(--orange); --c-danger:var(--red);
'''

if '--sp-1:4px' in h:
    print('ℹ️  token 已存在，跳过注入')
else:
    # 插到第一个 :root 块的末尾（--nav-w 那行之后）
    m = re.search(r'(:root\s*\{[^}]*?--nav-w:\d+px;[^}]*?)\}', h)
    if m:
        h = h[:m.end(1)] + '\n' + TOKENS + h[m.end(1):]
        print('✅ 已注入 token 到 :root')
    else:
        print('❌ 未找到 :root 插入点')

# ============ 2) body 显式字号 ============
old_body = 'body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.7;display:flex;min-height:100vh;overflow-x:hidden}'
new_body = ('body{font-family:var(--font);background:var(--bg);color:var(--text);'
            'font-size:var(--fs-body);line-height:var(--lh-body);display:flex;min-height:100vh;overflow-x:hidden}')
if old_body in h:
    h = h.replace(old_body, new_body, 1)
    print('✅ body 显式 font-size:15px')
elif 'font-size:var(--fs-body)' in h:
    print('ℹ️  body 已设')
else:
    print('⚠️  body 规则未匹配，尝试宽松匹配')
    h2 = re.sub(r'(body\{font-family:var\(--font\)[^}]*?)(line-height:[\d.]+;)',
                r'\1font-size:var(--fs-body);\2', h, count=1)
    if h2 != h:
        h = h2; print('✅ body 宽松匹配已插入')
    else:
        print('❌ body 未处理')

# ============ 3) 微字号上调 ============
BUMP = [('8px', '10px'), ('9px', '11px'), ('10px', '12px'), ('11px', '12px')]
counts = {}
for a, b in BUMP:
    pat = re.compile(r'(font-size:\s*)' + re.escape(a) + r'\b')
    n = len(pat.findall(h))
    if n:
        h = pat.sub(lambda m: m.group(1) + b, h)
    counts[a] = n
print('✅ 微字号上调：' + ' · '.join('%s→%s %d 处' % (a, dict(BUMP)[a], c) for a, c in counts.items()))

# 顺带处理 .muted/.htag 这类用 var 的极小数（若有 font-size:9 变体）
h = re.sub(r'font-size:\s*8px', 'font-size:10px', h)
h = re.sub(r'font-size:\s*9px', 'font-size:11px', h)

# ============ 4) 标题阶梯 ============
HEAD = [
 (r'(\.zh-hero h1\{font-size:)25px', r'\g<1>30px'),
 (r'(\.section-header h2\{font-size:)19px', r'\g<1>22px'),
 (r'(\.detail-panel h2\{font-size:)22px', r'\g<1>26px'),
 (r'(\.section-detail-header h2\{font-size:)20px', r'\g<1>22px'),
 (r'(\.card h3\{font-size:)14px', r'\g<1>15px'),
 (r'(\.sidebar-header h1\{font-size:)18px', r'\g<1>20px'),
]
hn = 0
for a, b in HEAD:
    h2, k = re.subn(a, b, h)
    if k:
        h = h2; hn += k
print('✅ 标题阶梯上调：%d 处' % hn)

# ============ 5) 6px 圆角 → 8px ============
r6 = len(re.findall(r'border-radius:\s*6px', h))
h = re.sub(r'border-radius:\s*6px', 'border-radius:8px', h)
print('✅ 圆角 6px → 8px：%d 处' % r6)

open(FP, 'w', encoding='utf-8').write(h)
print()
print('文件：%d → %d 字节（+%.1f KB）' % (orig_len, len(h), (len(h)-orig_len)/1024))

# 统计最终字号分布
sz = [int(m.group(1)) for m in re.finditer(r'font-size:\s*(\d+)px', h)]
from collections import Counter
c = Counter(sz)
print()
print('最终字号分布：')
for k in sorted(c):
    flag = ' ⚠️过小' if k < 11 else ''
    print('  %3dpx × %d%s' % (k, c[k], flag))
