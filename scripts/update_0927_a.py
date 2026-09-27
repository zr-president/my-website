# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-09-27（周日）
   主题：国庆假期前的复盘与规划
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
assert TODAY == '2026-09-27', '日期不符：' + TODAY
print('目标日期：%s（%s）' % (TODAY, WD))


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 今日要闻 ====================
highlights = [
 {"priority":1,"icon":"📅","section":"假期安排","headline":"国庆假期临近：9/28-9/29 是节前最后两个交易日，10/1-10/7 休市，10/8 开市","summary":"本周只剩 9/28（周一）、9/29（周二）两个交易日，随后进入 10/1-10/7 长假。三件事需要提前定：① A股节前仓位（长假期间外盘不可控，七天无法交易等于被动承担风险）② 训练安排（假期是增肌最容易中断的时期，提前定好最低训练量）③ 学习节奏（假期适合维持而非冲刺）。生活助手区的办事日历已同步假期安排。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"},
 {"priority":2,"icon":"📈","section":"A股周末复盘","headline":"沪指 3900 关口第三周争夺收官：结构市特征延续，节前仓位需要提前决定","summary":"本周（9/22-9/26）沪指继续在 3900 附近震荡争夺，成交维持存量博弈区间。AI 硬件（覆铜板/光模块/元件）的相对强度仍在延续——9/11 提出的【结构主线】判断已连续第三周成立。下周仅 9/28-9/29 两个交易日，节前效应会让量能进一步收缩。当前框架：量能未放大前维持结构市判断；不追高；节前按自己的风险承受度决定是否降低仓位。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":3,"icon":"💪","section":"健身进展","headline":"增肌计划第 2 周收官：下周进入第 3 周，重点检查训练容量是否持续上升","summary":"第 2 周按【每周只推一项】推进（先把同样负重从 8 次练到 12 次，再加 2-3kg 让次数回落）。第 3 周的关键不是加更多动作，而是确认容量曲线：各动作的 组×次×负重 是否较上周上升、体重是否按 0.25-0.5kg/周 增长。若容量涨但体重不涨，说明吃少了——每天加 200 kcal（只调主食，蛋白不动）。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":4,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 最终话倒计时 3 天（9/30）：本周末是补番的最后窗口","summary":"距离 9/30 最终话仅剩 3 天，今天（周日）是补完夺还篇的最后完整窗口。国庆假期正好接上最终话与秋季新番。动漫区的官方海报与观看顺序已更新。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":5,"icon":"🎓","section":"求职节奏","headline":"国庆后是秋招关键窗口：假期前把作品集整理好，节后直接投","summary":"金九银十进入尾声，但国庆假期后往往还有一波密集招聘（企业新财年预算落地 + 秋招补录）。建议假期前完成两件事：① 把已有的产品分析整理成作品集（DSH 桌面端对比、Jev 接入决策、留存分析等都是现成素材）② 确认目标岗位清单与投递节奏。假期期间不适合密集投递，适合打磨材料。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":6,"icon":"🖥️","section":"AI 一周回顾","headline":"本周 AI 两件事：DSH 桌面端预览版上线（9/25）· Jev 决策模型持续发酵","summary":"① DSH 桌面端官方预览版 9/25 上线，Electron 实现、复用同一套 Web UI 与 Agent/工具/插件逻辑，需实名认证+充值；结论是继续用网页版。② Jev（首个 System One Model，不生成文字只输出判断+概率）持续被讨论，结论是现在不接入、列入待观察。完整对比表与决策依据在 AI 动态追踪。","action":"看 AI 追踪","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":7,"icon":"📚","section":"假期学习","headline":"假期学习策略：维持节奏 &gt; 集中冲刺，每天 40 分钟即可","summary":"长假最容易出现两种极端：完全不学导致节后重启成本高，或者计划过满导致一天都没完成。更稳的做法是设一个【最低维持量】——每天 40 分钟（如 2 道 SQL + 1 道判读题），保持习惯连续性。能力训练平台的 30 天计划可以按天补，不必追求假期内跑完全部。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":8,"icon":"🍂","section":"生活与健康","headline":"假期作息提醒：昼夜节律一旦打乱，节后恢复通常需要 3-5 天","summary":"长假期间最容易打乱的是作息。昼夜节律紊乱会直接影响训练恢复与白天专注度，且节后恢复通常需要 3-5 天。三个具体建议：① 起床时间浮动不超过 1 小时 ② 训练最低量每天 15 分钟自重训练 ③ 饮水 ≥2.5L 照旧（结石预防）。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"}
]
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡（9/27 周日版）')

# ==================== 每日一词 ====================
words = [
 {"emoji":"🤖","category":"AI","word":"多模态 (Multimodal)","definition":"模型能同时理解多种输入形式（文字、图像、音频、视频），而不仅限于文本。","example":"原生支持视觉的模型可以直接读截图并回答图里的问题，不需要先用 OCR 转文字。","why_matters":"【能看图】是应用层的分水岭——大量业务数据是图片形式（票据、截图、商品图），此前必须先转文本才能处理。"},
 {"emoji":"🔧","category":"技术","word":"本地优先 (Local-first)","definition":"数据默认存在用户本机、而不是服务器，功能在本机即可完整运行的设计取向。","example":"训练平台的进度存在浏览器 localStorage，不上传服务器；个人网站的数据存本机。","why_matters":"它把隐私成本降到最低，同时保留完整功能。对个人工具类产品，这是比【云端同步】更合适的选择。"},
 {"emoji":"📊","category":"运营","word":"RFM 分层","definition":"按最近一次消费（Recency）、消费频率（Frequency）、消费金额（Monetary）三个维度给用户分层。","example":"高 R 高 F 高 M = 核心用户；低 R 高 F = 流失预警的高价值用户。","why_matters":"它把【用户】拆成可运营的群体，让动作有针对性——而不是对所有人发同样的券。"},
 {"emoji":"💪","category":"健身","word":"增肌平台期","definition":"训练一段时间后进步停滞，同重量与次数长期无法突破的状态。","example":"第 3-4 周常见：动作模式已熟悉，但容量没继续上升。","why_matters":"平台期通常不是训练问题，而是【吃不够或睡不够】。先检查热量与睡眠，再考虑改计划。"},
 {"emoji":"📈","category":"财经","word":"仓位管理","definition":"决定投入多少比例资金、留多少现金的纪律，独立于【买什么】的判断。","example":"长假前把仓位从 8 成降到 5 成，是为了应对七天不可交易的风险。","why_matters":"很多人只研究买什么，却忽略了【拿多少钱在里面】才是决定回撤幅度的关键变量。"},
 {"emoji":"🎓","category":"求职","word":"秋招节奏","definition":"秋季招聘的时间窗口规律：9-10 月为高峰，国庆后常有一波补录与预算落地后的新岗位。","example":"国庆后两周往往是投递的第二个高峰，竞争比 9 月略低。","why_matters":"把材料准备放在假期、把投递放在节后，能避开节前的拥挤并赶上新增岗位。"},
 {"emoji":"💰","category":"理财","word":"流动性分层","definition":"按【什么时候要用】把钱分开放：随时用、1-3 年用、5 年以上不用，对应不同风险等级的产品。","example":"应急金放货币基金（T+0），首付放存单，长期资金才做定投。","why_matters":"不分层是亏钱最常见的原因——用短期要用的钱去承担长期波动，就会被迫在低位卖出。"},
 {"emoji":"🧠","category":"学习","word":"间隔重复 (Spaced Repetition)","definition":"把学习内容分散到多个时间点复习，而不是一次集中学完。","example":"同一批 SQL 题，隔 2 天、7 天、21 天各重做一次，效果优于一天刷三遍。","why_matters":"集中学习带来的是短期熟悉感，间隔重复才能形成长期记忆——这也是错题本该定期重做的原因。"},
 {"emoji":"🍂","category":"生活","word":"假期综合征","definition":"长假后出现的注意力不集中、效率下降、作息紊乱等状态，通常需要数天恢复。","example":"假期后第一周上班/学习效率明显低于平时。","why_matters":"提前把作息浮动控制在 1 小时内，能把恢复期从 3-5 天压到 1 天。"},
 {"emoji":"⚖️","category":"产品","word":"灰度发布","definition":"新功能先对小比例用户开放，观察指标正常后再逐步扩大范围的发布方式。","example":"先在 1% 用户上线，观察客诉与核心指标，再放量到 10%、50%、100%。","why_matters":"AI 功能尤其需要灰度——效果不确定性高，一次全量上线出问题的成本远大于分批放量。"}
]
m = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_VOCAB = {\n  date: "%s",\n  words: %s\n};' % (TODAY, j(words)) + d[m.end():]
    print('✅ 每日一词 → 10 词（10 个领域）')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
