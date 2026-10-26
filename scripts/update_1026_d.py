# -*- coding: utf-8 -*-
"""2026-10-26（周一）更新 · 当日四件套 + 归档 + 日期同步 + 升版本

四件套：
  DAILY_DATA      update_date / update_time
  DAILY_BRIEFING  8 张卡 + date
  DAILY_VOCAB     10 词 / 10 领域 + date
  LEARN_PATHS     10 条新条目，current_day 27→28，旧条目归档到 2026-10-25
  DAILY_DECISIONS 5 条 + updated
日期同步：全部 updated 字段 → 2026-10-26（archive 的键绝不动）
升版本：SITE_VERSION 1.8.40 → 1.8.41
"""
import io, sys, os, re, json, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
TODAY = '2026-10-26'
TODAY_CN = '2026年10月26日'

src = open(DP, encoding='utf-8').read()

# ---------------- 通用：替换某个 `key: [ ... ]` 数组 ----------------
def replace_array(s, key, new_items, search_from=0):
    m = re.compile(r'(["\']?' + key + r'["\']?\s*:\s*)\[').search(s, search_from)
    if not m:
        raise SystemExit('❌ 找不到数组 %s' % key)
    open_br = m.end() - 1
    # 括号配对（跳过字符串）
    depth = 0; i = open_br; in_str = None
    while i < len(s):
        c = s[i]
        if in_str:
            if c == '\\':
                i += 2; continue
            if c == in_str: in_str = None
            i += 1; continue
        if c in '"\'':
            in_str = c; i += 1; continue
        if c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                close_br = i
                body = json.dumps(new_items, ensure_ascii=False, indent=2)
                body = '\n' + '\n'.join('  ' + ln for ln in body.split('\n')) + '\n'
                return s[:m.start(1)] + m.group(1) + '[' + body + ']' + s[close_br + 1:]
        i += 1
    raise SystemExit('❌ 数组 %s 没有闭合' % key)

# ---------------- 通用：替换标量字段 ----------------
def replace_scalar(s, key, value, search_from=0):
    m = re.compile(r'(["\']?' + re.escape(key) + r'["\']?\s*:\s*)(["\'])([^"\']*)\2').search(s, search_from)
    if not m:
        raise SystemExit('❌ 找不到字段 %s' % key)
    q = m.group(2)
    return s[:m.start(1)] + m.group(1) + q + str(value) + q + s[m.end():]

# ==================== 1) 归档旧 items（新增键 2026-10-25） ====================
probe = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),c);
console.log(JSON.stringify({items:c.LEARN_PATHS.items, day:c.LEARN_PATHS.current_day,
  archKeys:Object.keys(c.LEARN_PATHS.archive)}));
'''
pp = os.path.join(P, '_p1.js'); open(pp, 'w', encoding='utf-8').write(probe)
r = subprocess.run(['node', pp, DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
os.remove(pp)
cur = json.loads(r.stdout)
old_items = cur['items']
old_day = cur['day']
print('旧 items: %d 条（day%d）· archive 现有 %d 组' % (len(old_items), old_day, len(cur['archKeys'])))

# 在 archive 的 `{` 后插入新键
ARCH_KEY = '2026-10-25'
if ARCH_KEY in cur['archKeys']:
    print('⚠️ archive 已有 %s，跳过归档' % ARCH_KEY)
else:
    m = re.search(r'archive\s*:\s*\{', src)
    if not m:
        raise SystemExit('❌ 找不到 archive')
    entry = '\n    "%s": %s,' % (ARCH_KEY, json.dumps(old_items, ensure_ascii=False, indent=4).replace('\n', '\n    '))
    src = src[:m.end()] + entry + src[m.end():]
    print('✅ 已归档旧 items → archive["%s"]' % ARCH_KEY)

# ==================== 2) 新 items（10 条 / 10 领域） ====================
NEW_ITEMS = [
{"section":"AI","emoji":"🤖","title":"能力边界：为什么「说清我不知道」比答得好更重要？",
 "content":"REA 这类工具在设计上有一个共同点：要求输出必须含【证据】与【未知项】。这不是保守，而是让使用者能判断哪部分可以信。反过来说，一个从不说「我不确定」的系统，你无法区分它的准确回答和编造的答案，于是整体可信度下降。",
 "takeaway":"评价 AI 产品时先看它敢不敢说不知道。不敢说的，其他指标都要打折看。"},
{"section":"技术","emoji":"🔧","title":"幂等：为什么「重复点击不会出两次错」是一种能力？",
 "content":"幂等指同一个操作执行一次和执行多次，结果相同。赞一次和赞三次都只算一赞；提交一次和提交三次都只生成一条记录。实现方式通常是给每次操作一个唯一标识，服务端记住已处理过的标识。反例是「点两次提交生成两个订单」——这在支付场景是灾难。",
 "takeaway":"凡是「可能被重复触发」的动作，都要先问它幂等吗。没有幂等的地方就是事故点。"},
{"section":"运营","emoji":"🎯","title":"反馈率：为什么它能分开「材料问题」和「面试问题」？",
 "content":"反馈率 =（约面 + 明确拒绝）÷ 已投递。它的价值在于：低于 10% 说明简历或方向有问题（连门都进不去），而反馈率正常但面试通过率低，说明问题在面试环节。两个问题需要的动作完全不同——改材料 vs 练面试。不统计反馈率，就只能在两者之间瞎猜。",
 "takeaway":"先算反馈率再决定改什么。没有这个数，所有「帮我看看简历」都是盲改。"},
{"section":"健身","emoji":"💪","title":"渐进超负荷：为什么「一直做同样重量」不会继续长？",
 "content":"肌肉增长依赖超过当前适应水平的刺激。如果一直用同样的重量、同样的次数，身体适应后就不再变化。渐进超负荷不是每次都加重量，可以是加次数、加组数、缩短组间休息、或提高动作质量。对偏瘦体型，最安全的加量方式是「先把次数做满，再考虑负重」。",
 "takeaway":"每周至少有一个变量比上周高（重量/次数/组数）。一个都没变，这周就只是维持。"},
{"section":"财经","emoji":"📈","title":"量价背离：为什么「价格不动但成交量萎缩」是信号？",
 "content":"成交量代表分歧与参与度。价格上涨但成交量持续萎缩，说明追高的资金在减少；价格不动但成交量明显萎缩，说明愿意在这个价位交易的人变少了。后者常见于业主不愿降价、买家不愿接盘的对峙期——通常会先出现撤牌或议价空间扩大，价格随后才动。",
 "takeaway":"判断价格会往哪走，先看量。量先变，价后变，这个顺序很少反。"},
{"section":"求职","emoji":"🎯","title":"基线测评：为什么「感觉进步了」不能当证据？",
 "content":"基线测评是先做一次难度固定的测试，记录当时的水平；过一段时间用同难度但没见过的题再测一次。两次的差值才是真实进步。没有基线，「感觉进步了」可能只是因为题目变简单了、或你熟悉了题型。技能训练里最容易被自评骗过。",
 "takeaway":"开始练之前先测一次。没有基线的进步，都是自我感觉。"},
{"section":"理财","emoji":"💰","title":"沉没成本：为什么「已经投入这么多」不该影响下一步？",
 "content":"沉没成本是已经付出且无法收回的投入（时间、钱、精力）。理性决策只看【未来】的收益与成本，不看过去投入多少。但人对沉没成本异常敏感：看了一半的烂片舍不得关、学了两个月不想放弃的方向硬撑。判断标准是：如果今天从零开始，我还会选它吗？",
 "takeaway":"问「如果今天重新选，我还会选它吗」。答案是不会的时候，之前的投入就是应该止损的。"},
{"section":"学习","emoji":"📚","title":"闭卷复述：为什么「读的时候懂了」不等于学会？",
 "content":"读的时候大脑在做【识别】——看到文字觉得熟悉，就以为懂了。真正掌握需要【提取】——在不看材料的情况下自己说出来。识别很容易，提取很难，两者的差距就是真实掌握程度。判断方法：合上材料，用自己的话讲 90 秒；讲不出来的部分就是没学会的部分。",
 "takeaway":"学完立刻闭卷复述。讲得卡住的地方，才是真正需要再看的地方。"},
{"section":"生活","emoji":"🌡️","title":"洋葱式穿衣：为什么「穿一件厚的」反而更容易感冒？",
 "content":"温差大的季节，穿一件厚衣服的问题在于中午脱不掉：热了出不了汗，出汗后遇到降温或空调，反而更容易受凉。洋葱式是多层薄衣可随时增减，核心是让身体始终处在不出汗也不发冷的状态。判断标准是「能不能在 10 秒内调整一层的厚薄」。",
 "takeaway":"温差超过 6C 的日子，穿多层可脱的，别穿一件厚的。感冒多半来自出汗后受凉。"},
{"section":"产品","emoji":"🧭","title":"反逃避设计：为什么「让人看到自己在逃避什么」是一种产品能力？",
 "content":"舒适的工具会被用来替代痛苦但重要的事。比如把训练做得很好玩，用户可能每天训练却不投简历——训练成了焦虑的出口。反逃避设计是主动把「真实进展」摆在显眼位置，让工具无法帮助用户自我安慰。做法通常是把两类指标并排显示，而不是只展示好看的那个。",
 "takeaway":"如果一个工具让你感觉良好但没推进真实目标，它可能在帮你逃避。看它敢不敢显示难看的数。"},
]

src = replace_array(src, 'items', NEW_ITEMS, src.index('var LEARN_PATHS'))
print('✅ LEARN_PATHS.items 已换成 %d 条' % len(NEW_ITEMS))

# current_day 27 → 28
src = re.sub(r'(current_day\s*:\s*)27', r'\g<1>28', src, count=1)
print('✅ current_day 27 → 28')

# ==================== 3) DAILY_DATA ====================
now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
src = replace_scalar(src, 'update_date', TODAY_CN, src.index('var DAILY_DATA'))
src = replace_scalar(src, 'update_time', now, src.index('var DAILY_DATA'))
print('✅ DAILY_DATA: %s / %s' % (TODAY_CN, now))

# ==================== 4) DAILY_BRIEFING 8 卡 ====================
NEW_CARDS = [
{"priority":1,"icon":"📈","section":"A股复盘",
 "headline":"10 月最后一个完整交易周：三季报 10/31 截止，本周必须交实数",
 "summary":"本周（10/26-10/30）是 10 月唯一的完整交易周，也是<b>三季报披露的最后 5 个交易日</b>（10/31 截止）。两件事撞在一起：① 业绩地雷与超预期同时释放 ② 月末资金面偏紧、机构调仓在最后一周完成。<b>本周的量能与结构比月中更有说明力</b>：量能站上 2.2 万亿且连续 3 天，才算脱离存量博弈；三季报看「反应」不看「数字」——超预期不涨说明预期已兑现，业绩一般但抗跌说明筹码结构好。",
 "action":"看复盘","link":"#stock","deepLink":"#stock"},
{"priority":2,"icon":"🎮","section":"游戏",
 "headline":"影之刃零倒计时 3 天（10/29 发售）· 先清愿望单再谈买不买",
 "summary":"影之刃零 <b>10/29 发售</b>（预售 268 元起），距今 3 天。这是国产 3A 商业化的关键验证，意义超出游戏本身。<b>这周正确动作是先清愿望单</b>——秋促临近，愿望单里「加了但已经不想买」的会诱发冲动消费。<b>影之刃零先别预购</b>：3A 预购踩雷成本高，等首周实机评测（战斗手感/帧数/流程长度三项）。判断标准只有一个：<b>我会不会玩到通关</b>。",
 "action":"看游戏区","link":"#gaming","deepLink":"#gaming"},
{"priority":3,"icon":"💪","section":"健身",
 "headline":"改版第 9 天 · 第一周收尾，只问三个问题",
 "summary":"10/20 定的「只做三件事」到今天满一周，体脂 12-14%、体重 60.65kg 没变——<b>一周体重不变是正常的</b>，增肌真实反馈要 3-4 周。<b>第一周只看：拉类做了几次</b>（目标周一/周五各一次）。做到 2 次 → 计划成立；0 次 → 不是意志力问题，是动作或时机有障碍，要换动作。明天进第二周，<b>先别加新动作</b>。",
 "action":"看健身区","link":"#fitness","deepLink":"#fitness"},
{"priority":4,"icon":"🎯","section":"求职",
 "headline":"秋招 10 月最后一周：先盘点截止日期，再统计反馈率",
 "summary":"10 月只剩 5 天，<b>很多公司网申在 10/31 前后关闭</b>。顺序不能反：<b>先花 30 分钟把所有在看的机会的截止日期列成表</b>，按「截止近 + 匹配高」排，不按名气排。不列就投，容易在 11/1 发现最想去的那家已经关了。然后统计反馈率：<b>低于 10% → 改材料，不要继续投</b>。截止周 HR 筛得更快，<b>简历第一屏（定位句 + 一个数字）比后面所有内容都重要</b>。",
 "action":"看求职中心","link":"#career","deepLink":"#career"},
{"priority":5,"icon":"🤖","section":"AI 动态",
 "headline":"REA 真正的价值不是功能，是「MCP / Skill / CLI」三层分工",
 "summary":"REA（Reverse Engineer Anything，<code>morluto/rea</code>）GitHub 周榜第一，总星 29.1 万、周增 24.9 万。它要求输出必须含<b>证据与未知项</b>。但对 AI 产品岗，最值钱的是它的三层职责划分：<b>MCP = 能力边界 / Skill = 流程固化 / CLI = 给人用的入口</b>。三层混淆时最常见的错误，是把「该由人判断的」也塞进 MCP。<b>这是面试高频设计题，也是最容易一句话说清结构的答案。</b>",
 "action":"看 AI 追踪","link":"#ai-track","deepLink":"#ai-track"},
{"priority":6,"icon":"📚","section":"学习",
 "headline":"10 月只剩 5 天：收尾而不是扩张，先做一次月末清账",
 "summary":"本月已过 26 天，<b>现在加载新任务的边际收益极低</b>——开了头也做不完，还挤占收尾时间。正确做法是把「未完成的」收敛成两种：<b>5 天内能做完的排进这周；做不完的明确推到 11 月并写一句为什么</b>。最怕第三种状态：挂着、天天想着、但不动。顺便算一次真实完成率——<b>低于 50% 通常不是懒，是月初标准超出实际可投入时间</b>。",
 "action":"看学习区","link":"#learning","deepLink":"#learning"},
{"priority":7,"icon":"🏠","section":"楼市",
 "headline":"10 月最后一周：建立你自己的基线，本月不做决策",
 "summary":"广州核心区相对坚挺（天河约 5.3 万/㎡、越秀约 4.9 万/㎡），外围分化明显。本月成交数据会在 11 月初出来，<b>那个数字比现在任何报价都重要</b>。所以这周的动作是<b>记录而不是决策</b>：挑 3 个真正会考虑的小区，记下当前挂牌价与带看量，11 月才有对照。<b>没有基线，看到「降价」也分不清是真降还是回到原位。</b>",
 "action":"看购房租房","link":"#house","deepLink":"#house"},
{"priority":8,"icon":"🎬","section":"电影",
 "headline":"全年观影体验最好的窗口之一：排片宽松、票价回落",
 "summary":"国庆档已结束近三周，档期热度完全退去，现在到 11 月初<b>排片宽松、票价回落 20-30%、场次好挑</b>。这周两件事：① <b>补片只挑「需要大银幕」的</b>——视觉/音效驱动的去影院，剧情片在家看流媒体省两小时通勤 ② <b>看一眼 11 月定档</b>——定档提前 2-3 周出，11 月是进口大片与颁奖季集中期。<b>不着急的片等第二周，票价更低体验几乎无差别。</b>",
 "action":"看影视区","link":"#movie","deepLink":"#movie"},
]
src = replace_array(src, 'highlights', NEW_CARDS, src.index('var DAILY_BRIEFING'))
src = replace_scalar(src, 'date', TODAY, src.index('var DAILY_BRIEFING'))
print('✅ DAILY_BRIEFING: 8 卡 + date=%s' % TODAY)

# ==================== 5) DAILY_VOCAB 10 词 / 10 领域 ====================
NEW_WORDS = [
{"emoji":"🤖","category":"AI","word":"能力边界 (Capability Boundary)","definition":"系统明确声明自己能做什么、不能做什么，而不是对所有问题都给答案。","example":"「我只能查这份文档里的内容，问到其他主题我会说找不到。」","why_matters":"可信度来自边界。一个从不说「不知道」的系统，你无法区分准确和编造，整体可信度就下降了。"},
{"emoji":"🔧","category":"技术","word":"幂等 (Idempotency)","definition":"同一操作执行一次和执行多次，结果完全相同。","example":"点一次提交和点三次提交，都只生成一条记录。","why_matters":"凡是可能被重复触发的动作（提交、支付、导入）都要先问幂等吗。没有幂等的地方就是事故点。"},
{"emoji":"🎯","category":"运营","word":"反馈率 (Response Rate)","definition":"（约面 + 明确拒绝）÷ 已投递，衡量投出去的东西有没有被看见。","example":"投 30 家，3 家约面、2 家拒，反馈率 = 5÷30 ≈ 17%。","why_matters":"它能把「材料问题」和「面试问题」分开。低于 10% 改材料，反馈正常但面试通过率低就练面试——动作完全不同。"},
{"emoji":"💪","category":"健身","word":"渐进超负荷 (Progressive Overload)","definition":"逐渐增加训练刺激（重量/次数/组数），让身体持续面对超过当前适应水平的负荷。","example":"上周 4 组 × 8 次，这周做 4 组 × 10 次，就是一次超负荷。","why_matters":"一直做同样重量身体适应后就不再变化。每周至少一个变量要比上周高，否则只是维持。"},
{"emoji":"📈","category":"财经","word":"量价背离 (Volume-Price Divergence)","definition":"价格与成交量的变化方向或强度不一致，常被用作趋势转折的早期信号。","example":"价格还在涨，但成交量连续萎缩，说明追高资金在减少。","why_matters":"量代表分歧与参与度。判断价格往哪走先看量——量先变，价后变，这个顺序很少反。"},
{"emoji":"🎯","category":"求职","word":"基线测评 (Baseline Assessment)","definition":"训练开始前做一次难度固定的测试，记录当时水平，用于日后对比。","example":"练 SQL 前先做 10 道固定题，记录正确率；三周后用同难度新题再测。","why_matters":"没有基线，「感觉进步了」可能只是题目变简单或熟悉了题型。技能训练里最容易被自评骗过。"},
{"emoji":"💰","category":"理财","word":"沉没成本 (Sunk Cost)","definition":"已经付出且无法收回的投入，理性决策不应受它影响。","example":"看了一半的烂片舍不得关；学了两个月不想放弃的方向硬撑。","why_matters":"只看未来的收益与成本。问「如果今天从零开始，我还会选它吗」——答案是不会时，之前投入的就是该止损的。"},
{"emoji":"📚","category":"学习","word":"闭卷复述 (Closed-book Recall)","definition":"合上材料，用自己的话把内容讲出来，用来检验是否真正掌握。","example":"读完一节立刻合上，试着讲 90 秒；讲不出的地方就是要重看的地方。","why_matters":"读的时候大脑在做「识别」（觉得熟悉），真掌握需要「提取」（自己说出来）。两者的差距就是真实水平。"},
{"emoji":"🌡️","category":"生活","word":"洋葱式穿衣 (Layering)","definition":"用多层薄衣替代一件厚衣，随时增减来适应温差。","example":"短袖 + 衬衫 + 薄外套，中午脱外套、傍晚加回来。","why_matters":"一件厚衣的问题是中午脱不掉，出汗后遇降温更容易受凉。感冒多半来自出汗后受凉，不是天冷本身。"},
{"emoji":"🧭","category":"产品","word":"反逃避设计 (Anti-avoidance Design)","definition":"主动把「真实进展」摆在显眼位置，让工具无法帮助用户自我安慰。","example":"训练面板旁边并排显示「本周投递 0 家」，而不是只展示训练分数。","why_matters":"舒适的工具会被用来替代痛苦但重要的事。如果一个工具让你感觉良好却没推进真实目标，它可能在帮你逃避。"},
]
src = replace_array(src, 'words', NEW_WORDS, src.index('var DAILY_VOCAB'))
src = replace_scalar(src, 'date', TODAY, src.index('var DAILY_VOCAB'))
print('✅ DAILY_VOCAB: 10 词 / 10 领域 + date=%s' % TODAY)

# ==================== 6) DAILY_DECISIONS 5 条 ====================
NEW_DEC = [
{"icon":"📈","action":"三季报最后 5 个交易日：只看「反应」，不做预测","why":"数字本身已被预期消化，股价的反应方式才携带信息","how":"盯两类：① 业绩超预期但股价不涨（预期已兑现）② 业绩一般但抗跌（筹码结构好）。10/30 收盘后写一句结论，不再重判","priority":"P0"},
{"icon":"🎯","action":"把目标公司的网申截止日期列成一张表（30 分钟）","why":"10/31 前后是密集截止点，不列就会在 11/1 发现最想去的已经关了","how":"字节/腾讯/美团/小红书/微众/SHEIN/滴滴逐个查，按「截止近 + 匹配高」排序，不按名气","priority":"P0"},
{"icon":"📚","action":"10 月月末清账：未完成的事收敛成两类","why":"只剩 5 天，加载新任务的边际收益极低，挂着不动是最大消耗","how":"5 天内能做完的排进本周；做不完的明确推到 11 月并写一句为什么。然后算一次真实完成率","priority":"P0"},
{"icon":"💪","action":"第一周复盘只问三个问题，明天进第二周不加新动作","why":"第一周要看的是「有没有做」而不是「做得好不好」；没稳定就加动作只会更乱","how":"拉类做了几次（目标 2 次）/ 每次是否做到 8-12 次 / 有没有痛。0 次就换动作而不是加意志力","priority":"P1"},
{"icon":"🎮","action":"清 Steam 愿望单，影之刃零先别预购","why":"秋促临近，愿望单里「不想买但留着」的会诱发冲动消费；3A 预购踩雷成本高","how":"移出已不想买的；真正想要的 3-5 款标上心理价位；影之刃零等 10/29 后首周实机评测","priority":"P1"},
]
src = replace_array(src, 'items', NEW_DEC, src.index('var DAILY_DECISIONS'))
print('✅ DAILY_DECISIONS: 5 条')

# ==================== 7) 日期同步：全部 updated 字段 ====================
pat = re.compile(r'(updated\s*:\s*)(["\'])(2026-\d\d-\d\d)\2')
src, n_upd = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), src)
print('✅ 日期同步：%d 个 updated 字段 → %s' % (n_upd, TODAY))

# 确认 archive 键没被改
arch_after = re.findall(r'"(2026-\d\d-\d\d)"\s*:\s*\[', src)
print('   archive 键数量: %d（应 ≥17，且含 2026-10-25）' % len(arch_after))

# ==================== 8) 升版本 ====================
src = re.sub(r'var SITE_VERSION = "1\.8\.40";', 'var SITE_VERSION = "1.8.41";', src, count=1)
src = src.replace('版本1.8.40', '版本1.8.41')
open(DP, 'w', encoding='utf-8').write(src)
print('✅ SITE_VERSION → 1.8.41')

# ==================== 9) 语法与回读 ====================
r = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('   语法：' + ('OK' if r.returncode == 0 else 'FAIL\n' + (r.stderr or '')[:500]))
