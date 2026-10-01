# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-10-01（周四 · 国庆节）
   主题：假期第 1 天 —— 从"节前准备"切到"假期执行"
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
assert TODAY == '2026-10-01', '日期不符：' + TODAY
print('目标：%s（%s · 国庆节）' % (TODAY, WD))


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 今日要闻 ====================
highlights = [
 {"priority":1,"icon":"🇨🇳","section":"国庆节","headline":"10月1日国庆节：假期第 1 天，10/1-10/7 共七天","summary":"国庆假期正式开始。七天里三件事值得提前定好边界：① 训练（假期最容易整个停练，建议每天最低 15 分钟自重训练）② 作息（起床时间浮动控制在 1 小时内，节后恢复期能从 3-5 天压到 1 天）③ 学习（每天 40 分钟最低维持量，不追求冲刺）。假期不是空白期，是节奏管理期。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"},
 {"priority":2,"icon":"📈","section":"A股休市","headline":"A股 10/1-10/7 休市，10/8（周四）开市；假期无法交易，仓位已定","summary":"长假期间 A股 停止交易，10/8 恢复。这意味着：假期里任何外盘波动你都只能被动承接，无法操作。所以假期更该做的是【复盘】而不是【看盘】——把 9 月这波 3900 关口争夺的判断逻辑梳理清楚，为 10 月开市做准备。海外市场在假期期间仍在交易，10/8 开盘可能出现跳空。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":3,"icon":"💪","section":"健身进展","headline":"增肌计划进入第 3 周，假期训练是本月最容易断的一环","summary":"第 3 周的核心任务是确认容量曲线是否还在上升（组×次×负重 对比上周）。假期期间健身房可能休息或时间不固定，提前定好【最低训练量】：每天 15 分钟自重（俯卧撑/深蹲/卷腹/平板支撑），维持习惯连续性比单次强度更重要。若假期饮食热量不足，第 3 周体重可能不涨 —— 那就把主食加回来。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":4,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 夺还篇最终话已于 9/30 播出，秋季新番接档","summary":"追了一季的 Re:Zero 夺还篇在 9/30 收官，正好接上秋季新番。假期是补番与新番同时开始的最佳窗口。动漫区已更新秋季新番表与观看顺序建议。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":5,"icon":"🎓","section":"求职节奏","headline":"假期做材料、节后集中投递：国庆后是秋招第二波窗口","summary":"国庆后通常有一波招聘（企业新财年预算落地 + 秋招补录）。假期的正确用法是把作品集打磨完，而不是投递 —— 节日期间 HR 基本不处理简历。可以完成的三件事：① 把已有的产品分析整理成可展示的文档（DSH 桌面端对比、Jev 接入决策、留存分析等）② 更新简历里的项目描述 ③ 列出节后要投的公司清单与优先级。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":6,"icon":"📚","section":"假期学习","headline":"最低维持量执行：每天 40 分钟，假期第 1 天先跑通一次","summary":"假期的学习计划最大的风险不是学少了，而是【第一天就没做到】从而导致整个计划作废。所以第 1 天的目标只有一个：跑通一次。做 2 道 SQL + 1 道 AI 判读题就够，用训练平台的按天打勾记录。习惯连续性是唯一指标。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":7,"icon":"🍂","section":"健康作息","headline":"假期作息管理：只守一个指标 —— 起床时间浮动不超过 1 小时","summary":"长假最容易打乱的是作息，而昼夜节律一旦紊乱，节后恢复通常要 3-5 天。守住起床时间这一项就够了 —— 它是昼夜节律最强的锚点。其余（几点睡、午睡多久）可以宽松。另外饮水 ≥2.5L 照旧，这是结石预防的硬指标。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"},
 {"priority":8,"icon":"🤖","section":"AI 动态","headline":"假期值得复盘的 AI 两条线：DSH 桌面端（9/25 预览）· Jev 决策模型","summary":"本周没有需要立刻行动的新变化，适合把 9 月积累的两条线整理成结论：① DSH 桌面端 vs 网页版的取舍（结论：求职期继续用网页版）② Jev 该不该接入（结论：现在不接入，列入待观察）。把这两份分析写成可展示的产品文档，是假期性价比最高的产出 —— 它直接服务求职。","action":"看 AI 追踪","link":"#ai-track","deepLink":"#ai-track"}
]
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡（10/1 国庆版）')

# ==================== 每日一词 ====================
words = [
 {"emoji":"🤖","category":"AI","word":"推理成本 (Inference Cost)","definition":"模型每回答一次所消耗的算力费用，通常按输入+输出的 token 数计费。","example":"同一个问题，用大模型答要 0.02 元，用小模型答只要 0.0005 元。","why_matters":"它决定了哪些功能可以全量上线、哪些只能抽样。产品设计时要先算这笔账，再决定用哪个模型。"},
 {"emoji":"🔧","category":"技术","word":"冷启动 (Cold Start)","definition":"程序第一次运行或缓存为空时的启动过程，通常比后续启动慢很多。","example":"第一次跑 DSH 要下载 200MB 依赖，之后启动只要几秒。","why_matters":"冷启动是用户流失的高发环节。能预热就预热，能把依赖提前装好就别留到第一次用。"},
 {"emoji":"📊","category":"运营","word":"留存曲线","definition":"把不同时间点的留存率连成的曲线，用来判断产品是否真的留住了用户。","example":"次日留存 45%、7 日 25%、30 日 18% 是一条还算健康的曲线。","why_matters":"曲线在某个点之后走平，说明找到了核心用户；一直下滑则说明产品只是新鲜感。"},
 {"emoji":"💪","category":"健身","word":"训练容量 (Volume)","definition":"训练总量，通常用 组数 × 次数 × 负重 来衡量。","example":"4 组 × 10 次 × 40kg = 1600kg 的总容量。","why_matters":"增肌的核心变量是容量的渐进上升，而不是动作的花样。每周只推一项，才看得出是不是在进步。"},
 {"emoji":"📈","category":"财经","word":"跳空缺口","definition":"开盘价直接跳过前一日价格区间，中间留下一段没有成交的空白区域。","example":"长假后开盘受外盘影响，直接低开 2% 且未回补。","why_matters":"长假是跳空的高发场景（期间外盘在动但你无法交易）。这正是【节前决定仓位】的意义所在。"},
 {"emoji":"🎓","category":"求职","word":"STAR 法则","definition":"描述经历的结构：情境（Situation）、任务（Task）、行动（Action）、结果（Result）。","example":"【日活下滑 12%（S）→ 我要定位原因（T）→ 做了分渠道拆解（A）→ 发现是某渠道质量问题（R）】","why_matters":"面试官真正想听的是【你怎么想的】，而不是【你做了什么】。STAR 强制把思考过程讲出来。"},
 {"emoji":"💰","category":"理财","word":"复利","definition":"收益本身继续产生收益，时间越长效果越显著。","example":"10 万元年化 3%，10 年后约 13.4 万；若年化 6%，约 17.9 万。","why_matters":"它解释了为什么【早开始】比【追求高收益】更重要，也解释了为什么不该用短期要用的钱去冒险。"},
 {"emoji":"🧠","category":"学习","word":"主动回忆 (Active Recall)","definition":"合上材料，主动把内容回忆出来，而不是反复阅读。","example":"看完一章后合上书，写下记得的要点，再对照查漏。","why_matters":"重读带来的是【熟悉感】，回忆才是【提取练习】。后者才真正形成长期记忆。"},
 {"emoji":"🍂","category":"生活","word":"社交时差 (Social Jet Lag)","definition":"工作日与休息日作息差异过大，造成的类似倒时差的疲惫感。","example":"平时 7 点起，假期每天 11 点起，节后像出了趟国。","why_matters":"假期的起床时间浮动控制在 1 小时内，就能避免节后那 3-5 天的恢复期。"},
 {"emoji":"⚖️","category":"产品","word":"A/B 测试","definition":"把用户随机分成两组，分别看不同版本，用数据判断哪个更好。","example":"一半用户看到新版按钮，一半看旧版，比较点击率。","why_matters":"它把【我觉得】变成【数据显示】。但前提是指标选对 —— 指标错了，结论就错了。"}
]
m = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_VOCAB = {\n  date: "%s",\n  words: %s\n};' % (TODAY, j(words)) + d[m.end():]
    print('✅ 每日一词 → 10 词（10 个领域）')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
