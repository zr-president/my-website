# -*- coding: utf-8 -*-
"""修正 9/13 内容过于单一的问题：
   - 今日要闻：健身/饮食相关从 4 张压到 1 张，其余换成 AI/股市/求职/动漫/生活
   - 每日一词：从「10 条全健身」改为 健身3 + AI3 + 运营2 + 财经1 + 饮食1
   - 小白课堂：从「10 条全健身」改为 健身3 + AI3 + 运营2 + 财经1 + 求职1
"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


# ==================== 1) 今日要闻：降低健身占比 ====================
highlights = [
 {"priority":1,"icon":"💪","section":"健身方案调整","headline":"健身区大改：从「减脂露腹肌」转向「增肌 + 腹肌 双目标」（新增练腿·跳绳减量·热量转盈余）","summary":"你提出既要腹肌又要增肌——对 170cm/59kg、体脂 15-18% 的【瘦胖子】来说这其实是同一件事：体脂率偏高不是因为脂肪多，而是肌肉太少。继续减脂会掉到 55kg 更瘦弱，腹肌照样不明显。新方案三处改动：①新增下肢训练（原来完全没有）②跳绳 3-4 次减到 1-2 次 ③热量从轻缺口改为轻微盈余。12 周目标：62-63kg、体脂 13-14%、腹肌清晰。饮食页已同步调整（训练日 2500 / 休息日 2300 kcal）。","action":"查看新计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":2,"icon":"🐳","section":"DeepSeek V4.1 Flash","headline":"V4.1 Flash 开源权重放出后：社区垂直微调版本开始出现，私有化部署门槛明显下降","summary":"9/10 发布的 V4.1 Flash（5520 亿参数 MoE、原生视觉、KV 缓存 token 降至 V4-Flash 的 1/3.9）已放出开源权重，社区基于它做的垂直微调版本开始出现。对应用侧的实际意义：此前必须用闭源旗舰处理敏感数据的场景（如含客户联系方式的跟进记录摘要），现在可以走本地开源模型，成本能低一个数量级——这是【AI 落地成本】层面的结构性变化，不只是榜单分数。","action":"深度解读","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":3,"icon":"📉","section":"A股复盘","headline":"沪指 3888 点失守 3900 后观察企稳信号：成交 1.97 万亿，AI 硬件仍是结构主线","summary":"昨日沪指收 3888.11（643 家涨 / 4870 家跌），成交 1.97 万亿元。结构上仍是【AI 硬件】主线：覆铜板、光模块等环节受关注。当前判断维持不变——赚钱效应低、不适合追高；等企稳信号（收回关键位 + 放量）再谈加仓。今日需验证的判断：若继续跌破 3850 支撑，则本轮调整周期延长。","action":"看待验证判断","link":"#stock","deepLink":"#stock"},
 {"priority":4,"icon":"🤖","section":"AI 工程趋势","headline":"从「会写 Prompt」到「会设计 Workflow」：Agentic 工作流成为 AI 产品岗的新分水岭","summary":"行业讨论重心正从单次问答转向多步任务编排：一个 Agent 产品要拆解目标、调用工具、校验结果、失败重试。对求职的影响很直接——面试里【你怎么设计一个能完成任务的 Agent】正在取代【你怎么写 Prompt】。相关能力已加入能力训练平台的 AI Agent 实操模块。","action":"看 Agent 实操","link":"#ai-track","deepLink":"https://zr-president.github.io/training/#/agent"},
 {"priority":5,"icon":"🎓","section":"求职准备","headline":"能力训练平台新增「30 天训练计划」：从 0 开始、每天 40-60 分钟、完成打勾","summary":"面向策略运营/用户增长与 AI 产品经理两个方向，30 天 91 个任务、4 个阶段（打地基→核心数据能力→业务分析能力→产品与实战）。每天 2-4 个任务并直达对应模块，点【开始计划】后自动记录今天是第几天。平台同时新增 Python 数据分析案例（22 个可复制案例）与 AI 产品经理面试题库（18 题）。训练进度通过同源 localStorage 回流到本站侧边栏入口。","action":"去训练","link":"#fitness","deepLink":"https://zr-president.github.io/training/"},
 {"priority":6,"icon":"🛡️","section":"AI 治理","headline":"AI 内容标识与安全评估要求继续落地，To B 场景的合规成本开始显性化","summary":"生成式 AI 服务的内容标识、安全评估要求在持续落地。对做 AI 产品的人来说，这从【法务的事】变成了【产品需求】：AI 生成内容需要可标识、可溯源，转人工路径与日志留存要写进 PRD。这也是 AI PM 面试的高频考点——面试官常问【你的 AI 功能怎么满足合规要求】。","action":"看 AI 产品要点","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":7,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 第三季完结倒计时 17 天：本周更新第 10 话，剧情进入高潮段","summary":"Re:Zero 第三季进入收尾阶段，剩余约 3 话。本周第 10 话推进主线冲突，评价明显回升。想看完整番剧清单与官方海报可进动漫区（已按本季推荐更新海报与观看顺序）。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":8,"icon":"🍹","section":"生活灵感","headline":"秋燥时节的两件小事：补水节奏与居家湿度，比买什么补品都实在","summary":"9 月广州转晴回温但空气开始变干，白天出汗 + 空调房干燥容易双重脱水——这对你有结石预防需求尤其关键（饮水 ≥2.5L 并分散饮用）。生活助手区已更新秋季办事与健康提醒；睡眠保持 7-8 小时，也是增肌期肌肉修复的硬条件。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"}
]

# ==================== 2) 每日一词：全领域分布 ====================
words = [
 # —— 健身/营养 3 条（今日主题，保留但不占满）——
 {"emoji":"🧍","category":"健身","word":"瘦胖子 (Skinny Fat)","definition":"体重正常甚至偏轻，但体脂率偏高、肌肉量不足的体型。表面看是【微胖】，本质是【肌肉太少】。","example":"170cm/59kg、体脂 15-18% 就是典型瘦胖子——BMI 只有 20.4，但肚子有赘肉。","why_matters":"这决定了策略方向：瘦胖子该增肌而不是减脂。按减脂做只会更瘦弱，肚子依然松。"},
 {"emoji":"📈","category":"健身","word":"渐进超负荷 (Progressive Overload)","definition":"逐步增加训练难度（重量、次数、组数或动作难度），让身体持续被迫适应。","example":"俯卧撑从自重 60 个 → 背包负重 4×8-12 至力竭；同样负重从 8 次练到 12 次再加重量。","why_matters":"这是增肌唯一必需的变量。不加重 = 只练耐力不长肌肉，是居家训练最常见的停滞原因。"},
 {"emoji":"⚖️","category":"健身","word":"干扰效应 (Interference Effect)","definition":"大量有氧训练会消耗本该用于肌肉合成与恢复的能量，削弱增肌效果。","example":"每周 3-4 次跳绳 HIIT + 热量缺口，结果体重掉了但肌肉几乎没长。","why_matters":"这是把跳绳从 3-4 次减到 1-2 次的直接原因。有氧不是不能做，是不能过量。"},
 # —— AI 3 条 ——
 {"emoji":"🧩","category":"AI","word":"上下文工程 (Context Engineering)","definition":"系统性设计喂给模型的全部上下文（系统提示、检索片段、历史对话、工具返回、格式约束），而不只是雕琢一句 Prompt。","example":"同一句提问，附上 3 条检索到的制度原文 + 输出格式约束，回答质量与裸问完全不同。","why_matters":"模型能力趋同后，产品差异越来越取决于【喂什么上下文】。这也是 RAG 类产品真正的护城河所在。"},
 {"emoji":"🔗","category":"AI","word":"Agentic Workflow","definition":"把任务拆成多步，由模型自主决定调用哪些工具、按什么顺序执行、失败如何重试的工作流形态。","example":"写周报 Agent：取数 → 校验 → 生成解读 → 自检是否编造数字 → 落库待审。","why_matters":"这是 AI 从【回答问题】走向【完成任务】的关键。面试里【怎么设计一个能完成任务的 Agent】正在取代【怎么写出好 Prompt】。"},
 {"emoji":"🧪","category":"AI","word":"知识蒸馏 (Knowledge Distillation)","definition":"让小模型学习大模型的输出分布（而不只是原始标签），从而用更小体量逼近大模型表现。","example":"用旗舰模型的回答作为训练数据，蒸馏出可在本地 GPU 跑的小模型，成本降一个数量级。","why_matters":"这是开源模型能追上闭源的重要路径之一，也是私有化部署方案可行性的来源。"},
 # —— 运营/增长 2 条 ——
 {"emoji":"⭐","category":"运营","word":"北极星指标 (North Star Metric)","definition":"唯一能代表产品为用户创造核心价值的指标，全团队围绕它对齐。","example":"内容社区用【周活跃创作者数】而不是【总注册用户数】。","why_matters":"选错的典型后果是把虚荣指标当目标。判断标准：可行动、可比、能预警，且与长期价值正相关。"},
 {"emoji":"💰","category":"运营","word":"LTV / CAC","definition":"用户生命周期价值与获客成本之比，衡量增长是否健康。","example":"某渠道 LTV 90 元、CAC 30 元 → 比值 3，属于可放量区间。","why_matters":"小于 1 是亏钱买量，1-3 打平，大于 3 才适合放量。这是投放决策的第一道门槛。"},
 # —— 财经 1 条 ——
 {"emoji":"📊","category":"财经","word":"量价背离","definition":"价格与成交量走势不一致，通常被视为趋势动能减弱的信号。","example":"指数连涨但成交持续萎缩（缩量上涨），追高容易接在情绪高点。","why_matters":"单看价格会误判。放量下跌说明抛压真实，缩量上涨说明承接不足——两者含义完全不同。"},
 # —— 饮食 1 条 ——
 {"emoji":"🍚","category":"饮食","word":"升糖指数 (GI)","definition":"食物引起血糖上升速度的相对指标，数值越高升糖越快。","example":"白米饭 GI 约 83，糙米约 55，燕麦约 55。","why_matters":"增肌期不必惧怕碳水，但把部分精制主食换成低 GI 主食，血糖更稳、饱腹更久，也不易囤脂。"}
]

# ==================== 3) 小白课堂：全领域分布 ====================
learn_items = [
 # —— 健身 3 条 ——
 {"section":"健身","emoji":"🧍","title":"瘦胖子是什么？为什么体脂率会被【肌肉少】推高？","content":"同样 59kg，肌肉多的人体脂率可以只有 10%，肌肉少的人却会到 16%——因为体脂率 = 脂肪 ÷ 体重，而肌肉也是体重的一部分。瘦胖子的体重正常，但瘦体重偏低，于是脂肪占比被动升高。所以问题不是【脂肪太多要减】，而是【肌肉太少要加】。","takeaway":"体脂率是个比值。可以通过降分子（减脂）改善，也可以通过升分母（增肌）改善——瘦胖子应该选后者。"},
 {"section":"健身","emoji":"📈","title":"渐进超负荷：增肌唯一必需的变量","content":"肌肉增长的信号是【机械张力】——肌肉必须在超出以往的水平下发力。如果重量、次数、节奏长期不变，身体就没有理由继续长肌肉，只会提高神经效率与耐力。所以同样一组动作，必须持续加重量、加次数或加难度。","takeaway":"判断训练有没有效，先问一句：这周的负重或次数比上周多了吗？没有就是在原地踏步。"},
 {"section":"健身","emoji":"⚖️","title":"干扰效应：为什么有氧做多了影响增肌？","content":"有氧与力量训练争夺同一批恢复资源（糖原、氨基酸、恢复时间），并且有氧会激活 AMPK 通路、抑制肌肉合成的 mTOR 通路。每周 1-2 次中等强度有氧影响不大，但 4 次以上高强度有氧 + 热量缺口，增肌基本停滞。","takeaway":"增肌期有氧要【够用就好】：控心肺与体脂靠 1-2 次，不要当主力练。"},
 # —— AI 3 条 ——
 {"section":"AI","emoji":"🧩","title":"上下文工程是什么？为什么【会写 Prompt】已经不够了？","content":"模型能力逐渐趋同后，决定输出质量的不再是那句提问，而是你喂进去的全部信息：系统提示、检索到的原文、历史对话、工具返回结果、输出格式约束。这就是上下文工程——把【模型需要知道的一切】结构化地组织好，而不是指望一句话点石成金。类比：同一个聪明的员工，给他完整背景资料 vs 只丢一句话，产出完全不同。","takeaway":"做 AI 产品时，先问【上下文够不够、准不准、有没有冲突】，再考虑换不换模型——后者往往不是瓶颈。"},
 {"section":"AI","emoji":"🔗","title":"Agentic Workflow：AI 从【回答问题】到【完成任务】差在哪？","content":"单次问答只需要模型【生成一段话】；完成一个任务则需要拆解目标、调用外部工具、校验结果、失败重试、必要时转人工。Agentic Workflow 的本质是把不可靠的单次生成，变成多步可验证的流程——每一步都能检查、都能兜底。","takeaway":"任务型 AI 产品的设计重点不是【一次答得多好】，而是【每一步错了怎么办】。"},
 {"section":"AI","emoji":"🧪","title":"知识蒸馏：小模型凭什么能学会大模型的能力？","content":"传统训练只告诉模型【正确答案是什么】，蒸馏则让模型学习大模型输出的完整概率分布——相当于老师不只给答案，还解释了【为什么其他选项不对】。信息量更大，小模型因此能用少得多的参数逼近大模型表现。","takeaway":"这也是开源模型能快速追上闭源、并让私有化部署成本变低的关键路径之一。"},
 # —— 运营/增长 2 条 ——
 {"section":"运营","emoji":"⭐","title":"北极星指标怎么选？为什么不能用 GMV 当北极星？","content":"北极星指标要能代表【产品为用户创造的核心价值】，而不是财务结果。GMV 是结果不是原因——团队无法通过【直接提升 GMV】来行动，只能通过改善体验、提升复购等因。用结果指标当北极星，会导致团队只盯短期促销。","takeaway":"好指标的三个标准：可行动（能指导具体动作）、可比（能跨时间/团队对比）、能预警（变化早于结果指标）。"},
 {"section":"运营","emoji":"💰","title":"LTV/CAC 小于 1 意味着什么？怎么算才对？","content":"LTV 是单个用户整个生命周期贡献的毛利，CAC 是获取一个用户的成本。比值小于 1 说明花 1 块钱只赚回不到 1 块，规模越大亏得越多。常见错误有两个：用收入代替毛利算 LTV（高估）、只算广告费不算人力与补贴（低估 CAC）。","takeaway":"用毛利算 LTV、用全成本算 CAC，比值大于 3 才考虑放量——这是投放决策的第一道门槛。"},
 # —— 财经 1 条 ——
 {"section":"财经","emoji":"📊","title":"量价背离：为什么【缩量上涨】要警惕？","content":"成交量代表参与意愿的强度。放量下跌说明抛压是真实的、有大量筹码在出逃；缩量上涨说明推动力有限、承接盘不足，更多是存量资金在博弈。两者含义完全不同，只看价格会误判。","takeaway":"看趋势要【价 + 量】一起看：价格告诉你方向，成交量告诉你这个方向有多可信。"},
 # —— 求职 1 条 ——
 {"section":"求职","emoji":"🧭","title":"AI 产品经理面试：为什么【能用代码解决的事别用模型】是第一条判断？","content":"面试官问【什么需求适合用大模型】时，最想听的不是【什么都能做】，而是你知道边界：金额结算、风控裁决、实名审核这类需要 100% 确定性或涉及合规责任的场景，必须用规则代码或人工，因为模型输出本质上是概率性的。","takeaway":"判断口诀：语言类任务 × 容错空间可接受 × 有兜底或可抽检 × 效果可度量 —— 四条都满足才适合上模型。"}
]

# ==================== 写回 ====================
def replace_block(text, var, new_obj, extra_keys=None):
    m = re.search(r'var ' + var + r' = \{[\s\S]*?\n\};', text)
    if not m:
        print('MISS', var); return text
    if var == 'DAILY_BRIEFING':
        new = 'var DAILY_BRIEFING = {\n  date: "2026-09-13",\n  highlights: ' + j(new_obj) + '\n};'
    elif var == 'DAILY_VOCAB':
        new = 'var DAILY_VOCAB = {\n  date: "2026-09-13",\n  words: ' + j(new_obj) + '\n};'
    else:
        new = None
    if new is None:
        print('SKIP', var); return text
    print('OK', var, '→', len(new_obj), '条')
    return text[:m.start()] + new + text[m.end():]


d = replace_block(d, 'DAILY_BRIEFING', highlights)
d = replace_block(d, 'DAILY_VOCAB', words)

# LEARN_PATHS：只换 items，保留 archive 与 updated
lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[[\s\S]*?\n  \],', body)
    am = re.search(r'archive:\s*\{[\s\S]*\}\s*$', body)
    if im and am:
        new_body = '\n  updated: "2026-09-13",\n  current_day: 8,           // 当前学到第几天\n  items: ' + j(learn_items) + ',\n  ' + am.group(0).strip() + '\n'
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + new_body + '};' + d[lm.end():]
        print('OK LEARN_PATHS →', len(learn_items), '条（archive 保留）')
    else:
        print('MISS items/archive')
else:
    print('MISS LEARN_PATHS')

open(FP, 'w', encoding='utf-8').write(d)
print('done')

# 统计分布
def dist(arr, key):
    from collections import Counter
    return dict(Counter(x.get(key, '?') for x in arr))
print()
print('要闻分区分布:', dist(highlights, 'section'))
print('每日一词分区:', dist(words, 'category'))
print('小白课堂分区:', dist(learn_items, 'section'))
