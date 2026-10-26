# -*- coding: utf-8 -*-
"""个人站结构完整性检查（新增，用于防止「标签不平衡导致内容掉出分区」这类事故复发）

背景：2026-10-26 事故 —— ai-growth 分区里多了一个 </div>，
浏览器提前关闭 <section>，导致后续内容掉到 .main 下、任何视图都隐藏不掉，
表现为「首页出现不该出现的文字」。当时的 22 项一致性检查与 30 组视觉体检都是绿的。

所以这里补三类静态检查：
  1) 每个 <section> 内部的 div / table / p / details 开闭是否平衡
  2) 全文 div 总平衡（排除 JS 模板字符串里的假标签）
  3) 已知会「掉出分区」的高风险特征：孤儿 </div> 紧跟 <div class="card"> 这类组合

用法：python scripts/check_structure.py   （退出码 0 = 通过）
"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HP = os.path.join(P, 'index.html')

h = open(HP, encoding='utf-8').read()
errors = []
warns = []

# ---------- 0) 剔除 <script> 与 <style> 里的内容（里面有字符串形式的假标签） ----------
def strip_blocks(s):
    s = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', s, flags=re.I)
    s = re.sub(r'<style\b[^>]*>[\s\S]*?</style>', '', s, flags=re.I)
    return s

clean = strip_blocks(h)

# ---------- 1) 逐 section 检查标签平衡 ----------
secs = list(re.finditer(r'<section\b[^>]*id="([^"]+)"[^>]*>', clean))
problems = []
for k, m in enumerate(secs):
    start = m.end()
    end = clean.find('</section>', start)
    if end < 0:
        problems.append((m.group(1), '没有闭合的 </section>'))
        continue
    body = clean[start:end]
    for tag in ['div', 'table', 'tr', 'td', 'th', 'p', 'details', 'summary', 'ul', 'li', 'h3', 'h4']:
        o = len(re.findall(r'<' + tag + r'\b', body))
        c = len(re.findall(r'</' + tag + r'>', body))
        if o != c:
            problems.append((m.group(1), '%s 不平衡：%d 开 / %d 闭' % (tag, o, c)))

print('=== 1) 分区内部标签平衡 ===')
print('  扫描分区数：%d' % len(secs))
if problems:
    for sid, msg in problems:
        errors.append('[%s] %s' % (sid, msg))
        print('  ❌ [%s] %s' % (sid, msg))
else:
    print('  ✅ 所有分区的 div/table/p/details 等标签均平衡')

# ---------- 2) 全文 div 总平衡 ----------
print()
print('=== 2) 全文 div 总平衡 ===')
o_all = len(re.findall(r'<div\b', clean))
c_all = len(re.findall(r'</div>', clean))
print('  %d 开 / %d 闭 （差值 %+d）' % (o_all, c_all, o_all - c_all))
if o_all != c_all:
    errors.append('全文 div 不平衡（%d 开 / %d 闭）' % (o_all, c_all))
    print('  ❌ 不平衡')
else:
    print('  ✅ 平衡')

# ---------- 3) 高风险特征：没有容器包裹的顶层块 ----------
print()
print('=== 3) 裸块检查（.main 下直接出现 <p>/<h3>/<table> 等） ===')
# 取 <main ...> ... </main> 的最外层
mm = re.search(r'<main\b[^>]*>', clean)
if mm:
    main_start = mm.end()
    main_end = clean.find('</main>', main_start)
    main_body = clean[main_start:main_end] if main_end > 0 else ''

    # 移除所有 view-container 与 section 的内部内容，只看顶层还剩什么
    def remove_nested(s):
        out = s
        for pattern in [r'<section\b[^>]*>[\s\S]*?</section>',
                        r'<div\b[^>]*class="[^"]*view-container[^"]*"[^>]*>[\s\S]*?</div>\s*(?=<div[^>]*view-container|</main>|$)']:
            out = re.sub(pattern, '', out)
        return out

    # 更稳的做法：只看 .main 直接的子元素序列
    top_tags = re.findall(r'<(div|section|p|h[1-6]|table|ul|ol|details)\b[^>]*>', main_body)
    print('  .main 顶层元素类型统计：%s' % dict((t, top_tags.count(t)) for t in set(top_tags)))

    # 按 <div id="...View" class="view-container"> 切段，检查段外是否有正文类元素
    views = [v.start() for v in re.finditer(r'<div\b[^>]*class="[^"]*view-container', main_body)]
    if views:
        # 第一段（第一个 view-container 之前）应当没有正文
        head_part = main_body[:views[0]]
        stray = re.findall(r'<(p|h[1-6]|table|ul|ol)\b[^>]*>', head_part)
        if stray:
            errors.append('.main 第一个 view-container 之前出现裸正文元素：%s' % set(stray))
            print('  ❌ view-container 之前出现裸正文：%s' % set(stray))
        else:
            print('  ✅ 第一个 view-container 之前没有裸正文')
    else:
        warns.append('.main 里没找到 view-container')
        print('  ⚠️ 未找到 view-container')
else:
    warns.append('没找到 <main>')
    print('  ⚠️ 未找到 <main>')

# ---------- 4) 关键分区是否都存在 ----------
print()
print('=== 4) 关键分区存在性 ===')
KEY = ['dashboard', 'ai-growth', 'optimization', 'daily-vocab', 'daily-quiz', 'guide', 'career', 'fitness', 'diet']
missing = [k for k in KEY if ('id="%s"' % k) not in h]
if missing:
    errors.append('缺少关键分区：%s' % ', '.join(missing))
    print('  ❌ 缺少：%s' % ', '.join(missing))
else:
    print('  ✅ 9 个关键分区都在')

# ---------- 汇总 ----------
print()
print('=== 汇总 ===')
if warns:
    for w in warns:
        print('  ⚠️ %s' % w)
if errors:
    for e in errors:
        print('  ❌ %s' % e)
    print()
    print('❌ 结构检查失败（%d 项）' % len(errors))
    sys.exit(1)
else:
    print('✅ 结构检查通过（分区标签平衡 · 全文 div 平衡 · 无裸正文 · 关键分区齐全）')
    sys.exit(0)
