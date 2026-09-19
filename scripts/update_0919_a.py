# -*- coding: utf-8 -*-
"""个人网站更新 → 2026-09-19（周六）
   距上次内容日期 9/14 相隔 5 天（含 9/14-9/18 完整交易周），内容需实质刷新而非只改日期
"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'

now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
WD = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][now.weekday()]
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
MMDD = '%d月%d日' % (now.month, now.day)
print('目标日期：%s（%s）' % (TODAY, WD))
assert TODAY == '2026-09-19', '日期不符，请先确认系统时间'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 1) 今日要闻（8 卡，覆盖 5 天变化）====================
highlights = [
 {"priority":1,"icon":"💪","section":"健身复盘","headline":"增肌计划第 1 周收官：俯卧撑已开始加负重，下周重点是「每周只推一项」","summary":"9/14 起执行增肌版计划（4 力量日 + 1 有氧日，新增下肢训练）。第 1 周目标是把动作模式和负重基线立起来：负重俯卧撑 4×8-12、深蹲 4×12-15、保加利亚分腿蹲 3×10/腿。下周进入增肌期，加重原则是【每周只推一项】——先把同样负重从 8 次练到 12 次，再加 2-3kg 让次数回落。体重每周涨 0.25-0.5kg 为合适速度。","action":"看计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":2,"icon":"📈","section":"A股周复盘","headline":"一周行情：3900 关口反复争夺，AI 硬件仍是唯一有持续性的结构主线","summary":"9/14-9/18 这一周，指数在 3900 附近反复争夺，成交量维持在 1.8-2 万亿区间；结构上 AI 硬件（覆铜板/光模块/元件）延续了 9/11 以来的相对强势，其余板块轮动快、持续性弱。上周提出的判断【AI 硬件是结构主线】在本周得到验证；下周需观察：能否有效站稳 3900，以及量能是否配合放大。当前策略不变——赚钱效应不足时不追高。","action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":3,"icon":"🐳","section":"DeepSeek V4.1 Flash","headline":"V4.1 Flash 开源生态一周进展：私有化部署方案开始成型，成本结构变化比榜单更重要","summary":"V4.1 Flash（9/10 发布）开源权重放出满一周，社区围绕它的量化版本、垂直微调与本地部署方案陆续出现。对应用侧的意义不在于跑分，而在于【此前因成本或数据合规做不了的场景重新可行】——例如含客户联系方式的跟进记录摘要、内部知识库问答，现在可以走本地开源模型，单次成本能低一个数量级。这是应用层的机会窗口。","action":"深度解读","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":4,"icon":"🎓","section":"求职准备","headline":"金九银十第三周：AI 产品岗的能力描述已明确从「会用工具」转向「会定义边界」","summary":"9 月第三周，AI 产品岗的 JD 变化更清晰：过去写【熟悉大模型工具/Prompt 工程】，现在更多写【能判断什么该用与不该用模型、能定义验收标准与兜底路径】。这对转型者是好消息——它把考核重点从【工具熟练度】移到【判断力与方案能力】，而后者可以通过训练补齐。能力训练平台的 AI 产品经理模块（判读题 + PRD 工坊 + 面试题库）正是针对这个转向设计的。","action":"去训练","link":"#career","deepLink":"https://zr-president.github.io/training/"},
 {"priority":5,"icon":"🤖","section":"AI 工程趋势","headline":"Agentic Workflow 成为分水岭：面试题从「怎么写好 Prompt」变成「怎么设计能完成任务的 Agent」","summary":"行业讨论重心持续从单次问答转向多步任务编排：拆解目标、调用工具、校验结果、失败重试、必要时转人工。相关能力已加入能力训练平台的 AI Agent 实操模块（判读 + 提效计算器 + 4 个实操任务 + 3 份模板）。建议的准备方式：把【写周报 Agent】做成一个含异常处理的完整设计，比堆 Prompt 技巧更有说服力。","action":"看 Agent 实操","link":"#ai-track","deepLink":"https://zr-president.github.io/training/#/agent"},
 {"priority":6,"icon":"🍽️","section":"饮食调整","headline":"增肌饮食执行第 1 周：训练日 2500 / 休息日 2300 kcal，体重变化是唯一校准依据","summary":"新饮食方案执行一周：训练日 2500 kcal、休息日 2300 kcal，蛋白保持 110-130g。判断是否吃对只有一个标准——体重每周涨 0.25-0.5kg。完全不涨就每天再加 200 kcal（优先加碳水和蛋白）；涨超过 0.75kg/周就减 200 kcal。调热量只调主食，不动蛋白质；饮水 ≥2.5L 照旧（结石预防）。","action":"看食谱","link":"#diet","deepLink":"#diet"},
 {"priority":7,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 最终话 9/30 定档，倒计时 11 天：本周补番窗口正在收窄","summary":"Re:Zero S4【夺还篇】最终话 9/30，距离现在 11 天。这是本季最值得补的一部——夺还篇的认知博弈是全季密度最高的段落。国产方面 False Memory 与时光代理人 S3 稳定输出。动漫区的官方海报与观看顺序已更新。","action":"看动漫区","link":"#anime","deepLink":"#anime"},
 {"priority":8,"icon":"🍂","section":"生活与季节","headline":"秋分将至：昼夜温差继续拉大，这是全年最容易感冒的两周","summary":"9 月下旬广州进入秋分前后，白天仍可到 32-33℃，夜间回落到 24-25℃，温差接近 9℃。这个阶段的三件事：①早晚加薄外套，别硬扛 ②运动后及时换掉湿衣 ③增肌期睡眠保持 7-8 小时（睡不够等于白练）。办事日历与生活助手区已同步更新。","action":"看生活助手","link":"#life-tips","deepLink":"#life-tips"}
]

m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_BRIEFING = {\n  date: "%s",\n  highlights: %s\n};' % (TODAY, j(highlights)) + d[m.end():]
    print('✅ 今日要闻 → 8 卡（9/19 版）')

# ==================== 2) 每日一词（跨领域 10 条）====================
words = [
 {"emoji":"🔥","category":"健身","word":"热量盈余 (Caloric Surplus)","definition":"每日摄入热量高于消耗，为肌肉合成提供原料。增肌建议每天 +200 kcal 左右。","example":"59kg 的人维持约 2300 kcal，训练日吃到 2500 kcal 即为轻微盈余。","why_matters":"盈余过大脂肪一起长；没有盈余长不出肌肉。轻微盈余才叫 lean bulk。"},
 {"emoji":"📊","category":"财经","word":"量能配合 (Volume Confirmation)","definition":"价格突破关键位时，成交量同步放大才算有效突破。","example":"指数站上 3900 但成交萎缩 → 突破可信度低，容易假突破。","why_matters":"只看价格会误判。量能是判断突破真假最直接的工具。"},
 {"emoji":"🧩","category":"AI","word":"上下文工程 (Context Engineering)","definition":"系统性设计喂给模型的全部上下文（系统提示、检索片段、历史、工具返回、格式约束），而非只雕琢一句 Prompt。","example":"同一句提问，附上 3 条检索原文 + 输出格式约束，质量完全不同。","why_matters":"模型能力趋同后，产品差异取决于【喂什么上下文】，这是 RAG 类产品真正的护城河。"},
 {"emoji":"⭐","category":"运营","word":"留存曲线 (Retention Curve)","definition":"按注册时间分组，追踪同一批用户在各时间点的留存率变化。","example":"9/14 注册的 100 人，次日回来 45 人、7 日回来 22 人。","why_matters":"曲线走平的位置决定产品价值——走平越早、越高，说明用户越稳定。"},
 {"emoji":"🥩","category":"营养","word":"蛋白质分配 (Protein Distribution)","definition":"把每日蛋白总量分散到 4-6 餐，每餐 25-40g，而不是一顿猛吃。","example":"120g 蛋白 → 早餐 25g + 加餐 15g + 午餐 35g + 练后 25g + 晚餐 20g。","why_matters":"单次摄入过高利用率下降；分散摄入对肌肉合成的刺激更持续。"},
 {"emoji":"🔗","category":"AI","word":"Agentic Workflow","definition":"把任务拆成多步，由模型自主决定调用哪些工具、按什么顺序执行、失败如何重试。","example":"写周报 Agent：取数 → 校验 → 生成解读 → 自检是否编造数字 → 落库待审。","why_matters":"这是 AI 从【回答问题】走向【完成任务】的关键，也是当前面试的分水岭。"},
 {"emoji":"🧠","category":"学习","word":"刻意练习 (Deliberate Practice)","definition":"针对薄弱点设计的高强度、有即时反馈的练习，而非重复已会的内容。","example":"SQL 只练错题本里的题，比从头刷一遍效率高得多。","why_matters":"重复做会的题只是熟练度错觉。真正的进步来自持续攻击不会的部分。"},
 {"emoji":"🦵","category":"健身","word":"复合动作 (Compound Movement)","definition":"同时调动多个关节与肌群的动作，如深蹲、硬拉、划船、俯卧撑。","example":"保加利亚分腿蹲同时练股四头肌、臀大肌与核心稳定。","why_matters":"复合动作的增肌效率远高于孤立动作，居家条件下应放在训练日开头。"},
 {"emoji":"🏛️","category":"生活","word":"秋分 (Autumnal Equinox)","definition":"太阳直射赤道、昼夜等长的节气，此后北半球昼短夜长。","example":"秋分前后昼夜温差接近 9℃，是全年最容易感冒的两周。","why_matters":"温度变化快于身体适应速度。早晚加薄外套比事后吃药划算得多。"},
 {"emoji":"🎯","category":"求职","word":"作品集 (Portfolio)","definition":"用可验证的产出证明能力，而不是用形容词描述能力。","example":"一份【AI 功能 PRD（含异常与边界）】比一堆 Prompt 技巧合集更有说服力。","why_matters":"转型面试中，能拿出可验证产出的人会被当成【已经做过】，而不是【想转行】。"}
]
m2 = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m2:
    d = d[:m2.start()] + 'var DAILY_VOCAB = {\n  date: "%s",\n  words: %s\n};' % (TODAY, j(words)) + d[m2.end():]
    print('✅ 每日一词 → 10 词（5 个领域）')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
