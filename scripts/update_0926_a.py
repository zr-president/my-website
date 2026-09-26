# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-09-26（周六）
   ai-track 重写：DSH 桌面端 vs 网页版对比 + Jev 接入决策
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
assert TODAY == '2026-09-26', '日期不符：' + TODAY
print('目标日期：%s（%s）' % (TODAY, WD))


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 1) ai-track 重写 ====================
aitrack = {
 "verdict": "🎯 今日两条结论：① <b>DSH 桌面端</b>（9/25 官方预览版）——<b>建议继续用网页版</b>，桌面版的优势集中在插件开发与重度 Agent 流水线，且需要实名认证+充值；② <b>Jev</b>——<b>现在不接入</b>，列入待观察。你目前没有需要大量判断环节的后端系统，而求职期最该投入的是【产出可展示的作品】，不是接入新工具。两条都是【理解的价值 &gt; 使用的价值】。",
 "summary": "<b>一、DSH 桌面端（官方预览版）</b>：9 月 25 日晚，开发者在 DeepSeek Harness 官方仓库发现桌面端源码（<code>apps/desktop</code>），下载源为 download.deepseek.com，版本 <b>V0.1.7-rc.1</b>（内置更新可至 rc.2）。技术上是 <b>Electron</b> 实现——官方明确说明目标不是重做一套 Harness，而是<b>直接复用现有 Web UI 以及 Agent、会话、工具、插件等运行逻辑</b>。平台为 Windows x64 与 macOS arm64（Mac 版已过 Apple 公证，签名主体为杭州深度求索），<b>暂无 Linux</b>。<br><br><b>二、Jev 决策模型</b>：TypeSafe 9/15 发布的首个 System One Model。给它上下文 + 预声明答案类型的问题，直接返回选择/评分/概率，不生成文字。实测准确率 64-65%（不占优），但速度成本明显领先（0.73 秒/题、50 题 0.002 美元）。",
 "trend": "<b>DSH 桌面端 vs 网页版 · 逐项对比</b><br><br><table class=\"data-table\"><tr><th>维度</th><th>网页版（你现在用的）</th><th>桌面端（9/25 预览版）</th></tr>"
          "<tr><td><b>获取成本</b></td><td style=\"color:var(--green)\">注册即用，免费</td><td style=\"color:var(--red)\">无额度需充值 + <b>需实名认证</b></td></tr>"
          "<tr><td><b>安装</b></td><td style=\"color:var(--green)\">零安装，浏览器打开</td><td>需下载安装包（Win/Mac）</td></tr>"
          "<tr><td><b>平台</b></td><td style=\"color:var(--green)\">Win/Mac/Linux/平板手机通用</td><td>仅 Windows / macOS，<b>无 Linux</b></td></tr>"
          "<tr><td><b>升级</b></td><td style=\"color:var(--green)\">刷新即最新</td><td>内置更新，但需重启应用</td></tr>"
          "<tr><td><b>本地文件操作</b></td><td style=\"color:var(--green)\">完全可用（工作区就是本机目录）</td><td>同样可用</td></tr>"
          "<tr><td><b>API 接入</b></td><td>—</td><td style=\"color:var(--green)\">支持直接用官方 API Key</td></tr>"
          "<tr><td><b>UI 体验</b></td><td>标准 Web 界面</td><td style=\"color:var(--green)\">无边框轻拟态 · 任务式回答区（显示 Token 数/工具调用次数/耗时）· 结果卡片可交互</td></tr>"
          "<tr><td><b>工作模式</b></td><td>单一模式</td><td style=\"color:var(--green)\">办公创作 / 代码开发 两类 + 展示偏好三档（聚焦结果/关键细节/完整过程）</td></tr>"
          "<tr><td><b>Agent 档位</b></td><td>—</td><td style=\"color:var(--green)\">四种：标准 / <b>PTC</b> / 极简 / 创造</td></tr>"
          "<tr><td><b>插件管理</b></td><td>命令行</td><td style=\"color:var(--green)\">可视化面板（搜索提供方/Subagent 团队/执行管控/代码仓调用）</td></tr>"
          "<tr><td><b>稳定性</b></td><td style=\"color:var(--green)\">已稳定运行</td><td>rc 预览版，可能有 bug</td></tr></table>"
          "<br><b>四种 Agent 档位里最值得注意的是 PTC</b>（Programmatic Tool Calling）：模型不再通过多轮网络往返逐次执行命令，而是<b>自主编写一整段代码去编排、批量调度多项工具</b>，再统一筛选汇总——这能显著降低延迟、提升复杂流水线的稳定性。另外【创造模式】允许用自然语言直接调试 Cordis 插件、动态扩展界面。"
          "<br><br><b>Jev 的核心判断</b>：它不是【更强的模型】，而是把服务对象从人换成程序。两个必须看穿的宣传点：①「零幻觉」只保证输出结构（不跑出 schema），不代表判断正确；② 概率输出在阈值附近仍会波动（实测人工下限 2.00、模型给 1.99，15 次重复有 3 题通过失分交替）。",
 "tip": "<b>我的推荐：继续用网页版</b>。四条理由：<br>① <b>实名认证的隐私成本</b>——你只是用它改自己的网站、写脚本、做内容，为这个场景交出实名信息不划算；<br>② <b>充值成本</b>——你正在求职期，现金流要留给生活与应急，不该增加订阅支出；<br>③ <b>能力覆盖</b>——网页版已经能完全访问本机工作区（现在操作的这些脚本与文件就是证据），桌面端多出来的能力你暂时用不到；<br>④ <b>rc 预览版</b>——稳定性未知，不适合作为依赖。<br><br>"
          "<b>什么时候再考虑换桌面端</b>：① 你开始<b>开发 DSH 插件</b>（创造模式 + 可视化插件面板）② 你要跑<b>复杂多工具流水线</b>（PTC 降延迟收益明显）③ 你找到工作、有稳定收入后长期高频使用。建议先等 1-2 个正式版。<br><br>"
          "<b>Jev 的接入结论：现在不接入</b>。理由：① 你目前没有<b>带后端的、需要大量判断环节</b>的系统（训练平台是纯前端）② Jev 是决策模型不是聊天助手，你的日常场景（改网站、写内容）用不上 ③ 接入需要 API Key + 付费 + 开发工作。<br>"
          "<b>什么时候该接入</b>：① 你做<b>带后端的产品</b>（例如给训练平台加自动判卷，用 Jev 判定答案对错而非让 LLM 生成解析）② 你要做<b>批量任务</b>（如批量分析成千上万条用户反馈的分类）③ 单次判断成本降到千分之几美分后，原本只能抽样的功能可以全量化。",
 "reasoning": "为什么这两件事都值得关注但都不必马上用：<br><b>DSH 桌面端的信号意义在于架构选择</b>——官方选择 Electron 并明确【复用现有 Web UI 与运行逻辑】，而不是重做一套。这说明 DSH 的产品形态已经稳定到可以多端复用，桌面端是【入口扩展】而不是【能力分叉】。对使用者而言，这意味着<b>两条路的 Agent 能力是同一套</b>，不会因为留在网页版而少能力。<br>"
             "<b>Jev 的信号意义在于架构分工</b>——它把【写作/推理交给通用大模型，边界清晰的小判断交给专门组件】这个分工具体化了。团队 CEO Diogo Almeida 是 OpenAI InstructGPT 论文作者之一，他质疑自己参与推动的路线，这个转向本身就有信息量。但<b>理解一个方向不等于现在就要采用它</b>——尤其当你还不是在搭系统的时候。<br>"
             "<b>共同的判断原则</b>：新工具的价值分两层——【理解价值】与【使用价值】。前者现在就能拿到（写进观察、变成面试素材），后者取决于你是否真的处在它的适用场景里。你现在的场景是<b>求职期 + 内容产出</b>，所以这两件事的最优解都是：把理解变成作品，把使用推迟到有真实需求时。",
 "updated": TODAY
}
mt = re.search(r'\n  "ai-track": \{[\s\S]*?\n  \},', d) or re.search(r'\n  ai-track: \{[\s\S]*?\n  \},', d)
if mt:
    d = d[:mt.start()] + '\n  "ai-track": ' + j(aitrack) + ',' + d[mt.end():]
    print('✅ ai-track 已重写（DSH 桌面端对比 + Jev 接入决策）')
else:
    print('❌ MISS ai-track')

# ==================== 2) 今日要闻 ====================
highlights = [
 {"priority":1,"icon":"🖥️","section":"DSH 桌面端","headline":"DSH 桌面端预览版 9/25 上线：Electron 实现、复用同一套 Web UI，但需实名认证+充值","summary":"9/25 晚官方仓库被发现 apps/desktop 目录，下载源 download.deepseek.com，版本 V0.1.7-rc.1（可更新至 rc.2）。技术上是 Electron，官方明确【复用现有 Web UI 与 Agent/会话/工具/插件运行逻辑】——所以桌面端是入口扩展，不是能力分叉。平台为 Windows x64 + macOS arm64（Mac 版已过 Apple 公证），暂无 Linux。与网页版最大差异：桌面端需充值（或绑有余额账户）并需实名认证；新增四种 Agent 档位（标准/PTC/极简/创造）与可视化插件面板。我的推荐：继续用网页版，理由与切换时机见 AI 动态追踪。","action":"看完整对比","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":2,"icon":"🧠","section":"Jev 接入决策","headline":"Jev 是否要接入？结论：现在不接入——你还没有需要大量判断环节的后端系统","summary":"Jev 是决策模型（不生成文字，直接返回选择/评分/概率），它的价值场景是【有大量边界清晰的小判断要交给程序】。你目前的训练平台是纯前端、日常场景是改网站与写内容，都用不上。接入还需 API Key + 付费 + 开发工作。同时存在两个必须看穿的宣传点：零幻觉只保证输出结构不保证判断正确；概率输出在阈值附近仍会波动（1.99 vs 2.00）。什么时候该接入、怎么用，详见 AI 动态追踪。","action":"看接入建议","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":3,"icon":"⚙️","section":"技术看点","headline":"PTC 模式是什么？为什么它能降低复杂流水线的延迟","summary":"PTC（Programmatic Tool Calling）让模型不再通过多轮网络往返逐次执行命令，而是【自主编写一整段代码程序】去编排、批量调度多项工具，最后统一筛选汇总。对多工具流水线来说，这能显著减少往返次数、降低延迟并提升稳定性。这是这次桌面端更新里最值得理解的一项工程思路——它和【Agent 该怎么设计】直接相关。","action":"看对比","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":4,"icon":"📈","section":"A股周复盘","headline":"本周（9/22-9/26）3900 关口第三周争夺：结构市特征延续，量能仍是关键变量","summary":"沪指继续在 3900 附近震荡争夺，成交维持存量博弈区间。AI 硬件（覆铜板/光模块/元件）的相对强度仍在延续，9/11 提出的【结构主线】判断持续成立。当前框架不变：量能未放大前维持结构市判断；不追高，等收回关键位 + 放量。国庆假期前仅剩 2 个交易日（9/28-9/29），注意节前效应与仓位管理。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":5,"icon":"💪","section":"健身进展","headline":"增肌计划第 2 周收官：下周进入第 3 周，检查容量是否持续上升","summary":"第 2 周按【每周只推一项】推进（先把同样负重从 8 次练到 12 次，再加重让次数回落）。第 2 周收官该做两件事：① 对比第 1 周记录，确认训练容量（组×次×负重）是否上升 ② 体重是否按 0.25-0.5kg/周 的速度增长。不涨就是吃少了——每天加 200 kcal（只调主食，蛋白不动）。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":6,"icon":"🎓","section":"求职准备","headline":"金九银十进入尾声：把「DSH 桌面端 vs 网页版」的对比写成产品分析，是现成的作品","summary":"今天这份 DSH 桌面端与网页版的逐项对比、以及 Jev 的接入决策，本身就是一份完整的【AI 产品分析】：涉及多端形态取舍、成本与隐私权衡、能力边界判断、以及新技术的采用时机。这类分析在 AI 产品岗面试里的说服力，远高于罗列工具清单。建议整理进作品集。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":7,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 最终话倒计时 4 天（9/30）：本周末是补番的最后窗口","summary":"距离 9/30 最终话仅剩 4 天，本周末是补完夺还篇的最后完整窗口。国庆假期正好接上最终话，节奏刚好。动漫区的官方海报与观看顺序已更新。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":8,"icon":"🍂","section":"假期与生活","headline":"国庆假期临近：9/28-9/29 是节前最后两个交易日，出行与办事需提前安排","summary":"国庆假期临近，两件事需要提前：① A股 9/28-9/29 为节前最后交易日，节后 10/8 开市，注意持仓与节前效应 ② 出行/办事类事项按假期日历提前安排（生活助手区的办事日历已同步）。另外假期是增肌训练容易中断的时期——提前定好训练安排，避免整周停练。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"}
]
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
