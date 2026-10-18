# -*- coding: utf-8 -*-
"""重写 ai-track（REA / DeepSeek V4.1-Flash-1017 / Meta Muse Wonder）与 news
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
TODAY = '2026-10-18'
d = open(FP, 'r', encoding='utf-8').read()


def js(o):
    return json.dumps(o, ensure_ascii=False)


ai = {
 "verdict": ("🎯 <b>10/18 三条结论（AI 动态）</b>：<br><br>"
   "① <b>REA（Reverse Engineer Anything）</b>——GitHub 周榜第一（29 万星·周增 24.9 万），本质是 <b>MCP 服务器</b>，"
   "把应用/网页/二进制的逆向分析能力交给 Agent。<b>结论：理解优先，使用谨慎</b>——它不属于你的场景，"
   "但是「Agent 能力扩展」最好的教学案例。<br><br>"
   "② <b>DeepSeek-V4.1-Flash-1017</b>（10/17 上线）——<b>你正在用的就是它</b>（模型名仍是 deepseek-flash，旧调用自动升级）。"
   "代码与 Agent 基准大幅提升，且同时降延迟与输出长度。<br><br>"
   "③ <b>Meta Muse Wonder / Full</b>（10/12）——AA 智能指数 56（六周涨 8 分），"
   "SWE-Marathon 57.5% 超越 Opus 5.5 与 GPT-6 Astra，幻觉率仅 23%。<b>前沿模型重回三强格局</b>。"),

 "summary": ("<b>一、REA：一个 MCP 如何让 Agent「看懂」软件</b><br>"
   "REA 全称 <b>Reverse Engineer Anything</b>（仓库 <code>morluto/rea</code>，TypeScript）。"
   "截至 10/17，GitHub 总星 <b>29.1 万</b>、周增 <b>24.9 万</b>，位列 GitHub Trending weekly 第一；npm 与 Release 版本为 <b>6.4.0</b>。<br><br>"
   "它不是「输入软件就还原源码」的魔法。真实链路是：<b>Agent 提出问题 → REA 调用本地分析工具取证 → Agent 解释行为</b>。"
   "官方要求结果必须包含<b>观察依据、推断、以及未解决的问题</b>三部分——这一点很关键，它把「猜测」和「证据」分开了。<br><br>"
   "支持的目标：原生二进制（借 Hopper/Ghidra/IDA 读伪代码与调用关系）、JavaScript/Electron 应用、.NET 程序集、"
   "网站（需 Chrome 系浏览器）、Android APK（需 JADX + JDK）、固件、网络抓包、进程行为。"
   "<b>其中静态 JS 与 .NET 检查门槛最低</b>——不运行目标、不装原生分析引擎就能开始。<br><br>"
   "<b>三层分工</b>（这是最值得学的部分）：<b>MCP</b> 负责暴露分析工具给 Agent；"
   "<b>Skill</b> 是调查流程说明，教 Agent 何时调用哪个工具、怎么看证据；<b>CLI</b> 让人不经过 Agent 也能在终端直接分析。"
   "注意：只装 Skill 不会自动获得 MCP 工具，这两件事是分开的。<br><br>"

   "<b>二、DeepSeek-V4.1-Flash-1017（10/17 上线）</b><br>"
   "已同步上线网页端、App 与 API。API 模型名<b>仍是 <code>deepseek-flash</code></b>，旧名 <code>deepseek-v4-flash</code> 会自动路由到新版，"
   "<b>不需要改接口地址</b>。1M 上下文、最高 384K 输出，支持图像理解与工具调用。<br><br>"
   "官方基准（对上一版）：HLE <b>42.6</b>(+5.8)、Terminal-Bench 4.0 <b>42.3</b>(+11.1)、ProgramBench <b>29.1</b>(+8.8)、"
   "DeepSWE v1.1 <b>77.0</b>(+2.8)、NL2Repo <b>68.2</b>(+2.8)、Automation-Bench <b>60.5</b>(+5.7)。"
   "官方强调的不只是分数，而是<b>同时减少了运行时间与输出长度</b>，称为「性能—费用帕累托改进」。<br><br>"
   "最容易被感知的能力是「<b>许愿式编程</b>」：用带自反馈的强化学习，让模型写完第一版代码后自己检查、发现问题、再修改，"
   "而不是只生成一次就结束。官方演示了故宫 3D 场景、网页赛车、Godot 复刻《传送门 2》等案例。"
   "<b>看点不是「一句话替代开发团队」，而是任务链被拉长了</b>：需求理解 → 规划 → 生成 → 运行 → 检查 → 修复可以连续发生。<br><br>"
   "配套：<b>DeepSeek Harness 升到 0.2.1-rc.2</b>（10/17），已适配新模型与 <b>Search / Fetch API</b>"
   "（<code>/v1/tools/search</code>、<code>/v1/tools/fetch</code>，Search 支持 site:/lang:/after:/before: 操作符；"
   "每千次成功请求 ¥5，<b>2026-11-01 00:00 前通过 Harness 调用暂不收费</b>，账户级 5 QPS）。<br><br>"

   "<b>三、Meta Muse Wonder / Muse Wonder Full（10/12）</b><br>"
   "两档旗舰，均支持 1M 上下文、原生多模态（文本/高分辨率图/超长视频/连续音频），"
   "搭载 <b>Active Memory</b>（长会话自动保留偏好与约束）与 <b>Active Focus</b>（遇阻主动换策略、出错自检、实时调整计划）。"
   "诞生于 Meta 吉瓦级算力的 Prometheus 数据中心，经 14 个月基础设施重构，用大量长周期、多文件真实编程任务强化训练。<br><br>"
   "第三方测评（Artificial Analysis / Vals AI，10-12 数据）：AA 智能指数 Full <b>56</b>（与 Claude Sonnet 5.5 并列）、"
   "Wonder <b>52</b>；上代 Spark 1.3 为 48，<b>六周涨 8 分</b>。"
   "SWE-Marathon 完成率：Full <b>57.5%</b>、Wonder 53.1%，对比 Opus 5.5 46.3%、GPT-6 Astra 42.5%。"
   "Terminal-Bench 4.0：Full <b>57%</b>（上代仅 33%，提升 24pt）。"
   "法律专项 Harvey LAB-AA：Full <b>13.1</b> 分，是 Opus 5.5（4.2）的 3.1 倍。<br><br>"
   "<b>幻觉率是它最特别的一项</b>：Full <b>23%</b>，远低于 Astra 51%、Opus 59%。"
   "但代价是知识指数仅 30（Astra 43、Opus 46）——它更倾向「不确定就不答」。"
   "所以判断标准是：<b>要高置信度选它，要广度知识仍选 Opus/Astra</b>。"),

 "trend": ("<b>REA vs Jev：两者根本不是同一层的东西</b><br><br>"
   "很多人会把它们放在一起比，因为都「和 AI 有关、都叫新东西」。但它们的层次完全不同：<br><br>"
   "<table class=\"data-table\"><tr><th>维度</th><th>REA</th><th>Jev</th></tr>"
   "<tr><td><b>所在层次</b></td><td><b>工具层</b>（MCP 服务器）</td><td><b>模型层</b>（决策模型）</td></tr>"
   "<tr><td><b>解决什么</b></td><td>让 Agent 能<b>取证</b>：读应用、网页、二进制</td><td>让输出变成<b>结构化判断</b></td></tr>"
   "<tr><td><b>输出形态</b></td><td>证据 + 追踪路径（自然语言 + 证据位置）</td><td><code>choice</code> / <code>score</code> / <code>probability</code>（JSON）</td></tr>"
   "<tr><td><b>接入方式</b></td><td>挂到 Codex / Claude Code 等 Agent 上</td><td>嵌进自己的后端代码</td></tr>"
   "<tr><td><b>前提条件</b></td><td>目标需自有或获授权；本机运行分析</td><td>需要有大量判断环节的后端系统</td></tr>"
   "<tr><td><b>对幻觉的态度</b></td><td>不承诺零幻觉，但强制列出<b>证据与未知项</b></td><td>结构性零幻觉（不出 schema），但<b>判断不保证正确</b></td></tr>"
   "<tr><td><b>依赖成本</b></td><td>原生分析需 Hopper/Ghidra/IDA；JS/.NET 静态分析零依赖</td><td>只要 API Key + 后端</td></tr>"
   "<tr><td><b>对你的价值</b></td><td>理解 <b>MCP 三层分工</b>（求职高频设计题）</td><td>当前无场景，继续观察</td></tr></table><br>"
   "<b>一句话区分：REA 给 Agent 加「眼睛」，Jev 给模型换「大脑」。</b><br><br>"
   "<b>从 GitHub 周榜（10/17）看更大的趋势</b>：<br>"
   "榜单一 REA，榜单六 <code>mattpocock/skills</code>（29.4 万星·可组合 Agent Skills），"
   "榜单八 <code>context-mode</code>（3 万星·为 Agent 优化上下文窗口的 MCP + Hook），"
   "榜单十 <code>anthropics/claude-plugins-official</code>（4 万星·官方插件目录）。"
   "这组项目共同说明一件事：<b>Agent 的竞争点正在从「能不能写一段代码」移到「能不能稳定完成一套工程动作」</b>。"
   "而这个能力的组织方式已经收敛成三层——<b>MCP 提供工具、Skill 提供流程、CLI 提供人工入口</b>。"
   "这是 2026 下半年 AI 产品设计最值得记住的结构。"),

 "tip": ("<b>我的建议：学 REA 的思路，别急着上 REA 的工具</b><br><br>"
   "<b>✅ 值得学的部分（成本低、回报高）</b><br>"
   "① <b>MCP / Skill / CLI 三层分工</b>——这是 AI 产品岗的高频设计题：什么该做成工具、什么该写成流程说明、"
   "什么该留给人直接用。REA 的 README 把这三层讲得很清楚，是现成的教材。<br>"
   "② <b>「证据 + 推断 + 未知项」的输出规范</b>——它解决的是 AI 输出最让人不放心的点：分不清哪句是事实、哪句是猜的。"
   "这个规范可以直接搬到你自己的产品设计里。<br>"
   "③ <b>能力边界的诚实标注</b>——REA 明确写了「不同目标需要的引擎不同」「不保证结论完整」。"
   "这种写法本身就是好的产品文档示范。<br><br>"

   "<b>⚠️ 现在不建议真正上手的原因</b><br>"
   "① <b>你没有逆向需求</b>——你目前的项目是纯前端，没有需要分析二进制或第三方应用的场景。<br>"
   "② <b>法律边界</b>——官方免责声明限定在「自有或获授权软件」的分析。这个边界一旦模糊，风险不在技术层面。<br>"
   "③ <b>隐私</b>——REA 在本机分析，但<b>分析结果会进入 Agent 的对话上下文</b>，数据如何流转取决于模型服务商的政策。<br>"
   "④ <b>依赖重</b>——原生二进制分析要装 Hopper/Ghidra/IDA，和你「能用就行」的取向不符。<br><br>"

   "<b>🎯 如果只想花 15 分钟验证一下（推荐这个）</b><br>"
   "用<b>自己项目的已解包 JavaScript / Electron 应用</b>做静态检查，不需要任何原生引擎：<br>"
   "<code>npx rea-agents@latest setup</code>（选 Codex，注意向导会修改配置，会先给 dry-run 计划）<br>"
   "<code>npx -y rea-agents@latest analyze-javascript-application /绝对路径 --json</code><br>"
   "要求：Node.js 22.19+ / 24.11+ / 26+。结果如果很大，先存文件再看摘要，<b>不要把完整分析一次塞进对话</b>。<br><br>"

   "<b>📌 顺带一个立刻能用的结论：你已经在用新模型了。</b><br>"
   "DeepSeek-V4.1-Flash-1017（10/17）对已有调用是<b>自动生效</b>的（模型名仍是 <code>deepseek-flash</code>），"
   "不需要改任何配置。所以「要不要升级」这个问题不存在——<b>要判断的是要不要改用法</b>："
   "既然它更擅长长任务链，那就可以把以前拆成多轮的任务合并成一轮交给它。<br><br>"
   "<b>还有一个省钱的点</b>：deepseek-flash 高峰时段（工作日 9-12、14-18）输入 ¥2/输出 ¥8，<b>闲时减半</b>。"
   "批量任务排到晚上或周末跑，直接省一半。"),

 "reasoning": ("为什么这三件事值得一起看，而 REA 值得优先理解：<br><br>"
   "<b>① 它们分别代表三个不同层面的变化。</b>"
   "DeepSeek 的更新是<b>模型层</b>（同一个模型更强、更快、更省）；"
   "Meta Muse Wonder 是<b>竞争格局层</b>（前沿模型从两家独大回到三家竞争，且各有明确长板）；"
   "REA 是<b>工具/接入层</b>（Agent 能做什么，取决于它能调用什么工具、怎么组织流程）。"
   "只看模型会误判——因为模型能力已经足够，瓶颈正在往「工具与流程」移动。<br><br>"
   "<b>② GitHub 周榜是比发布会更早的信号。</b>"
   "前十名里有五个是 Agent 工具链项目（REA、skills、context-mode、claude-plugins-official、diagram-design）。"
   "一次发布会说明「某家公司打算做什么」，而榜单说明「开发者已经在用什么」。"
   "对求职者来说，后者的信息量更大——面试官问的往往是「你实际用过什么、怎么组织的」。<br><br>"
   "<b>③ 为什么 REA 优先于 Jev。</b>"
   "Jev 的适用前提是「你有一个带后端的、判断密集的系统」，你现在没有；"
   "而 REA 揭示的<b>三层分工</b>是任何 AI 产品都要面对的架构问题，"
   "你即便不装它，也必须理解它——这正是我上次说的「理解的价值 &gt; 使用的价值」，"
   "只是这一次 REA 的理解价值更高、学习成本更低。<br><br>"
   "<b>④ 一个容易被忽略的共同点：都在强调「证据」。</b>"
   "REA 强制输出证据与未知项；Muse Wonder 用「不确定就拒答」把幻觉率压到 23%；"
   "DeepSeek 把「减少输出长度」作为与分数提升并列的目标。"
   "三件事指向同一个方向：<b>AI 产品的评价标准，正在从「答案看起来对不对」转向「这个答案凭什么可信」</b>。"
   "理解这一条，比记住任何单个版本号都有用。")
}
ai["updated"] = TODAY


def replace_section(text, key, obj, region=None):
    target = text
    off = 0
    if region is not None:
        target, off = region[0], region[1]
    pat = re.compile(r'((?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\{)([\s\S]*?)(\n  \})')
    m = pat.search(target)
    if not m:
        print('  ❌ 未找到:', key); return text, False
    parts = []
    for f in ['verdict', 'summary', 'trend', 'tip', 'reasoning', 'updated']:
        if obj.get(f):
            parts.append('    %s: %s' % (f, js(obj[f])))
    new_seg = m.group(1) + '\n' + ',\n'.join(parts) + m.group(3)
    if region is not None:
        new_target = target[:m.start()] + new_seg + target[m.end():]
        return text[:off] + new_target + text[off + len(target):], True
    return text[:m.start()] + new_seg + text[m.end():], True


# 限定在 INSIGHTS 段内替换，避免命中 PICKS 里的同名键
i_ins = d.find('var INSIGHTS = {')
i_end = i_ins + re.search(r'\n\};', d[i_ins:]).end()
seg = d[i_ins:i_end]
seg2, ok = replace_section(seg, 'ai-track', ai)
d = d[:i_ins] + seg2 + d[i_end:]
print(('✅ ' if ok else '❌ ') + 'ai-track 已重写')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])
