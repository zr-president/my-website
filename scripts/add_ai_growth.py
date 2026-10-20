# -*- coding: utf-8 -*-
"""新增分区 ai-growth：AI 能力成长
   数据来源：桌面《资料》文件夹两份培训材料
   - AI办公系统搭建实战.pdf（55 页，CCE 实训营 · 每日互动 AI事业部 叶小健）
   - AI赋能办公效率倍增+数据分析.pptx（43 页，Richard Song）
   忽略其中第 26-40 页的「个知·智能工作站」产品推广
"""
import io, sys, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\index.html'
h = open(FP, encoding='utf-8').read()

SEC = '''<section id="ai-growth" class="section" data-search="AI 能力 成长 提示词 Skill Agent 工具 知识库 学习路径"><div class="section-header"><h2>🤖 AI 能力成长</h2><p>基于两份企业 AI 培训材料的提炼 · 我的能力定位与提升路径 · 2026-10-20</p></div>

<div class="callout info" style="margin-bottom:16px"><strong>📚 材料来源与取舍</strong><br>
两份材料：①《AI办公系统搭建实战》55 页（CCE 实训营 · 每日互动 AI事业部）②《AI赋能办公效率倍增+数据分析》43 页（Richard Song）。<br>
<b>已剔除</b>：第 26-40 页的「个知·智能工作站」产品介绍（混合云架构、四版本选型、会议纪要/公文写作等）——属厂商推广，对个人学习价值低。<br>
<b>真正有价值</b>：① 第 5-21 页「个人使用 AI 的五个能力阶段」② 第 41-54 页「AI 编程八步法」③ PPT 的提示词方法论与 Skill 设计规范。</div>

<h3>一、能力定位：我在五级里的哪一级</h3>
<table class="data-table"><tr><th>阶段</th><th>文档定义</th><th>我的现状</th><th>判定</th></tr>
<tr><td><b>01 会用 AI</b><br><span style="font-size:11px;color:var(--text3)">基础体验</span></td><td>尝试提问、写作和总结，了解 AI 能做什么</td><td>每天用豆包/DSH 提问、写内容、让 AI 改网站</td><td style="color:var(--green)"><b>✅ 已过</b></td></tr>
<tr><td><b>02 能用好 AI</b><br><span style="font-size:11px;color:var(--text3)">有效交互</span></td><td>说清目标与背景，通过多轮对话获得更合适的结果</td><td>能说清目标与背景，但<b>几乎不写验收标准</b>——所以经常需要「重新写」</td><td style="color:var(--orange)"><b>⚠️ 进行中</b></td></tr>
<tr><td><b>03 会组合工具</b><br><span style="font-size:11px;color:var(--text3)">拆解协作</span></td><td>拆解复杂任务，选择不同工具，组织能力接力</td><td>只用过 3 个工具（DSH / Claude Code / 豆包），<b>全在「对话 + 编程」同一类</b></td><td style="color:var(--red)"><b>❌ 未开始</b></td></tr>
<tr><td><b>04 会编排流程</b><br><span style="font-size:11px;color:var(--text3)">自动执行</span></td><td>串联步骤、设置规则，让重复任务按流程运行</td><td>每次更新网站都是<b>一次性交代</b>，没有 Skill、没有知识库、没有定时任务</td><td style="color:var(--red)"><b>❌ 未开始</b></td></tr>
<tr><td><b>05 能构建应用</b><br><span style="font-size:11px;color:var(--text3)">按需创造</span></td><td>借助 AI 编程，把自己的需求做成工具或应用</td><td>有个人网站 + 训练平台两个产品，但<b>构建由 AI 完成</b>，能力未闭环</td><td style="color:var(--orange)"><b>⚠️ 有成果无能力</b></td></tr></table>

<div class="callout warn" style="border-left:4px solid #f59e0b"><strong>🎯 判定：真实位置在 02 和 03 之间。</strong><br><br>
我有 05 的「成果」，但没有 05 的「能力」——<b>这是最需要警惕的错觉：拥有产品 ≠ 拥有构建能力</b>。<br>
网站和训练平台确实在跑，但每一次需求 → 代码的转换都不是我完成的。面试里如果被追问「这个功能你怎么实现的」，诚实答案是「我定义需求、验收结果」。<br><br>
<b>好消息</b>：文档里有一句关键判断——「<b>这五级台阶，个人练三个月就能走完</b>」。02→03→04 不需要天赋，只需要换方法。</div>

<h3>二、文档精华：值得带走的 9 条</h3>
<table class="data-table"><tr><th>#</th><th>要点</th><th>原话 / 说明</th><th>对我的用处</th></tr>
<tr><td>1</td><td><b>提示词六维度，第六维度最值钱</b></td>
<td>① 角色与受众 ② 任务目标 ③ 背景与素材 ④ 具体要求（含「不要什么」）⑤ 输出形式 <b>⑥ 约束与判断标准</b><br><span style="font-size:11px;color:var(--text3)">「这条最难写，也最值钱」</span></td>
<td>我长期只写 1-5，缺 6 —— 这正是反复返工的根源</td></tr>
<tr><td>2</td><td><b>不在于写得长，在于把影响结果的要求说清</b></td>
<td>反例「帮我画一只猫」：结果像开盲盒，品种、动作、场景全由模型默认值决定，<b>无法复现</b></td>
<td>可复现 = 下次还能拿到同样质量的结果</td></tr>
<tr><td>3</td><td><b>会组合工具的三件事</b></td>
<td>① 会拆任务 ② 会选工具 ③ 会衔接成果<br><span style="font-size:11px;color:var(--text3)">「关键不在于用了多少工具，而在于能否组合成完整成果」</span></td>
<td>我现在是一个工具做所有事，没有「拆」的意识</td></tr>
<tr><td>4</td><td><b>Agent / Skill / CLI / MCP 四层分工</b></td>
<td>Agent = 执行任务的助理；<b>Skill = 助理的工作手册</b>；CLI = 命令入口；MCP = 通用连接规范<br><span style="font-size:11px;color:var(--text3)">「助理负责执行，手册提供方法，工具入口让它能动手——不一定同时用上」</span></td>
<td>这是 2026 年 AI 产品岗最硬的结构性知识</td></tr>
<tr><td>5</td><td><b>知识库价值不在「记得多」，在「随时调得出来」</b></td>
<td>三个条件：<b>本地</b> / <b>Markdown</b> / <b>Agent 可读</b><br>判断好坏只一个问题：<b>「问它问题，它敢不敢给出来源」</b></td>
<td>我目前让 AI「每次从零开始」，因为没有知识库</td></tr>
<tr><td>6</td><td><b>先想清楚，再说清楚</b></td>
<td>自己想清楚：谁来用 / 解决什么 / 做到哪<br>跟 AI 说清楚：功能 / 规则 / 边界 / 验收标准<br><span style="font-size:11px;color:var(--text3)">「最怕的不是 AI 做不出来，而是我们自己也没想清楚」</span></td>
<td>我常在没有「做到哪」的情况下就开始要结果</td></tr>
<tr><td>7</td><td><b>评测驱动：先建「无 Skill」基线</b></td>
<td>先不用 Skill 直接跑一遍，记录<b>不稳定、不可复现、歧义、误触发</b>的地方——这些才是 Skill 要解决的真实缺口。<br>Skill 五个设计标准里最重要的是<b>边界明确</b>：「模型最容易犯的错误不是『不知道怎么做』，而是『不知道什么时候该做』」</td>
<td>这条直接可用：把每次返工原因记下来，就是 Skill 的需求清单</td></tr>
<tr><td>8</td><td><b>反馈要给「现象 + 预期」，不是「感觉不对」</b></td>
<td>❌「感觉不太对」→ 要来回好几轮才对齐<br>✅「<b>连续点击两次提交，出现了两条周报。预期只保存一条。</b>」</td>
<td>我多数反馈属于前者，这让 AI 只能猜</td></tr>
<tr><td>9</td><td><b>AI 味的三特征与判断标准</b></td>
<td>布局雷同 / 重点不清 / 业务细节不足<br><span style="font-size:11px;color:var(--text3)">「像不像样是次要的——能不能一眼看出业务重点，才是分水岭」</span></td>
<td>做作品集和产品原型时用来自检</td></tr></table>

<h3>三、五个提升方向</h3>

<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🔴 方向 1：把「验收标准」写进每一次交代（补第六维度）</h4>
<p style="margin:0 0 8px"><b>现状</b>：我会说「更新我的个人网站内容」——只有目标，没有验收。<br>
<b>升级版</b>：「更新网站内容。<b>验收标准</b>：① 站点日期 = 系统真实日期 ② 17 个分区的 summary/trend/tip 三个字段都必须有当日日期 ③ 评分表要含最新发布的模型 ④ <b>不要动归档键</b>（那是历史记录）。」</p>
<p style="margin:0;font-size:13px;color:var(--text2)"><b>收益</b>：现在每轮至少一次返工（「今日行动没更新」「Opus 5.5 没在表里」都是我事后发现的）。写清验收 = 把发现问题的环节从「事后」移到「事前」。</p></div>

<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🔴 方向 2：工具图谱从 3 个补到 6 类</h4>
<table class="data-table" style="margin:8px 0"><tr><th>类别</th><th>现在</th><th>缺的代表</th><th>具体用途</th></tr>
<tr><td><b>对话 / 通用</b></td><td style="color:var(--green)">✅ 豆包</td><td>—</td><td>日常问答、初稿</td></tr>
<tr><td><b>编程 Agent</b></td><td style="color:var(--green)">✅ DSH / Claude Code</td><td>—</td><td>改网站、写脚本、做工具</td></tr>
<tr><td><b>信息检索</b></td><td style="color:var(--red)">❌</td><td>Perplexity / 秘塔</td><td>查行业数据、竞品动态，替代「凭印象」</td></tr>
<tr><td><b>图像生成</b></td><td style="color:var(--red)">❌</td><td>即梦 / 可画</td><td>作品集配图、公众号头图、原型视觉</td></tr>
<tr><td><b>数据分析</b></td><td style="color:var(--red)">❌</td><td>Excel + AI / 代码解释器</td><td>跑训练平台的数据题、做留存/漏斗分析</td></tr>
<tr><td><b>自动化</b></td><td style="color:var(--red)">❌</td><td>n8n / 系统定时任务</td><td>网站每日更新、投递提醒、周报生成</td></tr></table>
<p style="margin:6px 0 0;font-size:13px;color:var(--text2)"><b>原则</b>（来自文档）：每类<b>只需要会一个</b>。重点不是多，而是建立「什么任务该交给哪一类」的判断。目标公司面试里问「你用什么工具」时，能说出 6 类 > 能说出 1 个工具的 6 个功能。</p></div>

<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🟡 方向 3：把重复交代沉淀成 Skill（最大杠杆）</h4>
<p style="margin:0 0 8px"><b>事实</b>：我每次更新网站都要重新说一遍要求——日期必须最新、17 个分区都要刷、口径要统一、不要写个人金额。这些规则<b>已经稳定了三个月</b>，却每周重新口述一次。</p>
<p style="margin:0 0 8px"><b>该做</b>：写一个 <code>weekly-site-update</code> 的 SKILL.md，把规则固化下来：<br>
· <b>前置</b>：先读系统时钟（这是踩过的坑）<br>
· <b>刷新</b>：17 分区的 summary / trend / tip 三字段都要有当日日期<br>
· <b>检查</b>：22 项一致性 + 逐字段审计<br>
· <b>口径</b>：体重 60.65kg、训练日 2600 kcal、蛋白 130-140g<br>
· <b>禁止</b>：不改归档键、不写个人金额、不使用中文单引号</p>
<p style="margin:0;font-size:13px;color:var(--text2)"><b>方法论直接用文档的</b>：SKILL.md 用 YAML front matter + Markdown；<b>边界要写正反两面</b>（Use when: 用户说「更新网站」/ Don't use: 只是想改一个错别字）；<b>评测驱动</b>——把过去每次返工的原因记下来，那就是 Skill 的第一版需求。</p></div>

<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🟡 方向 4：建个人知识库，让 AI 有依据</h4>
<p style="margin:0 0 8px"><b>现状</b>：我现在的 AI 是「每次都从零开始的助手」——它不知道我的简历、不知道我的项目复盘、不知道我上次为什么那样决策。所以我只能每次重新复述背景。</p>
<p style="margin:0 0 8px"><b>该做</b>：桌面建一个 <code>知识库</code> 目录，全部用 Markdown，放四类：<br>
· 简历与投递记录（哪家、什么岗位、结果）<br>
· 项目复盘（做了什么、当时怎么想、结果如何）<br>
· AI 观察笔记（模型发布、产品判断）<br>
· 生活与训练记录（可选）<br>
<b>收益</b>：AI 能直接读这些文件，不用每次复述；面试前可以让我基于真实记录生成 STAR 案例。</p>
<p style="margin:0;font-size:13px;color:var(--text2)"><b>判断标准</b>（文档原话）：<b>「问它问题，它敢不敢给出来源」</b>——如果 AI 的回答能指回某个 md 文件和具体段落，说明知识库建对了。</p></div>

<div class="card" style="margin-bottom:12px"><h4 style="margin:0 0 8px">🟢 方向 5：从「看结果」升级为「定标准」（评委能力）</h4>
<p style="margin:0 0 8px"><b>好消息</b>：我其实已经在做——会质疑「今日行动没更新」、会发现「Opus 5.5 不在表里」、会追问「启动器到底有没有用」。这些是<b>评委能力</b>的雏形。</p>
<p style="margin:0 0 8px"><b>该做的升级</b>：把「事后质疑」变成「事前清单」。为每类任务列一张验收清单（网站更新 / 简历 / 作品集 / 数据分析），交付时逐条打勾。<b>清单本身是可复用的资产</b>。</p>
<p style="margin:0;font-size:13px;color:var(--text2)"><b>文档里最扎心的一条观察</b>（第 50 页）：CCE 现场几位技术开发人员分享时，<b>15-20 分钟里讲的全是「怎么调研场景、怎么和业务沟通需求、怎么拆解需求」</b>，几乎不谈 AI 写代码；有人说「AI 写的代码压根没细看过」。<br>
结论：<b>把需求沟通和拆解做扎实，写代码反而是最简单的一步。</b> 这正好说明——我的方向不是学写代码，是把需求能力和验收能力做到前面。</p></div>

<h3>四、本周可做（3 件事）</h3>
<table class="data-table"><tr><th>#</th><th>动作</th><th>成本</th><th>验收标准</th></tr>
<tr><td>1</td><td><b>下一次交代任务时，加一段「验收标准」</b>（至少 3 条）</td><td>0 元 / 5 分钟</td><td>该轮任务不需要「重新写」就达到预期</td></tr>
<tr><td>2</td><td><b>装一个信息检索工具</b>（Perplexity 或秘塔），用它查一次本周 AI 动态</td><td>0 元 / 20 分钟</td><td>能对比出「它给的来源」vs「豆包凭印象」的差别</td></tr>
<tr><td>3</td><td><b>桌面建 <code>知识库</code> 文件夹</b>，先放 3 个 md：简历、网站更新规则、求职记录</td><td>0 元 / 30 分钟</td><td>让 AI 读这 3 个文件后，能不复述背景就答对「我的目标岗位是什么」</td></tr></table>

<div class="callout info" style="margin-top:14px"><strong>📌 一条判断</strong>：文档说「五级台阶个人练三个月就能走完」。但<a href="#optimization" style="color:var(--accent)">优化日记</a>里堆积的 12 条建议告诉我另一件事——<b>真正卡住人的不是台阶太高，是每次都在原地把同一件事重新做一遍</b>。<br>
所以本轮最该做的不是「学更多工具」，而是<b>方向 3（把规则沉淀成 Skill）</b>：它一次性把你未来所有重复交代都省掉。</div>
</section>

'''

# 插入到 learning 之后（gaming 之前）
anchor = '<section id="gaming" class="section"'
if anchor in h:
    h = h.replace(anchor, SEC + anchor, 1)
    print('✅ 已插入 ai-growth 分区（learning 之后）')
else:
    print('❌ 未找到 gaming 锚点')

# 侧栏导航加一项
nav_old = '<a href="#learning">🎓 学习区</a><a href="#skill-radar">🧭 技能雷达</a>'
nav_new = '<a href="#learning">🎓 学习区</a><a href="#ai-growth">🤖 AI 能力成长</a><a href="#skill-radar">🧭 技能雷达</a>'
if nav_old in h:
    h = h.replace(nav_old, nav_new, 1)
    print('✅ 侧栏已加「🤖 AI 能力成长」')
else:
    print('❌ 未找到侧栏锚点')

# 版本
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.30', h)
h = re.sub(r'detail_content\.js\?v=[\d.]+', 'detail_content.js?v=1.8.30', h)
open(FP, 'w', encoding='utf-8').write(h)
print('✅ index.html 已写入（%.1f KB）' % (len(h.encode('utf-8')) / 1024))

# 版本号同步到 daily_data
DFP = BASE + r'\daily_data.js'
d = open(DFP, encoding='utf-8').read()
d = d.replace('var SITE_VERSION = "1.8.29";', 'var SITE_VERSION = "1.8.30";')
d = re.sub(r'版本1\.8\.2[0-9]', '版本1.8.30', d)
open(DFP, 'w', encoding='utf-8').write(d)
print('✅ SITE_VERSION → 1.8.30')

r = subprocess.run(['node', '--check', DFP], capture_output=True, text=True)
print('daily_data 语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
