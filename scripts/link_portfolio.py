# -*- coding: utf-8 -*-
"""给个人站加「公开作品集」入口（首屏 CTA + 侧栏「关于求职」组）"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()
changed = []

# ---- 1) 首屏 CTA：加「公开作品集」按钮（放最前，这是给陌生人看的第一入口） ----
OLD_CTA = '  <button class="zh-cta primary" onclick="zh_goObs()">📚 开始探索（看今日内容）</button>'
NEW_CTA = ('  <a class="zh-cta primary" href="portfolio.html" target="_blank" rel="noopener" '
           'style="text-decoration:none;background:linear-gradient(135deg,var(--green),var(--accent))">📄 公开作品集（投递用 · 可打印）</a>\n'
           + OLD_CTA)
if OLD_CTA in h and 'portfolio.html' not in h:
    h = h.replace(OLD_CTA, NEW_CTA, 1)
    changed.append('首屏 CTA')
elif 'portfolio.html' in h:
    print('ℹ️  已有 portfolio 链接')
else:
    print('⚠️ 首屏 CTA 锚点未匹配')

# ---- 2) 侧栏「关于求职」组：加一项 ----
OLD_NAV = ('<a href="#career">求职中心</a><a href="#mock-interview">模拟面试舱</a></div>')
NEW_NAV = ('<a href="#career">求职中心</a><a href="portfolio.html" target="_blank" rel="noopener">'
           '公开作品集 ↗</a><a href="#mock-interview">模拟面试舱</a></div>')
if OLD_NAV in h and h.count('portfolio.html') < 2:
    h = h.replace(OLD_NAV, NEW_NAV, 1)
    changed.append('侧栏导航')
elif '公开作品集' in h:
    print('ℹ️  侧栏已有入口')
else:
    print('⚠️ 侧栏锚点未匹配')

# ---- 3) 版本同步 → 1.8.38 ----
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.38', h)
h = re.sub(r'detail_content\.js\?v=[\d.]+', 'detail_content.js?v=1.8.38', h)
h = re.sub(r'img_style\.js\?v=[\d.]+', 'img_style.js?v=1.8.38', h)
h = re.sub(r'personal_config\.js\?v=[\d.]+', 'personal_config.js?v=1.8.38', h)

open(FP, 'w', encoding='utf-8').write(h)
print('✅ 已加：' + ('、'.join(changed) if changed else '无改动'))

# ---- 4) 更新 daily_data 版本与说明 ----
DP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(DP, encoding='utf-8').read()
d = d.replace('var SITE_VERSION = "1.8.37";', 'var SITE_VERSION = "1.8.38";')
d = re.sub(r'版本1\.8\.3[0-9]', '版本1.8.38', d)
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.38。10/25 新增【公开作品集】独立页面 portfolio.html（方案里的 S09）：'
       '面向面试官/HR 的对外版本，与个人站分离 —— 单页包含 定位 + 4 个可核对数字 + '
       '3 个案例（个人网站 / 训练平台 / 用另一个模型做方案评审）+ 一条判断练习 + 6 行能力证据表 + 联系方式。'
       '采用 A4 打印样式，右下角按钮可直接存为一页 PDF，投递时作为附件。'
       '首屏 CTA 与侧栏「关于求职」组均已加入口。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
open(DP, 'w', encoding='utf-8').write(d)
print('✅ 版本 → 1.8.38')

r = subprocess.run(['node', '--check', DP], capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print('daily_data 语法：', 'OK' if r.returncode == 0 else 'FAIL')

h2 = open(FP, encoding='utf-8').read()
print()
for k in ['portfolio.html', '公开作品集', '1.8.38']:
    print('  含 %-16s %s' % (k, k in h2))
print('  portfolio 链接数：', h2.count('portfolio.html'))
