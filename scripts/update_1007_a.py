# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-10-07（周三 · 假期最后一天）
   主题：假期收官 + 明日（10/8）开市准备
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
assert TODAY == '2026-10-07', '日期不符：' + TODAY
print('目标：%s（%s · 假期最后一天）' % (TODAY, WD))


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

highlights = [
 {"priority":1,"icon":"📅","section":"假期收官","headline":"10月7日：国庆假期最后一天，明日 10/8（周四）恢复交易与工作","summary":"七天假期今天结束。收官日该做的不是继续放松，而是把节奏调回来 —— 三件事：① 今晚把睡觉时间往前调（明早固定时间起床，这是昼夜节律唯一的锚点）② 复盘假期三条边界的执行情况（训练/作息/学习各打了几次勾）③ 准备好明天要用的东西（投递材料、开市观察清单）。假期执行得怎么样不重要，重要的是明天能不能接上。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"},
 {"priority":2,"icon":"📈","section":"A股明日开市","headline":"10/8 恢复交易：假期七天无法操作，开盘存在跳空可能，先看信号再动手","summary":"长假期间海外市场照常运行，而你的持仓无法调整，因此 10/8 开盘价可能直接跳过 9/30 的收盘区间——这就是【跳空】。应对原则：① 开盘前先核对假期期间外盘的实际表现（不猜，去看）② 10/1 定下的三个观察点按顺序验证（量能能否放大 / 3900 能否有效站稳 / AI 硬件主线是否延续）③ 跳空不改逻辑，只改价格；逻辑没变就不因为价格恐慌操作。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":3,"icon":"💪","section":"健身进展","headline":"增肌第 3 周收官：假期训练执行复盘 + 明日恢复正式计划","summary":"假期七天如果守住了【每天最低 15 分钟自重】，连续性就保住了，节后回健身房不会有明显的能力回落。收官日做两件事：① 统计假期共完成几次训练（哪怕只有 3 次也算成功，比 0 次好得多）② 定好明天回健身房的第一练内容——建议用较轻重量重新激活，而不是直接上假期前的极限重量。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":4,"icon":"🎓","section":"求职节奏","headline":"节后第一波投递从明天开始：假期准备的材料该用出去了","summary":"国庆后通常有一波招聘窗口（企业新财年预算落地 + 秋招补录）。如果假期把作品集整理好了，明天就是投递的正确时机；如果没整理完，明天先把【最想去的 3 家】的材料补齐再投，不要等全部完美。投递节奏建议：先投 3-5 家试水，根据反馈调整表述，再扩大范围。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":5,"icon":"🍂","section":"健康作息","headline":"今晚是把生物钟调回来的最后窗口：明早固定时间起床","summary":"假期作息若已打乱，节后恢复期通常需要 3-5 天，而今晚是压缩这个恢复期的关键窗口。方法只有一条但有效：明早按工作日的固定时间起床（哪怕昨晚睡得晚），不补觉到中午。起床时间是昼夜节律最强的锚点，它一旦固定，后续几天会自然回正。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"},
 {"priority":6,"icon":"📚","section":"假期学习","headline":"假期最低维持量复盘：重点不是完成了多少，而是有没有断过","summary":"假期学习的唯一目标是【不断】，而不是【学多少】。收官统计一下：七天里有几天完成了 40 分钟的最低量？如果连续做到了 4 天以上，说明这个量定得合理，节后可以沿用；如果只做到 1-2 天，说明 40 分钟对你偏高，明天应该把标准降到 20 分钟。计划能持续的前提是它足够小。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":7,"icon":"🎬","section":"动漫追番","headline":"秋季新番开播第一周：先看评分再决定追哪几部","summary":"Re:Zero 夺还篇已于 9/30 收官，秋季新番陆续开播。第一周不建议立刻决定追番名单——新番通常在第 2-3 周才看得出质量。可以先用第一集做筛选，把明显不合口味的排除，剩下的观察两集再定。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":8,"icon":"🤖","section":"AI 动态","headline":"节后 AI 待办：把假期的两份产品分析文档收尾","summary":"假期的计划是把 DSH 桌面端对比与 Jev 接入决策写成分产品分析文档。如果已完成，明天可以直接用于投递；如果还没写，明天用 40 分钟把框架搭出来（背景→对比维度→结论与依据→改变结论的条件），不需要一次写完。这两份文档的价值在于展示架构判断力，而不是文采。","action":"看 AI 追踪","link":"#ai-track","deepLink":"#ai-track"}
]
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡（10/7 假期收官版）')

words = [
 {"emoji":"🤖","category":"AI","word":"上下文窗口 (Context Window)","definition":"模型单次能记住并处理的文本长度上限，通常以 token 计。","example":"窗口 128K 大约相当于一次能读 6-8 万字的中文材料。","why_matters":"它决定了哪些任务能一次性交给模型（如读完一份长报告），哪些必须先拆分。产品设计时这是个硬约束。"},
 {"emoji":"🔧","category":"技术","word":"幂等 (Idempotent)","definition":"同一个操作执行一次和执行多次，结果相同。","example":"【把余额设为 100】是幂等的；【余额加 10】不是。","why_matters":"网络会重试，用户会连点。不幂等的接口在重试时会造成重复扣款、重复下单 —— 这是生产事故的高频来源。"},
 {"emoji":"📊","category":"运营","word":"转化漏斗","definition":"把用户从进入到完成目标的过程拆成多个环节，逐环节看流失。","example":"1000 人访问 → 300 人注册 → 90 人下单 → 60 人复购。","why_matters":"它把【效果不好】这个模糊问题拆成【哪一步漏得最多】，让优化有明确的发力点。"},
 {"emoji":"💪","category":"健身","word":"恢复期 (Recovery)","definition":"训练结束后身体修复并变强的时间段，通常是 24-72 小时。","example":"大肌群训练后需要约 48 小时才恢复；恢复不足时力量会下降。","why_matters":"肌肉是在恢复期长的，不是在训练时长的。练得勤但睡不够，等于一直在破坏而没有重建。"},
 {"emoji":"📈","category":"财经","word":"量价背离","definition":"价格走势与成交量方向不一致，通常被视为趋势可能反转的信号。","example":"指数创新高但成交量比前一周明显萎缩 —— 缩量上涨。","why_matters":"价格可以靠少量资金拉起来，但持续的上涨需要成交量配合。背离是【上涨质量差】的提示。"},
 {"emoji":"🎓","category":"求职","word":"作品集 (Portfolio)","definition":"用具体项目展示能力的材料集合，重点是可验证的产出而非自述。","example":"一份含【背景-分析-结论-数据】的产品分析文档，胜过十句【我具备分析能力】。","why_matters":"它把抽象的【能力】变成可检验的【证据】。对转行或经验不足的人，作品集往往比简历更有说服力。"},
 {"emoji":"💰","category":"理财","word":"应急金","definition":"专门用于应对失业、疾病等突发状况的现金储备，通常覆盖 3-6 个月支出。","example":"月支出 5000 元 → 应急金 1.5 万-3 万元，放在随时可取的地方。","why_matters":"它的作用不是赚收益，而是让你在意外发生时不必在低位卖出长期资产。这是整个理财计划的地基。"},
 {"emoji":"🧠","category":"学习","word":"费曼技巧","definition":"把学到的东西用最通俗的语言讲给外行听，讲不通的地方就是没懂的地方。","example":"试着不用术语解释【什么是幂等】，卡住的地方就是理解缺口。","why_matters":"它把【自我感觉懂了】暴露成【具体哪里没懂】，是检验理解深度最快的方法。"},
 {"emoji":"🍂","category":"生活","word":"节后综合征","definition":"长假结束后出现的注意力涣散、疲惫、效率下降等状态。","example":"假期后第一天上班，看什么都提不起劲。","why_matters":"它主要是作息紊乱造成的，而非意志力问题。提前一天把起床时间固定，能显著减轻。"},
 {"emoji":"⚖️","category":"产品","word":"MVP (最小可行产品)","definition":"用最小成本做出能验证核心假设的版本，先确认方向对不对再投入。","example":"先做一个只有核心功能的页面测试用户是否愿意用，而不是先开发完整系统。","why_matters":"它把【一次性做对】换成【快速试错】。大部分产品的失败源于方向错误，而不是功能不足。"}
]
m = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_VOCAB = {\n  date: "%s",\n  words: %s\n};' % (TODAY, j(words)) + d[m.end():]
    print('✅ 每日一词 → 10 词（10 个领域）')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
