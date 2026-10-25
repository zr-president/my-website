# -*- coding: utf-8 -*-
"""补首屏 CTA 的公开作品集入口（缩进为 Tab，用正则定位）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()

if h.count('portfolio.html') >= 2:
    print('ℹ️  首屏 CTA 已有 portfolio 链接')
else:
    # 匹配：<缩进><button class="zh-cta primary" onclick="zh_goObs()">…</button>
    m = re.search(r'([ \t]*)<button class="zh-cta primary" onclick="zh_goObs\(\)">[^<]*</button>', h)
    if not m:
        print('❌ 仍未匹配')
        i = h.find('zh_goObs')
        print('  附近：', repr(h[i - 160:i + 120]) if i > 0 else '未找到')
    else:
        indent = m.group(1)
        link = (indent + '<a class="zh-cta primary" href="portfolio.html" target="_blank" rel="noopener" '
                'style="text-decoration:none;background:linear-gradient(135deg,var(--green),var(--accent))">'
                '📄 公开作品集（投递用 · 可打印）</a>\n')
        h = h[:m.start()] + link + h[m.start():]
        open(FP, 'w', encoding='utf-8').write(h)
        print('✅ 首屏 CTA 已加（缩进长度 %d）' % len(indent))
        print('   插入内容：' + link.strip()[:110] + '…')

h2 = open(FP, encoding='utf-8').read()
print()
print('  portfolio.html 出现次数：', h2.count('portfolio.html'))
print('  含「公开作品集」：', h2.count('公开作品集'), '处')
