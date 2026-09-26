# -*- coding: utf-8 -*-
"""更新第二步：词汇/课堂/待办/news/日期/版本"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-09-26'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

words = [
 {"emoji":"🖥️","category":"AI","word":"PTC（程序化工具调用）","definition":"Programmatic Tool Calling：模型不逐次往返调用工具，而是自主编写一整段代码去编排、批量调度多项工具，再统一筛选汇总。","example":"需要查 20 个页面的数据时，不是往返 20 次，而是一次生成脚本批量抓取再汇总。","why_matters":"多轮网络往返是 Agent 延迟的主要来源。PTC 把【逐次执行】换成【一次编排】，显著降低复杂流水线的延迟。"},
 {"emoji":"🔐","category":"产品","word":"隐私成本","definition":"用户为使用产品而付出的个人信息代价（如实名认证、手机号、通讯录授权），是一种隐性成本。","example":"同一功能，网页版注册即用 vs 桌面端需实名认证 —— 后者会劝退一部分用户。","why_matters":"它不进财务报表，但直接影响转化率。产品决策里必须把它和金钱成本一起权衡。"},
 {"emoji":"🧠","category":"AI","word":"决策模型 vs 生成模型","definition":"生成模型产出文本供人阅读；决策模型直接返回结构化判断（选项/分数/概率）供程序使用。","example":"Jev 就是决策模型：不生成文字，只返回【是否紧急/属于哪一类/概率多少】。","why_matters":"判断环节的接收者是代码，不需要漂亮解释。选错类型会让成本和延迟无谓增加。"},
 {"emoji":"💪","category":"健身","word":"超量恢复 (Supercompensation)","definition":"训练后身体不仅恢复到原有水平，还会略微超过原有水平，以适应下次同等刺激。","example":"深蹲后休息 48 小时，肌肉力量与糖原储备超过训练前。","why_matters":"肌肉是在休息期长出来的，不是在训练时。睡不够、休息不足，超量恢复就不会发生。"},
 {"emoji":"📉","category":"财经","word":"节前效应","definition":"长假前市场常出现的缩量、交投转淡现象，源于资金规避假期不确定性。","example":"国庆前最后两个交易日成交往往低于平时，波动也可能放大。","why_matters":"它解释了为什么节前常缩量——这是资金行为而非基本面变化，判断行情性质时要区分开。"},
 {"emoji":"📊","category":"运营","word":"激活率 (Activation Rate)","definition":"新用户完成【关键行为】的比例，该行为被验证与长期留存强相关。","example":"注册后 7 天内发布 1 条内容 → 视为激活，激活率 32%。","why_matters":"注册数只反映渠道量，激活率才反映产品是否让人真正用起来。这是增长分析的核心指标之一。"},
 {"emoji":"🎓","category":"求职","word":"技术判断力","definition":"在不懂实现细节的情况下，仍能判断方案边界、成本结构与失败模式的能力。","example":"能说清【桌面端复用 Web UI 意味着能力不会分叉】或【决策模型不生成文字是设计而非缺陷】。","why_matters":"AI 产品岗面试正在从【会用工具】转向【会做判断】，这正是被考核的核心。"},
 {"emoji":"💰","category":"理财","word":"应急金 (Emergency Fund)","definition":"专门用于应对失业、医疗等突发状况的资金，要求随时可取且不能承担本金风险。","example":"按月开销 5000 计，求职期建议准备 6 个月即 3 万元。","why_matters":"它的作用不是收益，而是让你在突发情况下不必被迫做坏决定（如接受不合适的 offer 或割肉卖出）。"},
 {"emoji":"🍂","category":"生活","word":"假期节律紊乱","definition":"长假期间作息、饮食、训练节奏被打乱，导致假期后恢复期延长。","example":"国庆七天完全不训练 + 熬夜，节后第一周力量水平明显下降。","why_matters":"增肌的连续性比单次强度重要。假期提前定好最低训练量，比节后补练更有效。"},
 {"emoji":"⚙️","category":"技术","word":"多端复用架构","definition":"不重写业务逻辑，而是让桌面/移动端复用同一套 Web UI 与运行逻辑的设计方式。","example":"DSH 桌面端用 Electron 直接复用 Web 端的 Agent、会话、工具与插件逻辑。","why_matters":"它意味着多端之间【能力不会分叉】。判断该用哪个端时，只需比较体验与成本，不必担心功能缺失。"}
]
m = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_VOCAB = {\n  date: "%s",\n  words: %s\n};' % (TODAY, j(words)) + d[m.end():]
    print('✅ 每日一词 → 10 词（9 个领域）')

learn = [
 {"section":"AI","emoji":"🖥️","title":"PTC 模式：为什么「写一段代码去调度工具」比「多轮往返」更快？","content":"传统 Agent 调工具是【往返式】：模型说调用工具 A → 等结果 → 再决定调用 B → 再等结果。每一次往返都包含网络延迟与模型推理时间，20 个页面就是 20 次往返。PTC 换了个思路：让模型先写出一整段代码，由这段代码在本地批量调用、筛选、汇总，最后只把结果交回模型。往返次数从 20 次压到 1 次。","takeaway":"复杂流水线的延迟瓶颈往往不在模型本身，而在往返次数。把编排交给代码，是当前 Agent 工程的明确方向。"},
 {"section":"技术","emoji":"⚙️","title":"Electron 复用 Web UI：多端产品的正确做法是什么？","content":"DSH 桌面端的官方说明很关键：目标不是重做一套 Harness，而是直接复用现有 Web UI 以及 Agent、会话、工具、插件的运行逻辑。这意味着桌面端是【入口扩展】而不是【能力分叉】——两条路的能力是同一套。","takeaway":"判断一个多端产品该不该换端时，先看它是复用还是分叉。复用的情况下，你只需要比较体验与成本，不必担心功能缺失。"},
 {"section":"产品","emoji":"🔐","title":"隐私成本：为什么「要实名」会劝退一部分用户？","content":"实名认证不进财务报表，但它是一种真实的成本——用户要交出身份证信息，承担被泄露的风险。在【功能相同】的前提下，需要实名的产品会流失一部分在意隐私的用户。做产品决策时，它必须和金钱成本一起被权衡，而不是当成无所谓的小事。","takeaway":"把隐私成本当成一个可量化的决策变量：它影响转化率，也影响用户对产品的信任定性。"},
 {"section":"AI","emoji":"🧠","title":"决策模型与生成模型的分工：什么时候不需要「说话」？","content":"判断一个环节该用哪种模型，先问两件事：这个环节的接收者是人还是程序？判断错了会怎样？接收者是程序时，它要的只是一个能用于下一步的值，一段漂亮的文字说明是纯浪费；收益低、代价小的判断，就可以交给更快更便宜的专门组件。","takeaway":"不是所有环节都需要最强模型。先分类，再分配——这是控制 AI 产品成本结构的第一步。"},
 {"section":"产品","emoji":"🧭","title":"新技术的采用时机：区分「理解价值」与「使用价值」","content":"新工具的价值分两层：理解价值（知道它是什么、解决什么问题、边界在哪）和使用价值（你当下真的处在它的适用场景里）。前者立刻能拿到——写进观察、变成面试素材；后者取决于你的实际需求。混淆两者会导致两种错误：盲目追新，或者因为【暂时用不上】而完全不去理解。","takeaway":"理解可以领先，采用必须滞后。对求职者来说，能讲清楚一个新方向的价值，往往比真的用它更值钱。"},
 {"section":"健身","emoji":"💪","title":"超量恢复：肌肉到底是在什么时候长出来的？","content":"训练只是给身体一个信号，真正的肌肉合成发生在训练后的休息期。身体不仅会修复，还会略微超过原有水平，以便适应下次同样强度的刺激——这就是超量恢复。睡眠不足、连续训练同一肌群、热量不够，都会让超量恢复无法发生。","takeaway":"训练、营养、睡眠是同一件事的三个部分。任缺一个，另外两个的效果都会打折。"},
 {"section":"财经","emoji":"📉","title":"节前效应：为什么长假前市场容易缩量？","content":"长假前资金会规避不确定性——假期里外盘可能大幅波动，而 A 股无法交易，等于被动承担了七天风险。部分资金因此选择减仓或观望，成交量随之下降。这是资金行为，不是基本面变化。","takeaway":"判断行情性质时要区分【资金行为】与【基本面变化】。缩量本身不代表变差，但会让突破的可信度下降。"},
 {"section":"运营","emoji":"📊","title":"激活率：为什么「注册数」不是一个好指标？","content":"注册数只反映渠道带来了多少人，不反映产品是否让人真正用起来。激活率的做法是：找出一个与长期留存强相关的关键行为（如 7 天内发布 1 条内容），再看新用户完成该行为的比例。它把【量】换成了【质】。","takeaway":"好的增长指标要能指导动作。注册数只能告诉你投放效果，激活率才能告诉你产品问题。"},
 {"section":"求职","emoji":"🎓","title":"技术判断力：AI 产品岗面试官真正想听的是什么？","content":"面试官问【这个功能该怎么做】时，往往不是要方案细节，而是看你能否判断边界：什么该用模型、什么该用规则代码、失败了怎么办、成本大概多少、验收标准怎么定。这些都不需要你会写代码，但需要你能把取舍讲清楚。","takeaway":"把每一个新技术都翻译成【它改变了什么取舍】，这就是技术判断力的训练方式。"},
 {"section":"生活","emoji":"🍂","title":"假期为什么容易打乱训练节奏？","content":"假期的问题不是没时间，而是【环境线索全部变了】：作息推迟、饮食不规律、训练场地方便性下降。习惯依赖环境线索触发，线索一变，行为就容易断。解决办法是给假期设一个【最低训练量】——比如每天 15 分钟自重训练，保持连续性。","takeaway":"假期保持连续性比保持强度更容易做到，也更重要——节后恢复成本会低很多。"}
]
lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_arch = re.sub(r',\s*$', '', am.group(1).strip())
        nb = ('\n  updated: "%s",\n  current_day: 21,           // 当前学到第几天\n  items: %s,\n'
              '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
              '  archive: {\n    "2026-09-23": [\n%s\n    ]%s\n  }\n') % (
            TODAY, j(learn), old_items, (',\n' + old_arch) if old_arch else '')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + nb + '};' + d[lm.end():]
        print('✅ 小白课堂 → 10 条，旧 10 条归档为 2026-09-23')

decisions = [
 {"icon":"🖥️","action":"把「DSH 桌面端 vs 网页版」对比 + Jev 接入决策整理成一份产品分析","why":"这本身就是完整的 AI 产品分析：多端形态取舍、成本与隐私权衡、能力边界判断、新技术采用时机——面试说服力远高于罗列工具清单","how":"结构：①两条事实（桌面端 9/25 预览版 / Jev 技术特点）②对比表 ③推荐与理由 ④什么条件下改变结论；写完归档作品集","priority":"P0"},
 {"icon":"💪","action":"增肌第 2 周收官复盘：对比训练容量与体重","why":"容量与体重是增肌期唯一两个可靠的进步信号；不复盘就无法判断第 3 周该加重还是该加餐","how":"拿出第 1 周记录对比：①各动作的 组×次×负重 是否上升 ②体重是否涨 0.25-0.5kg；容积涨而体重不涨 = 吃少了（每天加 200 kcal，只调主食）","priority":"P0"},
 {"icon":"⚖️","action":"早晨空腹称重，记录本周体重变化","why":"增肌期热量校准只能靠体重速度，感觉不可靠","how":"与上周对比：涨 0.25-0.5kg 保持；不涨加 200 kcal；涨超 0.75kg 减 200 kcal","priority":"P0"},
 {"icon":"📈","action":"周末复盘 + 国庆前仓位安排","why":"下周仅 9/28-9/29 两个交易日，节前效应会让量能进一步收缩，需要提前决定仓位","how":"①确认 3900 争夺的结果与 AI 硬件强度是否延续 ②决定是否降低节前仓位（长假期间外盘不可控）③把结论回填判断台账","priority":"P1"},
 {"icon":"🎓","action":"训练平台补进度：本周至少完成 2 天任务","why":"30 天计划的连续性比单日强度重要，断档容易整体放弃","how":"优先 SQL 训练场与数据集实验室；AI 产品经理新增的 p11（模型选型）与 p12（验收标准）两题可结合今天的 DSH/Jev 分析一起做","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_DECISIONS = {\n  updated: "%s",\n  items: %s\n};' % (TODAY, j(decisions)) + d[m.end():]
    print('✅ 今日待办 → 5 条（9/26 周六版）')

news = {
 "summary": "9月26日资讯速览：(1)<b>DSH 桌面端</b>——9/25 官方预览版上线（V0.1.7-rc.1，Electron 实现，复用同一套 Web UI 与 Agent/工具/插件逻辑），Windows+macOS，暂无 Linux；与网页版最大差异是需充值并实名认证，另新增四种 Agent 档位（标准/PTC/极简/创造）与可视化插件面板。(2)<b>AI 模型</b>——Jev（决策模型，不生成文字只输出判断+概率）持续被讨论，本月两次更新中已拆解其【零幻觉只保证结构】与【阈值波动】两个要点。(3)<b>A股</b>——沪指 3900 关口进入第三周争夺，结构市特征延续，下周仅 9/28-9/29 两个交易日。(4)<b>求职</b>——AI 产品岗考核重心继续从工具熟练度转向判断力与边界定义能力。",
 "trend": "本周资讯三条主线：①<b>多端复用成为主流工程选择</b>——DSH 桌面端选择 Electron 复用 Web UI 而非重做，说明产品形态稳定的前提下，多端是入口扩展而非能力分叉；②<b>Agent 工程从【往返式】走向【程序化编排】</b>——PTC 模式用一段代码批量调度工具，把往返次数从 N 次压到 1 次；③<b>A股维持结构市</b>——指数与个股分化，判断行情性质的关键仍是量能。",
 "tip": "今日跟踪：①把 DSH 桌面端对比整理进作品集（这是现成的 AI 产品分析）②确认 Jev 的接入时机条件（有后端系统 + 有大量判断环节时）③国庆前完成节前仓位决定并回填判断台账。",
 "updated": TODAY
}
mn = re.search(r'\n  news: \{[\s\S]*?\n  \},', d)
if mn:
    d = d[:mn.start()] + '\n  news: ' + j(news) + ',' + d[mn.end():]
    print('✅ news 分区已更新')

# 日期同步
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-09-2[0-9])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
d, n2 = re.subn(r'("update_date":\s*")([^"]+)(")', lambda m: m.group(1) + CN + m.group(3), d)
d, n3 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 日期同步：updated %d · update_date %d · update_time %d' % (n1, n2, n3))

fixes = [('9月23日（周三）', '9月26日（周六）'), ('9月23日', '9月26日'),
         ('2026年9月23日', CN), ('追番第42天', '追番第45天'),
         ('倒计时7天', '倒计时4天'), ('倒计时 7 天', '倒计时 4 天'),
         ('本周（9/22-9/26）', '本周（9/22-9/26）'), ('9/22-9/26', '9/22-9/26')]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 文本日期/天数：%d 处' % c)

d = d.replace('var SITE_VERSION = "1.8.17";', 'var SITE_VERSION = "1.8.18";')
d = re.sub(r'版本1\.8\.1[0-9]', '版本1.8.18', d)
print('✅ 版本 → 1.8.18')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])

IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.18', h)
open(IP, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.18')
