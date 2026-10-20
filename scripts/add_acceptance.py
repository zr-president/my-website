# -*- coding: utf-8 -*-
"""在 ai-growth 分区新增「五、验收标准参考」
   回应「无法事前完美预判」这个真实问题：
   ① 通用四层模板（L1 有 / L2 对 / L3 边界 / L4 可复现）
   ② Skill 沉淀的 6 组验收标准（全部可测）
   ③ 个人知识库的 7 条验收标准
   ④ 探索型任务的三条过程标准（解决「边用边发现」）
"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\index.html'
h = open(FP, encoding='utf-8').read()

SEC5 = '''<h3>五、验收标准参考（可直接抄用）</h3>

<div class="callout warn" style="border-left:4px solid #f59e0b"><strong>⚠️ 先修正一个误解：验收标准 ≠ 事前预判需求</strong><br><br>
人在使用 AI 的过程中迸发新想法是常态，不可能把所有需求都想清楚再动手。<b>验收标准的作用不是「预判你要什么」，而是「界定什么算完成」</b>——这两件事完全不同。<br><br>
而且它是<b>分层的</b>：<b>结果标准</b>（做什么）适合重复性任务；<b>过程标准</b>（怎么做、什么时候停）适合探索性任务；<b>禁止标准</b>（不许出现什么）两类都适用，且<b>最容易事前穷举</b>。<br><br>
所以真正可执行的规则不是「事前想全」，而是：<b>同一条要求你说到第二次，就把它固化下来。</b>你不需要预判，只需要一个触发条件。</div>

<h4>5.1 通用四层模板（任何任务都能套）</h4>
<table class="data-table"><tr><th>层级</th><th>一句话问题</th><th>例子（以更新网站为例）</th><th>事前能写清楚吗</th></tr>
<tr><td><b>L1 有</b></td><td>交付物存在吗？</td><td>8 张要闻卡都在 · 17 个分区都有内容 · 页面能打开</td><td style="color:var(--green)">✅ 很容易</td></tr>
<tr><td><b>L2 对</b></td><td>内容正确吗？</td><td>站点日期 = 系统日期 · 数字与口径一致（60.65kg / 2600 kcal）</td><td style="color:var(--orange)">⚠️ 部分要事后核对</td></tr>
<tr><td><b>L3 边界</b></td><td>不该有的有没有？</td><td>没动归档键 · 没写个人金额 · 没引入外部图片 · 没用中文单引号</td><td style="color:var(--green)"><b>✅ 最容易穷举</b></td></tr>
<tr><td><b>L4 可复现</b></td><td>下次还能拿到吗？</td><td>同样指令跑 3 次，结构一致（分区数、检查项、版本规则不变）</td><td style="color:var(--orange)">⚠️ 要靠积累</td></tr></table>
<div class="callout"><strong>关键用法</strong>：不要一开始就试图写满 L2。<b>先把 L1 和 L3 写出来</b>——它们几乎可以穷举，而且立刻能减少返工。L2 靠每次踩坑补一条，L4 等规则稳定后自然成立。</div>

<h4>5.2 Skill 沉淀的验收标准（6 组，全部可测）</h4>
<table class="data-table"><tr><th>#</th><th>维度</th><th>验收标准</th><th>怎么测</th></tr>
<tr><td>1</td><td><b>触发准确</b><br><span style="font-size:11px;color:var(--text3)">边界明确</span></td>
<td>正向：≥5 条真实历史说法<b>全部命中</b><br>负向：≥3 条易混说法<b>全部不命中</b></td>
<td>拿 20 条历史对话回测<br>要求：命中 100% · 误触发 0</td></tr>
<tr><td>2</td><td><b>覆盖已知失败</b></td><td>过去每一次返工的具体原因，SKILL.md 里都有对应条款</td>
<td>逐条对照历史返工记录<br>缺一条就补一条</td></tr>
<tr><td>3</td><td><b>结构可复现</b></td><td>同一指令跑 3 次，产出的<b>结构和检查项完全一致</b>（内容可不同）</td>
<td>比对 3 次输出的骨架</td></tr>
<tr><td>4</td><td><b>失败可见</b></td><td>故意注入 1 个错误（如把日期改成昨天），Skill 必须<b>报错</b>而不是静默通过</td>
<td>注入错误测试（这是最重要的一项）</td></tr>
<tr><td>5</td><td><b>可维护</b></td><td>新增/修改一条规则，只需改<b>一处</b></td>
<td>改一次口径，看是否牵动多处</td></tr>
<tr><td>6</td><td><b>人工点 ≤2</b></td><td>跑完人工只需「看报告 + 决定是否推送」</td>
<td>数一下需要人做的动作数</td></tr></table>

<h4>5.3 个人知识库的 7 条验收标准</h4>
<table class="data-table"><tr><th>#</th><th>标准</th><th>可测方式</th></tr>
<tr><td>1</td><td><b>可检索</b></td><td>任取一个问题，10 秒内能定位到对应文件</td></tr>
<tr><td>2</td><td><b>可引用</b><br><span style="font-size:11px;color:var(--text3)">文档原话：敢不敢给出来源</span></td>
<td>让 AI 回答「我的目标岗位是什么」，它必须能指到「文件名 + 段落」，而不是说「根据资料」</td></tr>
<tr><td>3</td><td><b>原子</b></td><td>一个文件只讲一件事——简历和复盘不混写，投递记录不混进项目复盘</td></tr>
<tr><td>4</td><td><b>可维护</b></td><td>新增一条记录 ≤1 分钟，且<b>不需要改结构</b></td></tr>
<tr><td>5</td><td><b>有时效</b></td><td>每份文件顶部写「最后更新」，超过 30 天的标为待复核</td></tr>
<tr><td>6</td><td><b>覆盖四类</b></td><td>简历投递 / 项目复盘 / AI 观察 / 生活训练——<b>缺一类就是缺口</b></td></tr>
<tr><td>7</td><td><b>隐私边界</b></td><td>明确列出「不进去」的内容：薪资、身份证、健康细节、他人隐私。<b>因为 AI 会读到这些</b></td></tr></table>

<h4>5.4 探索型任务怎么验收（解决「边用边发现」）</h4>
<p>如果需求本身就是边聊边长的，<b>不要用结果标准，改用过程标准</b>：</p>
<table class="data-table"><tr><th>#</th><th>过程标准</th><th>为什么有效</th></tr>
<tr><td>1</td><td><b>每轮必须有增量</b>：一轮结束，必须能说出「这轮新发现了什么」</td>
<td>说不出 = 这轮白跑。它把「聊了很久但没进展」变成可检测的状态</td></tr>
<tr><td>2</td><td><b>说过第二次就固化</b>：同一条要求你说了第二遍，就写进 Skill 或清单</td>
<td><b>这是最关键的一条</b>——它解决「无法预判」问题的全部：你不需要预判，只需要一个触发条件</td></tr>
<tr><td>3</td><td><b>每轮结束问一句「要不要固化」</b></td>
<td>把「发现 → 沉淀」做成习惯动作，而不是靠记得</td></tr></table>

<div class="callout info"><strong>📌 为什么这样设计</strong><br>
文档里 Skill 的构建方式是「<b>评测驱动、失败优先</b>」——先跑一遍，记录不稳定、歧义、误触发的地方，<b>那些才是 Skill 要解决的真实缺口</b>。<br>
换句话说：<b>Skill 不是事前设计出来的，是从返工里长出来的。</b>这正好回应了「想法在过程中迸发」——迸发出来的想法，就是下一版 Skill 的输入。<br><br>
<b>所以顺序是</b>：先跑（发现问题）→ 记下（形成缺口）→ 说第二次（触发固化）→ 写进 Skill（沉淀）。<b>四步里没有一步需要你事前预判。</b></div>

'''

anchor = '<div class="callout info" style="margin-top:14px"><strong>📌 一条判断</strong>'
if '五、验收标准参考' in h:
    print('ℹ️  已存在，跳过')
elif anchor in h:
    h = h.replace(anchor, SEC5 + anchor, 1)
    open(FP, 'w', encoding='utf-8').write(h)
    print('✅ 已插入「五、验收标准参考」')
else:
    print('❌ 未找到锚点')
    i = h.find('📌 一条判断')
    print('  相近:', repr(h[i-80:i+60]) if i > 0 else '未找到')

# 版本
h2 = open(FP, encoding='utf-8').read()
h2 = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.31', h2)
h2 = re.sub(r'detail_content\.js\?v=[\d.]+', 'detail_content.js?v=1.8.31', h2)
open(FP, 'w', encoding='utf-8').write(h2)

DFP = BASE + r'\daily_data.js'
d = open(DFP, encoding='utf-8').read()
d = d.replace('var SITE_VERSION = "1.8.30";', 'var SITE_VERSION = "1.8.31";')
d = re.sub(r'版本1\.8\.3[0-9]', '版本1.8.31', d)
open(DFP, 'w', encoding='utf-8').write(d)

for t in ['五、验收标准参考', '同一条要求你说到第二次', 'Skill 不是事前设计出来的', '5.4 探索型任务', '隐私边界']:
    print('  含 %-30s %s' % (t, t in h2))
print('  文件 %.1f KB' % (len(h2.encode('utf-8')) / 1024))
r = subprocess.run(['node', '--check', DFP], capture_output=True, text=True)
print('  daily_data 语法：', 'OK' if r.returncode == 0 else 'FAIL')
