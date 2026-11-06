# -*- coding: utf-8 -*-
"""个人网站 2026-11-06（周五）刷新 · 第二步
1) DAILY_BRIEFING 8 卡
2) DAILY_VOCAB 10 词 / 10 领域
3) LEARN_PATHS 10 条 + 旧条归档到 archive['2026-10-26'] + current_day 28→29
4) DAILY_DECISIONS 5 条
5) DAILY_DATA.update_date → 2026年11月6日
6) 同步所有 updated 字段（只动 updated，绝不动 archive 键）
7) 升版本 1.8.41 → 1.8.42（三处）
"""
import io, sys, os, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(r'C:\Users\ZR\Desktop\钟锐的个人网站')

TODAY = '2026-11-06'
OLD_ARCHIVE_KEY = '2026-10-26'
NEW_VER = '1.8.42'
OLD_VER = '1.8.41'
D = '11月6日（周五）'

# ============================================================
# 通用工具
# ============================================================
def find_decl(text, name):
    m = re.search(r'var\s+' + re.escape(name) + r'\s*=', text)
    return m.end() if m else None

def brace_extent(text, start):
    """从 start 起找第一个 { 或 [，返回配对结束位置（含）"""
    i = start
    while i < len(text) and text[i] not in '{[':
        i += 1
    if i >= len(text):
        return None, None
    open_ch = text[i]
    close_ch = '}' if open_ch == '{' else ']'
    depth = 0
    instr = None
    j = i
    while j < len(text):
        c = text[j]
        if instr:
            if c == '\\':
                j += 2
                continue
            if c == instr:
                instr = None
            j += 1
            continue
        if c in '"\'':
            instr = c
            j += 1
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    return None, None

def get_block(text, key, base=0):
    m = re.search(r'(?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\{', text[base:])
    if not m:
        return None, None
    i = base + text[base:].index('{', m.start())
    depth = 0
    instr = None
    j = i
    while j < len(text):
        c = text[j]
        if instr:
            if c == '\\':
                j += 2
                continue
            if c == instr:
                instr = None
            j += 1
            continue
        if c in '"\'':
            instr = c
            j += 1
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    return None, None

def get_array_block(text, key, base=0):
    m = re.search(r'(?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\[', text[base:])
    if not m:
        return None, None
    i = base + text[base:].index('[', m.start())
    depth = 0
    instr = None
    j = i
    while j < len(text):
        c = text[j]
        if instr:
            if c == '\\':
                j += 2
                continue
            if c == instr:
                instr = None
            j += 1
            continue
        if c in '"\'':
            instr = c
            j += 1
            continue
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    return None, None

def js(obj, indent=2):
    return json.dumps(obj, ensure_ascii=False, indent=indent)

text = open('daily_data.js', encoding='utf-8').read()
orig = len(text)

# ============================================================
# 1) DAILY_BRIEFING
# ============================================================
BRIEF = {"date": TODAY, "highlights": [
 {"priority":1,"icon":"📈","section":"A股复盘",
  "headline":"11 月首个完整交易周收官 · 三季报空窗期开始",
  "summary":"%s，11/2-11/6 是 11 月第一个完整交易周，今天收官。三季报已于 10/31 全部披露完毕，从现在到明年 1 月进入【业绩空窗期】——没有财报催化，行情由资金面与政策预期主导。判断依据要切换：从【看业绩】改为【看资金是否连续净流入】，单日放量不算，连续 3 天才算。" % D,
  "action":"看复盘","link":"#stock","deepLink":"#stock"},
 {"priority":2,"icon":"🎓","section":"学习学院",
  "headline":"金融课 9 单元全部成稿 · 从「指数是什么」到「把钱分成几份」",
  "summary":"本周把训练场的学院结构重做了：一个领域一门课、课内 4-9 个由浅入深的单元。金融课 9 个单元已全部成稿——指数与估值 → 货币利率通胀 → 资产类别 → A股与美股 → 基金费率 → 估值进阶 → 债券利率风险 → 汇率与海外资产 → 综合实战配置。每单元 7 步，含 3 级提示阶梯与 3 天后复测。",
  "action":"去学院","link":"https://zr-president.github.io/training/#/academy","deepLink":"#career"},
 {"priority":3,"icon":"💪","section":"健身",
  "headline":"训练第 11 个月 · 冬季先改热身再谈重量",
  "summary":"%s，基线：170cm / 60.65kg / BMI 21.0 / 体脂约 12-14%%。11 月主线是【维持 + 弱项补强】，不冲大重量——冬季恢复变慢，受伤成本高于收益。最该改的是热身：从 8 分钟延长到 12 分钟，每个训练日第一组降 10%% 重量做过渡组。热量训练日 2600 / 休息日 2400 kcal，蛋白 130-140g 不变。" % D,
  "action":"看健身","link":"#fitness","deepLink":"#fitness"},
 {"priority":4,"icon":"🎮","section":"游戏",
  "headline":"影之刃零 10/29 已发售 · 首周口碑窗口怎么读",
  "summary":"%s，影之刃零已于 10/29 发售，现在处于首周窗口。这是判断 3A 值不值得买的最佳时点：媒体评分、实机帧数、通关时长三项数据齐了，剧透还没扩散。只看三项——战斗手感是否被反复提到、帧数表现、主线时长。不要看首发日的短视频评价，那是宣发期内容。" % D,
  "action":"看游戏","link":"#gaming","deepLink":"#gaming"},
 {"priority":5,"icon":"🤖","section":"AI 动态",
  "headline":"Agent 工程化成为重心 · 静默失败最危险",
  "summary":"%s，行业讨论的重心已从【模型能做什么】转向【怎么让流程可靠地跑完】：失败重试、人工介入点、成本上限、输出验收。最危险的是静默失败——格式正确但内容错误，且不报错。工程对策是强制输出证据 + 必须能说不知道，做不到这两点的不该接入决策链。" % D,
  "action":"看 AI","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":6,"icon":"💼","section":"求职",
  "headline":"主线=策略分析 · 面试考的是「拆问题」的顺序",
  "summary":"%s，主线已明确为策略分析——经营分析 / 商业化运营 / 渠道运营 / 数据运营。经营分析岗面试有稳定结构：给一个【某指标跌了】的现象，看候选人怎么拆。合格顺序是先对齐口径 → 再拆维度 → 再排假设 → 最后说怎么验证；直接跳到原因猜测是不合格。这个顺序本身就是能力证明。" % D,
  "action":"看求职","link":"#career","deepLink":"#career"},
 {"priority":7,"icon":"🎬","section":"影视",
  "headline":"颁奖季前哨 · 用「值不值得进影院」筛片",
  "summary":"%s，11-12 月是冲奥片集中上映窗口，特点是作者表达强、节奏偏慢。这个档期不适合用【好不好看】评价，适合用【值不值得在影院看】筛选：视听设计强的进影院，其余等流媒体。这个标准能砍掉大部分观影支出。" % D,
  "action":"看电影","link":"#movie","deepLink":"#movie"},
 {"priority":8,"icon":"🏠","section":"生活",
  "headline":"入冬先管湿度 · 目标 40-60%",
  "summary":"%s，北方供暖后室内湿度常低于 30%%，南方湿冷则相反。过低导致咽喉不适与静电，过高滋生霉菌。买一个温湿度计放卧室，低于 40%% 加湿、高于 60%% 通风。不要凭体感判断——人对湿度的感知很不准。" % D,
  "action":"看生活","link":"#life-tips","deepLink":"#life-tips"}
]}
a, b = find_decl(text, 'DAILY_BRIEFING'), None
i, j = brace_extent(text, a)
text = text[:i] + js(BRIEF) + text[j:]
print('✅ DAILY_BRIEFING：8 卡，date=%s' % TODAY)

# ============================================================
# 2) DAILY_VOCAB
# ============================================================
VOCAB = {"date": TODAY, "words": [
 {"emoji":"💰","category":"金融","word":"实际利率 (Real Interest Rate)",
  "definition":"名义利率减去通胀率。它才是「购买力有没有变多」的答案。",
  "example":"「活期 0.25%、通胀 3%，实际利率是 −2.75%，10 万放一年购买力亏约 2,750 元。」",
  "why_matters":"只看名义利率会得出相反结论。2% 的理财在 3% 通胀下是亏的——名义让你安心，实际才决定你变富还是变穷。"},
 {"emoji":"🤖","category":"AI","word":"静默失败 (Silent Failure)",
  "definition":"系统给出了格式正确但内容错误的结果，且没有任何报错。",
  "example":"「Agent 返回了一份结构完整的报告，但其中三处数字是编的，流程显示成功。」",
  "why_matters":"崩溃能被发现，静默失败会被当成正确答案使用。所以流程必须能输出证据、能说不知道——否则越顺滑越危险。"},
 {"emoji":"📊","category":"数据","word":"辛普森悖论 (Simpson's Paradox)",
  "definition":"分群看每一组都是 A 好于 B，合并后总体却是 B 好于 A。",
  "example":"「两个渠道分别看转化率都是新渠道更高，合并后旧渠道反而更高——因为两渠道的流量结构不同。」",
  "why_matters":"它提醒你：总体结论可能由构成变化造成。看到分群与总体方向相反，先查权重而不是怀疑数据。"},
 {"emoji":"💼","category":"职场","word":"口径对齐 (Metric Alignment)",
  "definition":"在讨论数字之前，先确认双方说的是不是同一个定义。",
  "example":"「运营说 GMV 1200 万、财务说收入 950 万——不是谁算错，是口径不同（退款/折扣/时间）。」",
  "why_matters":"大部分「数据对不上」不是错误，是口径差异。先对齐口径再谈结论，是经营分析的第一道门槛。"},
 {"emoji":"🔥","category":"健身","word":"食物热效应 (TEF)",
  "definition":"消化吸收食物本身消耗的能量，约占该食物热量的比例。",
  "example":"「蛋白的 TEF 约 20-30%，碳水 5-10%，脂肪更低。」",
  "why_matters":"同样热量下，蛋白占比高的餐净摄入更低、饱腹感更强。这是把蛋白提到 130-140g 的第二层理由。"},
 {"emoji":"📝","category":"法律","word":"定金 vs 订金",
  "definition":"定金有担保效力（违约方不得要求返还）；订金只是预付款，可要求返还。",
  "example":"「合同写【定金】而你违约，钱要不回；写【订金】通常可以退。」",
  "why_matters":"一个字之差决定几千元能不能退。签字前只看这两个字，比看整份合同的其他条款更划算。"},
 {"emoji":"⏳","category":"医学","word":"半衰期 (Half-life)",
  "definition":"体内物质浓度下降一半所需的时间。",
  "example":"「咖啡因半衰期约 5 小时，睡前 10 小时喝的那杯，到睡前仍剩约 1/4。」",
  "why_matters":"它把【多久能代谢掉】变成可计算的数。影响睡眠的不只是喝没喝，还有什么时候喝。"},
 {"emoji":"🧠","category":"心理","word":"确认偏误 (Confirmation Bias)",
  "definition":"倾向于寻找、相信支持自己已有观点的信息，忽略相反证据。",
  "example":"「看好某只股票后，只点开利好的分析，看到利空就归因为【噪音】。」",
  "why_matters":"它让判断越来越自信但越来越不准。破解方法是主动写下【最强反方论证】——写不出说明还没懂。"},
 {"emoji":"📉","category":"商业","word":"边际收益递减 (Diminishing Returns)",
  "definition":"在其他条件不变时，持续增加某一投入，每一单位新增投入带来的新增产出会下降。",
  "example":"「某渠道 ROI 最高，但预算翻倍后 ROI 明显下滑——因为最优质的那批用户已经被买完了。」",
  "why_matters":"它解释了为什么【表现最好的渠道】不该拿走全部预算。分配看边际，不看平均值。"},
 {"emoji":"🪜","category":"学习","word":"提示阶梯 (Hint Ladder)",
  "definition":"把提示分成多级，第一级指方向、第二级给关键事实、最后才给答案。",
  "example":"「卡住时先看【想想分母是什么】，还是不会再要【分母此时处于历史什么位置】。」",
  "why_matters":"用提示不算失败，但也不算独立完成。这个区分防止把【读过】误当成【会做】。"}
]}
a = find_decl(text, 'DAILY_VOCAB')
i, j = brace_extent(text, a)
text = text[:i] + js(VOCAB) + text[j:]
cats = [w['category'] for w in VOCAB['words']]
print('✅ DAILY_VOCAB：%d 词 / %d 个不同领域（%s）' % (len(VOCAB['words']), len(set(cats)), '、'.join(sorted(set(cats)))))

# ============================================================
# 3) LEARN_PATHS：归档旧条 → 换新条 → current_day +1
# ============================================================
lp_start = find_decl(text, 'LEARN_PATHS')
old_items_s, old_items_e = get_array_block(text, 'items', lp_start)
old_items_js = text[old_items_s:old_items_e]
print('   旧课堂条目数组长度：%d 字符' % len(old_items_js))

NEW_ITEMS = [
 {"section":"AI","emoji":"🤖","title":"静默失败：为什么「流程跑成功了」不等于结果对？",
  "content":"AI 流程最危险的失败不是崩溃，而是格式正确但内容错误且不报错。崩溃你能发现，静默失败会被当成正确答案直接使用。对应的工程做法是两条：强制输出证据（每条结论要能指回原文）、必须能说不知道（找不到依据就明说）。做不到这两点的流程，不该接入任何决策链。",
  "takeaway":"评价一个 AI 流程，先问「它出错时我会不会发现」。答不出来说明这个流程还不该用。"},
 {"section":"金融","emoji":"💰","title":"实际利率：为什么「2% 的理财」可能是亏的？",
  "content":"判断一笔钱赚没赚，看的不是名义利率而是实际利率 = 名义利率 − 通胀率。通胀 3% 时，活期 0.25% 的实际利率是 −2.75%，2% 的理财是 −1%。账上钱变多了，能买的东西却变少了。换成金额更直观：10 万 × (−1%) = 亏 1,000 元购买力。",
  "takeaway":"看到任何收益率，先减掉通胀再判断。不减就是拿名义当实际。"},
 {"section":"数据","emoji":"📊","title":"辛普森悖论：分群都优、合并却劣，该信哪个？",
  "content":"当分群与总体结论方向相反时，通常不是数据错，而是【构成变化】在起作用——某个群体在总体里占比变了，把总体的加权结果拉向另一边。正确做法不是选一个信，而是把权重摊开：每一组的人数、转化率、占比都列出来，看清是【组内差异】还是【结构差异】。",
  "takeaway":"看到分群与总体矛盾，先查权重构成，别急着怀疑数据。"},
 {"section":"求职","emoji":"💼","title":"口径对齐：为什么两个报表能差 30%？",
  "content":"经营分析面试的高频题：运营报 GMV 1200 万、财务报收入 950 万，问你怎么处理。合格回答的顺序是——先确认差额总量，再列【可能的差异来源清单】（时间口径 / 退款 / 折扣补贴 / 运费代收），逐项量化，加总看能不能解释掉。能解释 90% 以上才算定位成功；差的那部分恰恰是风险。",
  "takeaway":"面试里能按这个顺序讲，比说【最后查出来是退款】有说服力得多。"},
 {"section":"健身","emoji":"💪","title":"冬季训练的变量是热身时长，不是重量",
  "content":"气温下降后肌肉粘滞性增加，同样强度的动作需要更长时间进入状态。经验口径：热身从 8 分钟延长到 12 分钟，第一个正式组降 10% 重量做过渡组。另一个被忽略的变量是补水——冬季口渴感减弱，但出汗量并未显著下降。",
  "takeaway":"入冬先把热身和过渡组加上，再谈要不要冲重量。"},
 {"section":"法律","emoji":"📝","title":"定金与订金：一个字决定几千元能不能退",
  "content":"定金有担保效力：给付方违约不得要求返还，收受方违约要双倍返还。订金只是预付款，通常可以要求返还。签任何预付款合同（租房、买车、装修）前，只看这两个字，比通读其他条款更划算。",
  "takeaway":"签合同先搜【定金】两个字。有它就当钱已经花掉了。"},
 {"section":"心理","emoji":"🧠","title":"确认偏误：为什么看了很多资料反而更确信错的？",
  "content":"人倾向于寻找并相信支持自己观点的信息，忽略相反证据。这导致一个反直觉结果：信息越多，判断可能越偏，因为你只吸收了同侧的那部分。破解方法很具体——每形成一个判断，必须写下【最强的反对论证】。写不出来，说明还没真正理解，只是找到了同盟。",
  "takeaway":"判断的质量不看支持证据有多少，看你能不能说出反方最强的那一句。"},
 {"section":"商业","emoji":"📉","title":"边际收益递减：为什么 ROI 最高的渠道不该拿走全部预算？",
  "content":"某渠道 ROI 最高，往往是因为它只吃到了最优质的那批用户。预算翻倍后，新增的那部分用户质量下降，边际 ROI 会明显下滑。所以预算分配看的是【边际】而不是【平均】——最后一个单位的投入能带来多少回报，才决定该不该继续加。",
  "takeaway":"问【再加 10 万会怎样】，而不是【过去 10 万回报多少】。"},
 {"section":"生活","emoji":"🏠","title":"入冬先管湿度：40-60% 这个区间为什么重要",
  "content":"北方供暖后室内湿度常低于 30%，导致咽喉不适、皮肤干、静电；南方湿冷时湿度高于 70%，容易滋生霉菌。目标区间 40-60%。人对湿度的感知很不准，必须用温湿度计，不能凭体感。",
  "takeaway":"花几十元买个温湿度计，比反复调整空调温度有效。"},
 {"section":"影视","emoji":"🎬","title":"用「值不值得进影院」筛片，而不是「好不好看」",
  "content":"颁奖季的片子特点是作者表达强、节奏偏慢，用【好不好看】评价容易误判。换成【值不值得在影院看】：只有三类值得——视听设计是核心卖点、有剧透风险、需要大银幕沉浸。这个标准能砍掉大部分观影支出，也不会错过真正该在大银幕看的东西。",
  "takeaway":"把标准换成【必须在大银幕】，选择立刻变清晰。"}
]

# 归档旧条：往 archive 里插入 OLD_ARCHIVE_KEY
arc_s, arc_e = get_block(text, 'archive', lp_start)
if arc_s is None:
    print('❌ 找不到 archive')
    sys.exit(1)
arc_body = text[arc_s:arc_e]
if ('"' + OLD_ARCHIVE_KEY + '"') in arc_body or ("'" + OLD_ARCHIVE_KEY + "'") in arc_body:
    print('ℹ️  archive 已含 %s，跳过归档' % OLD_ARCHIVE_KEY)
else:
    ins = arc_s + 1  # 在 { 之后插入
    text = text[:ins] + '\n    "' + OLD_ARCHIVE_KEY + '": ' + old_items_js + ',' + text[ins:]
    print('✅ 旧课堂条目已归档到 archive["%s"]' % OLD_ARCHIVE_KEY)

# 替换 items
lp_start = find_decl(text, 'LEARN_PATHS')
i, j = get_array_block(text, 'items', lp_start)
text = text[:i] + js(NEW_ITEMS) + text[j:]
print('✅ LEARN_PATHS.items：%d 条 / %d 个领域' % (len(NEW_ITEMS), len(set(x['section'] for x in NEW_ITEMS))))

# current_day +1
m = re.search(r'current_day\s*:\s*(\d+)', text)
if m:
    oldd = int(m.group(1))
    text = text[:m.start(1)] + str(oldd + 1) + text[m.end(1):]
    print('✅ current_day：%d → %d' % (oldd, oldd + 1))

# ============================================================
# 4) DAILY_DECISIONS
# ============================================================
DEC = {"updated": TODAY, "items": [
 {"icon":"📈","action":"三季报空窗期：把自选股按「已披露 / 未披露」分类",
  "why":"空窗期没有财报催化，未披露的公司一旦暴雷没有缓冲",
  "how":"列出自选股，只留已披露三季报的进观察池；未披露的单列一份，等披露后再说。空窗期的题材首日涨停不追","priority":"P0"},
 {"icon":"💼","action":"准备一个 3 分钟的「口径对齐」故事",
  "why":"这是经营分析面试命中率最高的故事类型，比讲结论更证明能力",
  "how":"按【发现两个数对不上 → 列差异来源清单 → 逐项量化 → 加总解释掉 90% 以上】四步讲，中间不要跳到原因","priority":"P0"},
 {"icon":"🎓","action":"学金融课第 2 单元（货币、利率、通胀），排 3 天后复测",
  "why":"实际利率是后面所有理财判断的基准，先把这个基准建起来",
  "how":"打开训练场 → 学习学院 → 金融 → 第 2 单元。学完点【安排 3 天后复测】，不要当天复述","priority":"P1"},
 {"icon":"🤖","action":"检查自己在用的一个 AI 流程，回答三个问题",
  "why":"静默失败比崩溃危险，但大多数流程从没被问过这件事",
  "how":"问：① 它出错时我会不会发现 ② 成本上限是多少 ③ 有没有必须人工确认的节点。三问都答不出的先别用在正式产出上","priority":"P1"},
 {"icon":"🏠","action":"买一个温湿度计放卧室",
  "why":"入冬后湿度对睡眠与咽喉的影响大于温度，而人对湿度感知很不准",
  "how":"几十元的即可。低于 40% 加湿、高于 60% 通风，记录一周看规律","priority":"P2"}
]}
a = find_decl(text, 'DAILY_DECISIONS')
i, j = brace_extent(text, a)
text = text[:i] + js(DEC) + text[j:]
print('✅ DAILY_DECISIONS：%d 条，updated=%s' % (len(DEC['items']), TODAY))

# ============================================================
# 5) DAILY_DATA.update_date
# ============================================================
a = find_decl(text, 'DAILY_DATA')
if a:
    i, j = brace_extent(text, a)
    blk = text[i:j]
    blk2 = re.sub(r'(update_date\s*:\s*)(["\'])([^"\']*)\2', lambda m: m.group(1) + '"2026年11月6日"', blk, count=1)
    text = text[:i] + blk2 + text[j:]
    print('✅ DAILY_DATA.update_date → 2026年11月6日')

# ============================================================
# 6) 同步 updated 字段（只动 updated）
# ============================================================
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-\d\d-\d\d)\2')
text, n = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), text)
print('✅ updated 字段同步：%d 处 → %s' % (n, TODAY))

# ============================================================
# 7) 升版本
# ============================================================
text, nv = re.subn(r'(var\s+SITE_VERSION\s*=\s*["\'])' + re.escape(OLD_VER) + r'(["\'])', r'\g<1>' + NEW_VER + r'\g<2>', text)
print('✅ SITE_VERSION → %s（%d 处）' % (NEW_VER, nv))

open('daily_data.js', 'w', encoding='utf-8').write(text)
print('\n文件：%d → %d 字节' % (orig, len(text)))
