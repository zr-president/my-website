# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-09-23（周三）
   核心新增：Jev（TypeSafe 9/15 发布的首个 System One Model）深度内容
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-09-23', '日期不符：' + TODAY
print('目标日期：%s（%s）' % (TODAY, WD))


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 1) 今日要闻 ====================
highlights = [
 {"priority":1,"icon":"🧠","section":"Jev 决策模型","headline":"TypeSafe 发布 Jev（9/15）：首个「System One Model」——不生成文字，只输出判断与概率","summary":"Jev 的用法和所有大模型都不同：给它一段 state（上下文）和一组预先声明答案类型的 questions，它直接返回【选择 / 评分 / 真假判断 + 概率】，不生成任何文字。TypeSafe 把它定义为第一个 System One Model（取自卡尼曼《思考，快与慢》的直觉式快思考），训练方法为 RLCD（面向校准决策的强化学习）。上线 Vercel AI Gateway 24 小时内，近 13% 的付费团队用过它——平台历史上采用最快的模型发布。它不是【更聪明的模型】，而是把模型的服务对象从人换成了程序。","action":"深度解读","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":2,"icon":"⚖️","section":"Jev 实测","headline":"实测数据：Jev 准确率并不突出（64-65%），但速度与成本是压倒性的——0.73 秒/题、50 题 0.002 美元","summary":"第三方实测（50 条中文客服题，四项判断全对才算正确）：Jev 完整准确率约 64-65%，在便宜小模型组排第二，比 DeepSeek V4 Flash 少 1.2 分；但在更强模型组里排在最后（MiniMax M3 准确率高约 10.8 个百分点）。真正的差异在速度与成本：Jev 平均 0.73 秒/题、50 题总成本约 0.002 美元，两项都是最低；DeepSeek V4 Flash 每题要 5.58 秒、成本约 2.5 倍。结论：Jev 不是【更强】，而是一组明确的取舍——少等、少花钱，接受一定准确率差距。","action":"看对比","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":3,"icon":"⚠️","section":"技术理解","headline":"两个必须看穿的宣传点：「零幻觉」不等于不会判断错；概率输出在阈值附近仍会波动","summary":"第一，TypeSafe 说的【零幻觉】指的是输出结构保证——不会生成 schema 之外的类型、不会把该是数字的结果写成一段话；但它在 A/B/C 里仍然可能选错，只是不会跑出 D。第二，实测出现阈值陷阱：人工标注严重度下限 2.00，Jev 给 1.99——若业务规则写【达到 2.00 才转人工】，1.99 和 2.00 会被程序当成完全不同的信号；重复测试 15 次有 3 题出现通过/失分交替。这说明【返回精确小数】并不会自动让业务规则变可靠。这两点正是 AI 产品岗该有的技术理解深度。","action":"看产品要点","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":4,"icon":"🎓","section":"求职准备","headline":"Jev 是你 AI 产品岗面试的绝佳素材：它考的是「什么该用 LLM、什么不该」这个判断力","summary":"Jev 背后是一个清晰的架构主张：写作、代码生成、复杂推理继续交给擅长这些的模型；而 Agent 执行过程中的大量【边界清晰的小判断】——这次请求能否交给便宜模型、检索结果是否相关、该调用哪个工具、任务该继续还是重试、另一个模型的答案是否可信——交给专门优化的判断组件。这些环节的接收者是程序，用不上一段漂亮的说明。把这件事讲清楚，比背 Prompt 技巧更能证明你的产品判断力。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":5,"icon":"📈","section":"A股周中","headline":"3900 关口进入第二周争夺：结构性行情特征未变，量能仍是判断行情性质的关键","summary":"沪指继续在 3900 附近反复争夺，成交维持在存量博弈区间。结构上【AI 硬件】的相对强度仍在延续，验证了 9/11 以来的判断。当前操作框架不变：量能未放大前维持结构市而非全面行情；不追高，等收回关键位 + 放量。9/21 起的预案继续有效：关注 3900 站稳与否，下方看 3850 支撑。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":6,"icon":"💪","section":"健身进展","headline":"增肌计划进入第 2 周：从建立基线转入正式增肌期，开始按「每周只推一项」加重","summary":"第 1 周完成了动作模式与负重基线的建立（负重俯卧撑 4×8-12、深蹲 4×12-15、保加利亚分腿蹲 3×10/腿）。第 2 周进入正式增肌期：每周只推进一个变量——先把同样负重从 8 次练到 12 次，再加 2-3kg 让次数回落。体重每周涨 0.25-0.5kg 为合适速度；饮水 ≥2.5L 照旧（结石预防）。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":7,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 最终话倒计时 7 天（9/30）：本周是补番的最后完整窗口","summary":"距离 9/30 最终话还有 7 天。夺还篇的认知博弈是全季密度最高的段落，本周内补完节奏最舒服。国产方面 False Memory 与时光代理人 S3 稳定输出。动漫区的官方海报与观看顺序已更新。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":8,"icon":"🍂","section":"季节与生活","headline":"秋分已过：昼短夜长开始，早晚温差继续拉大，作息与训练时间需要顺延调整","summary":"秋分（9/23 前后）之后北半球昼短夜长，广州早晚温差继续拉大。三个实际影响：①傍晚天黑得早，户外训练/快走建议提前到 18:30 前 ②早晚加薄外套，训练后及时换掉湿衣 ③增肌期睡眠 7-8 小时是硬指标（睡不够恢复不足，等于白练）。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"}
]
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡（含 3 张 Jev）')

# ==================== 2) ai-track 深度重写（Jev 专题）====================
aitrack = {
 "verdict": "🎯 一句话结论：Jev 不是【更强的模型】，而是一个【把服务对象从人换成程序】的判断组件。它值得你花一小时研究——不是因为现在要用，而是因为它把 AI 产品岗最核心的能力【判断什么该用 LLM、什么不该】具体化了。",
 "summary": "9月15日 TypeSafe 发布 Jev，定义为第一个【System One Model】。用法与所有大模型不同：给它一段 state（需要判断的上下文）+ 一组预先声明答案类型的 questions，它直接返回【选择 / 评分 / 真假判断 + 概率】，不生成任何文字。训练方法为 RLCD（Reinforcement Learning for Calibrated Decisions，面向校准决策的强化学习），配套新的模型架构与并行 sampler。工程上通过 Vercel AI SDK / AI Gateway 调用，questions 可分别声明为 Choice / Score / Boolean。上线 Gateway 24 小时内，近 13% 的付费团队已经用过它——这是该平台历史上采用最快的模型发布。",
 "trend": "<b>跟 LLM 的本质区别（四点）</b>：<br>① <b>输出形态</b>——LLM 逐个 token 生成一段文字，再由程序去解析 JSON；Jev 直接返回结构化的判断结果与概率，输出空间提前限定，不会出现 schema 之外的类型错误。<br>② <b>服务对象</b>——LLM 面向人（要解释、要可读），Jev 面向程序（要能直接用于下一步决策）。<br>③ <b>速度与成本</b>——实测 Jev 约 0.73 秒/题、50 题成本约 0.002 美元；同等任务上 DeepSeek V4 Flash 每题约 5.58 秒、成本约 2.5 倍。<br>④ <b>准确率并不占优</b>——50 条中文客服题实测，Jev 完整准确率约 64-65%，在便宜小模型组排第二；在更强模型组里排在最后（MiniMax M3 高约 10.8 个百分点，但只多花约 0.0035 美元、每题约 1.80 秒）。<br><br><b>两个必须看穿的宣传点</b>：<br>① <b>【零幻觉】的含义被窄化了</b>——它保证的是输出结构（不会跑出 D 选项），不代表判断正确（仍然可能把 A 选成 B）。<br>② <b>概率输出在阈值附近仍会波动</b>——实测中人工标注严重度下限 2.00，Jev 给 1.99；若业务规则是【≥2.00 转人工】，1.99 与 2.00 会被程序当成完全不同的信号。重复 15 次有 3 题出现通过/失分交替。",
 "tip": "<b>对你（AI 产品方向）的三个实际用法</b>：<br>① <b>面试素材</b>——把 Jev 讲成一个架构判断案例：Agent 执行中有大量边界清晰的小判断（能否交给便宜模型 / 检索是否相关 / 该调哪个工具 / 是否重试 / 另一个模型的答案是否可信），这些环节的接收者是程序，不该用通用大模型逐个生成文字回答。这直接呼应面试题【什么需求适合用大模型】。<br>② <b>验收标准的真实案例</b>——阈值陷阱（1.99 vs 2.00）说明：即使模型返回精确小数，业务规则仍必须处理波动、设计复核路径。这正是 AI 功能 PRD 里【异常与边界】该写的内容。<br>③ <b>成本结构的启示</b>——当单次判断成本降到千分之几美分，原本因成本只能抽样做的功能（如全量评论实时分类打标）变得可行。这是 AI 增长运营可以主动提的方向。<br><br><b>是否现在就用</b>：短期内【了解 &gt; 使用】。它不适合当聊天助手（它不说话），你目前也没有需要大量判断环节的后端系统。但它是理解【AI 系统内部分工】的最好样本。",
 "reasoning": "为什么 Jev 会火，以及为什么它值得关注：<br><b>① 团队的分量</b>——CEO Diogo Almeida 曾在 OpenAI 参与 InstructGPT 研究，是那篇 RLHF 论文的作者之一（该研究证明 13 亿参数的 InstructGPT 比 1750 亿参数的 GPT-3 更受评估者偏爱）。一位亲手推动语言模型变成好用助手的人，现在质疑自己参与推动的路线，这个转向本身就有信号意义。<br><b>② 它击中的行业疲惫</b>——发布故事越来越熟悉：更高分数、更长上下文、更强推理，然后等下一轮榜单。Almeida 在发布文章开头直接问：【模型在聊天上超越人类已经好几年了，自动化在哪里？】<br><b>③ 一个可检验的押注</b>——TypeSafe 给出的激进预期是：未来大规模 AI 自动化中，99% 的交互发生在机器之间，只有 1% 面向人。这个判断未必成立，但它把【模型该怎么被使用】这个问题重新摆上桌面。<br><b>④ 理念务实</b>——官网写 Build Prod, Not God（做能投入实际使用的产品，而不是造神）。<br><br>所以对求职者的价值在于：它是【AI 产品判断力】的活教材，而不是一个新工具。",
 "updated": TODAY
}
mt = re.search(r'\n  "ai-track": \{[\s\S]*?\n  \},', d) or re.search(r'\n  ai-track: \{[\s\S]*?\n  \},', d)
if mt:
    d = d[:mt.start()] + '\n  "ai-track": ' + j(aitrack) + ',' + d[mt.end():]
    print('✅ ai-track 已重写为 Jev 专题')
else:
    print('❌ MISS ai-track')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
