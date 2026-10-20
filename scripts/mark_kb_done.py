# -*- coding: utf-8 -*-
"""更新 ai-growth 分区：方向 4（建个人知识库）标记为已完成，并补实际结构"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\index.html'
h = open(FP, encoding='utf-8').read()

OLD = ('<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🟡 方向 4：建个人知识库，让 AI 有依据</h4>')

NEW = ('<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">'
       '✅ 方向 4：建个人知识库，让 AI 有依据 <span style="font-size:11px;color:var(--green);'
       'font-weight:400">（2026-10-20 已建）</span></h4>'
       '<p style="margin:0 0 8px"><b>已落地</b>：桌面 <code>知识库</code> 目录，9 个文件 + 1 个质检脚本，'
       '7 条验收标准全部可执行。</p>'
       '<table class="data-table" style="margin:8px 0"><tr><th>目录</th><th>文件</th><th>装什么</th></tr>'
       '<tr><td><code>01-简历与投递</code></td><td>简历正文 · 投递记录</td><td>目标岗位、投递状态与反馈率</td></tr>'
       '<tr><td><code>02-项目复盘</code></td><td>个人网站 · 训练平台 · 求职作品集素材</td>'
       '<td>做过什么、当时怎么想、踩过什么坑</td></tr>'
       '<tr><td><code>03-AI观察</code></td><td>模型与产品判断 · 工具与工作流</td>'
       '<td>5 条带「改变结论条件」的判断</td></tr>'
       '<tr><td><code>04-生活训练</code></td><td>训练与饮食</td><td>60.65kg 基线、4+3 周计划、租房友好拉类方案</td></tr></table>'
       '<p style="margin:8px 0"><b>质检脚本</b>：<code>python _check_kb.py</code> → 34 项自动检查'
       '（四类覆盖 / 最后更新 / 超期 30 天 / README 索引 / H1+H2 / 隐私模式 / 文件名规范）。</p>'
       '<p style="margin:0 0 8px"><b>失败可见性已验证</b>：注入 5 类违规（缺日期 · 索引未收录 · 身份证号 · 卡号 · 文件名带空格），'
       '脚本全部抓住并返回退出码 1；清理后 34 项全过、退出码 0。</p>'
       '<p style="margin:0;font-size:13px;color:var(--text2)"><b>判断标准</b>（文档原话）：'
       '<b>「问它问题，它敢不敢给出来源」</b>——现在问「我的目标岗位是什么」，答案能指回 '
       '<code>01-简历与投递/简历正文.md</code> 的具体小节。</p></div>')

if OLD in h and '已建）' not in h:
    h = h.replace(OLD, NEW, 1)
    print('✅ 方向 4 已标记为已完成')
else:
    print('ℹ️  已更新或锚点未找到')

# 本周可做第 3 项标记完成
h = h.replace('<td>3</td><td><b>桌面建 <code>知识库</code> 文件夹</b>，先放 3 个 md：简历、网站更新规则、求职记录</td>',
              '<td>3</td><td><b>桌面建 <code>知识库</code> 文件夹</b>，先放 3 个 md '
              '<span style="color:var(--green)">（✅ 已完成，实际建了 9 个 + 质检脚本）</span></td>')

# 版本
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.33', h)
h = re.sub(r'detail_content\.js\?v=[\d.]+', 'detail_content.js?v=1.8.33', h)
open(FP, 'w', encoding='utf-8').write(h)

DFP = BASE + r'\daily_data.js'
d = open(DFP, encoding='utf-8').read()
d = d.replace('var SITE_VERSION = "1.8.32";', 'var SITE_VERSION = "1.8.33";')
d = re.sub(r'版本1\.8\.3[0-9]', '版本1.8.33', d)
open(DFP, 'w', encoding='utf-8').write(d)

h2 = open(FP, encoding='utf-8').read()
for t in ['2026-10-20 已建', '_check_kb.py', '失败可见性已验证', '34 项自动检查']:
    print('  含 %-24s %s' % (t, t in h2))
r = subprocess.run(['node', '--check', DFP], capture_output=True, text=True)
print('  daily_data 语法：', 'OK' if r.returncode == 0 else 'FAIL')
