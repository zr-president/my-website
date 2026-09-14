# -*- coding: utf-8 -*-
"""个人网站 2026-09-13 内容更新：围绕健身方案「减脂→增肌」的调整"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()


def j(o, ind=2):
    """JSON → 带缩进的 JS 字面量"""
    s = json.dumps(o, ensure_ascii=False, indent=ind)
    return s.replace('\n', '\n' + ' ' * ind)


# ==================== 1) DAILY_BRIEFING ====================
highlights = [
 {"priority":1,"icon":"💪","section":"健身方案调整","headline":"健身区大改：从「减脂露腹肌」转向「增肌 + 腹肌 双目标」（新增练腿·跳绳减量·热量转盈余）","summary":"你提出既要腹肌又要增肌——这两件事对 170cm/59kg、体脂 15-18% 的【瘦胖子】来说其实是同一件事：体脂率偏高不是因为脂肪多，而是肌肉太少。继续按减脂思路练会掉到 55kg、看起来更瘦弱，腹肌照样不明显。新方案三处改动：①新增下肢训练（原来完全没有，腿占全身肌肉一半以上）②跳绳从 3-4 次减到 1-2 次（过量有氧抢走增肌的热量与恢复）③热量从轻缺口改为轻微盈余（训练日 +200 kcal）。12 周目标：62-63kg、体脂 13-14%、腹肌清晰。","action":"查看新计划","link":"#fitness","deepLink":"#fitness"},
 {"priority":2,"icon":"🍽️","section":"饮食调整","headline":"饮食同步改为增肌版：训练日 2500 / 休息日 2300 kcal，蛋白维持 110-130g","summary":"原方案是【轻缺口 2300 kcal】——那是减脂思路，59kg 的人靠缺口长不出肌肉。新方案：训练日 2500 kcal（+200 盈余）、休息日 2300 kcal（维持），蛋白保持 110-130g（1.9-2.2g/kg），碳水训练日 50-55%、脂肪 25-30%。原饮食页写的 2600-2800 kcal 与健身页的 2300-2500 互相矛盾，本次一并统一。肾结石预防照旧：饮水 ≥2.5L、控草酸、限盐。","action":"看饮食方案","link":"#diet","deepLink":"#diet"},
 {"priority":3,"icon":"📈","section":"训练方法论","headline":"渐进超负荷：你标准俯卧撑能一口气做 60 个，说明自重已经完全适应——必须加负重才能长肌肉","summary":"这是本次调整里最容易被忽略的一点。同一个动作做久了身体会适应，此后再做只提升耐力、不增加肌肉。所以：俯卧撑改为背包负重（每 2 周加 2-3kg）并练到每组最后 2-3 次很吃力；深蹲/分腿蹲/臀桥从自重起步再加重；腹肌从高次数平板改为负重与动态动作。加重原则：每周只推一项——先把同样重量从 8 次练到 12 次，再加重让次数回落到 8 次，如此循环。","action":"看进阶表","link":"#fitness","deepLink":"#fitness"},
 {"priority":4,"icon":"🎓","section":"求职准备","headline":"能力训练平台新增「30 天训练计划」：从 0 开始、每天 40-60 分钟、完成打勾","summary":"面向策略运营/用户增长与 AI 产品经理两个方向，30 天 91 个任务、4 个阶段（打地基→核心数据能力→业务分析能力→产品与实战）。每天 2-4 个任务并直达对应模块，点【开始计划】后自动记录今天是第几天。平台同时新增 Python 数据分析案例（22 个可复制案例）与 AI 产品经理面试题库（18 题）。训练进度通过同源 localStorage 回流到本站侧边栏入口。","action":"去训练","link":"#fitness","deepLink":"https://zr-president.github.io/training/"},
 {"priority":5,"icon":"🐳","section":"DeepSeek V4.1 Flash","headline":"V4.1 Flash 后续观察：MIT 开源权重已放出，社区微调版本开始出现","summary":"9/10 发布的 V4.1 Flash（5520 亿参数 MoE、原生视觉、KV 缓存 token 降至 V4-Flash 的 1/3.9）已放出开源权重，社区基于它做的垂直微调版本开始出现。对应用侧的意义：私有化部署可行性明显提升——此前必须用闭源旗舰处理敏感数据的场景（如含客户联系方式的跟进记录摘要），现在可以走本地开源模型，成本能低一个数量级。","action":"深度解读","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":6,"icon":"📉","section":"A股复盘","headline":"沪指 3888 点失守 3900 后观察企稳信号：成交 1.97 万亿，AI 硬件仍是结构主线","summary":"昨日沪指收 3888.11（643 家涨 / 4870 家跌），成交 1.97 万亿元。结构上仍是【AI 硬件】主线：覆铜板、光模块等环节受关注。当前判断维持不变——赚钱效应低、不适合追高；等企稳信号（收回关键位 + 放量）再谈加仓。今日需验证的判断：若继续跌破 3850 支撑，则本轮调整周期延长。","action":"看待验证判断","link":"#stock","deepLink":"#stock"},
 {"priority":7,"icon":"🛡️","section":"AI 治理","headline":"AI 内容标识与安全评估要求继续落地，To B 场景的合规成本开始显性化","summary":"生成式 AI 服务的内容标识、安全评估要求在持续落地。对做 AI 产品的人来说，这从【法务的事】变成了【产品需求】：AI 生成内容需要可标识、可溯源，转人工路径与日志留存要写进 PRD。这也是 AI PM 面试的高频考点——面试官常问【你的 AI 功能怎么满足合规要求】。","action":"看 AI 产品要点","link":"#ai-track","deepLink":"#ai-track"},
 {"priority":8,"icon":"🎬","section":"动漫追番","headline":"Re:Zero 第三季完结倒计时 17 天：本周更新第 10 话，剧情进入高潮段","summary":"Re:Zero 第三季进入收尾阶段，剩余约 3 话。本周第 10 话推进主线冲突，评价明显回升。想看完整番剧清单与官方海报可进动漫区（已按本季推荐更新海报与观看顺序）。","action":"看动漫区","link":"#anime","deepLink":"#anime"}
]
brief_new = ('var DAILY_BRIEFING = {\n  date: "2026-09-13",\n  highlights: '
             + j(highlights) + '\n};')
m = re.search(r'var DAILY_BRIEFING = \{[\s\S]*?\n\};', d)
if m:
    d = d[:m.start()] + brief_new + d[m.end():]
    print('OK DAILY_BRIEFING → 2026-09-13（8 张卡）')
else:
    print('MISS DAILY_BRIEFING')

# ==================== 2) DAILY_VOCAB ====================
words = [
 {"emoji":"🧍","category":"健身","word":"瘦胖子 (Skinny Fat)","definition":"体重正常甚至偏轻，但体脂率偏高、肌肉量不足的体型。表面看是【微胖】，本质是【肌肉太少】。","example":"170cm/59kg、体脂 15-18% 就是典型瘦胖子——BMI 只有 20.4，但肚子有赘肉。","why_matters":"这决定了策略方向：瘦胖子该增肌而不是减脂。按减脂做只会更瘦弱，肚子依然松。"},
 {"emoji":"🔁","category":"健身","word":"身体重组 (Body Recomposition)","definition":"同时增肌与减脂，让体重变化不大但体成分明显改善。","example":"12 周内增 3kg 肌肉、减 1kg 脂肪：体重 59→61kg，体脂率 16%→13.8%。","why_matters":"这是瘦胖子最该走的路线。新手与体脂中等的人重组效率最高，老手则很难同时做到。"},
 {"emoji":"📈","category":"健身","word":"渐进超负荷 (Progressive Overload)","definition":"逐步增加训练难度（重量、次数、组数或动作难度），让身体持续被迫适应。","example":"俯卧撑从自重 60 个 → 背包负重 4×8-12 至力竭；同样负重从 8 次练到 12 次再加重量。","why_matters":"这是增肌唯一必需的变量。不加重 = 只练耐力不长肌肉，是居家训练最常见的停滞原因。"},
 {"emoji":"⚖️","category":"健身","word":"干扰效应 (Interference Effect)","definition":"大量有氧训练会消耗本该用于肌肉合成与恢复的能量，削弱增肌效果。","example":"每周 3-4 次跳绳 HIIT + 热量缺口，结果体重掉了但肌肉几乎没长。","why_matters":"这是本次把跳绳从 3-4 次减到 1-2 次的直接原因。有氧不是不能做，是不能过量。"},
 {"emoji":"💪","category":"健身","word":"瘦体重 (Lean Body Mass)","definition":"体重减去脂肪后的部分，包含肌肉、骨骼、水分与器官。","example":"59kg、体脂 16% → 脂肪约 9.4kg，瘦体重约 49.6kg。","why_matters":"比体重更能反映体型。增肌期的目标是瘦体重上升，体重涨不涨反而是次要的。"},
 {"emoji":"🔥","category":"营养","word":"热量盈余 (Caloric Surplus)","definition":"每日摄入热量高于消耗，为肌肉合成提供原料与能量。","example":"增肌建议每天 +200 kcal 左右，对应每周增重 0.25-0.5kg。","why_matters":"盈余过大 → 脂肪一起长；没有盈余 → 长不出肌肉。轻微盈余才叫 lean bulk。"},
 {"emoji":"🥩","category":"营养","word":"蛋白质摄入区间 1.6-2.2g/kg","definition":"增肌期每公斤体重每天所需的蛋白质范围，超出后收益递减。","example":"59kg → 每天 94-130g；本方案取 110-130g。","why_matters":"低于 1.6g/kg 会限制增肌速度；高于 2.2g/kg 不再有额外收益，还可能加重肾脏负担（对你有结石预防需求尤其要注意补水）。"},
 {"emoji":"🏋️","category":"健身","word":"力竭 (Muscular Failure)","definition":"一组动作做到无法再用标准姿势完成下一次。","example":"俯卧撑做到第 10 个时动作开始变形，第 10 个就是该组终点。","why_matters":"增肌的有效组通常要接近力竭（留 1-3 次余力）。做 60 个还能继续的组，几乎没有增肌刺激。"},
 {"emoji":"🦵","category":"健身","word":"复合动作 (Compound Movement)","definition":"同时调动多个关节与肌群的动作，如深蹲、硬拉、划船、俯卧撑。","example":"保加利亚分腿蹲同时练股四头肌、臀大肌与核心稳定。","why_matters":"复合动作的增肌效率远高于孤立动作。居家条件下应把复合动作放在训练日开头。"},
 {"emoji":"📏","category":"健身","word":"围度优先于体重","definition":"用腰围、胸围、大腿围判断进步，而不是只看体重秤。","example":"体重从 59 涨到 62kg，但腰围不变、胸围与大腿各 +2cm → 长的是肌肉。","why_matters":"增肌期体重必然上涨（含水分与糖原）。只看体重会误判为【变胖】而错误减量。"}
]
vocab_new = ('var DAILY_VOCAB = {\n  date: "2026-09-13",\n  words: ' + j(words) + '\n};')
m2 = re.search(r'var DAILY_VOCAB = \{[\s\S]*?\n\};', d)
if m2:
    d = d[:m2.start()] + vocab_new + d[m2.end():]
    print('OK DAILY_VOCAB → 2026-09-13（10 词）')
else:
    print('MISS DAILY_VOCAB')

# ==================== 3) LEARN_PATHS（把旧 items 归档，再放新 items） ====================
learn_items = [
 {"section":"健身","emoji":"🧍","title":"瘦胖子是什么？为什么体脂率会被【肌肉少】推高？","content":"同样 59kg，肌肉多的人体脂率可以只有 10%，肌肉少的人却会到 16%——因为体脂率 = 脂肪 ÷ 体重，而肌肉也是体重的一部分。瘦胖子的体重正常，但瘦体重偏低，于是脂肪占比被动升高。所以问题不是【脂肪太多要减】，而是【肌肉太少要加】。","takeaway":"体脂率是个比值。可以通过降分子（减脂）改善，也可以通过升分母（增肌）改善——瘦胖子应该选后者。"},
 {"section":"健身","emoji":"🔁","title":"为什么减脂和增肌很难同时做？","content":"减脂需要热量缺口，增肌需要热量盈余，两者能量方向相反。能做到【重组】的前提是：训练新手、体脂中等、蛋白质充足、睡眠足够。满足这些条件时身体会优先用脂肪供能、用食物蛋白合成肌肉，效果慢但真实存在。","takeaway":"重组适合新手与瘦胖子；训练 2 年以上、体脂又低的人，最好分增肌期与减脂期来做。"},
 {"section":"健身","emoji":"📈","title":"渐进超负荷：增肌唯一必需的变量","content":"肌肉增长的信号是【机械张力】——肌肉必须在超出以往的水平下发力。如果重量、次数、节奏长期不变，身体就没有理由继续长肌肉，只会提高神经效率与耐力。所以同样一组动作，必须持续加重量、加次数或加难度。","takeaway":"判断训练有没有效，先问一句：这周的负重或次数比上周多了吗？没有就是在原地踏步。"},
 {"section":"健身","emoji":"⏸️","title":"为什么自重训练会【失效】？适应原理","content":"身体对重复刺激会产生适应：同样的俯卧撑做到第 4 周，神经与肌肉都已习惯，此后每组做得再多也只是提升耐力。这就是为什么能一口气做 60 个俯卧撑的人，胸肌往往并不大。","takeaway":"自重不是不能增肌，而是必须不断升级难度（负重、单侧、慢离心、爆发）才能维持刺激。"},
 {"section":"健身","emoji":"🦵","title":"练腿为什么能提升全身增肌效率？","content":"腿部肌群体量占全身一半以上，大重量深蹲等复合动作会带来更强的全身性激素与代谢反应，同时显著提高整体训练容量。不练腿的另一后果是体型失衡：上身壮、下身细，视觉上并不好看。","takeaway":"想增肌却不练腿，等于只用一半的引擎——效率与观感都会打折。"},
 {"section":"健身","emoji":"⚖️","title":"干扰效应：为什么有氧做多了影响增肌？","content":"有氧与力量训练争夺同一批恢复资源（糖原、氨基酸、恢复时间），并且有氧会激活 AMPK 通路、抑制肌肉合成的 mTOR 通路。每周 1-2 次中等强度有氧影响不大，但 4 次以上高强度有氧 + 热量缺口，增肌基本停滞。","takeaway":"增肌期有氧要【够用就好】：控心肺与体脂靠 1-2 次，不要当主力练。"},
 {"section":"营养","emoji":"🔥","title":"热量盈余该加多少？lean bulk 的 +200 逻辑","content":"肌肉合成速度有上限：新手每月约 1-2kg，训练久了更低。盈余太大，多出来的热量只能变成脂肪。每天 +200 kcal 左右（每周增重 0.25-0.5kg）是兼顾增肌与控脂的常用区间。","takeaway":"增肌速度慢不是失败，是生理上限。追求每周涨 1kg 的人，涨的大部分是脂肪。"},
 {"section":"营养","emoji":"🥩","title":"蛋白质 1.6-2.2g/kg 这个区间是怎么来的？","content":"多项剂量-反应研究显示：增肌期蛋白质摄入从 1.6g/kg 起收益明显，到 2.2g/kg 左右趋于平台，再往上没有额外增肌收益。区间下限对应维持，上限对应热量缺口较大或训练量很高的情况。","takeaway":"59kg 的你，110-130g 就够了。把蛋白分散到 4-6 餐比一顿猛吃吸收更好。"},
 {"section":"健身","emoji":"🧪","title":"身体重组适合谁？怎么判断自己在不在状态","content":"适合：训练新手、体脂 15-25% 的男性、长期节食后代谢偏低者、以及【体重正常但肌肉少】的瘦胖子。判断依据：训练是否持续加重、蛋白是否达标、睡眠是否 ≥7 小时、体重是否缓慢上升或持平但围度改善。","takeaway":"重组不是玄学，它有明确适用人群与可验证指标——围度与力量，而不是体重秤。"},
 {"section":"健身","emoji":"📏","title":"为什么增肌期【看围度不看体重】？","content":"增肌期体重上涨是必然的：除了肌肉，还有糖原与结合水（每 1g 糖原约带 3g 水）。所以头几周体重快速上涨大多是水分，而真实进步体现在腰围不变、胸围与大腿增加、同重量能多做几次。","takeaway":"只看体重会误判为【变胖】从而错误减量，最后既没长肌肉也没瘦——这是增肌期最常见的自我破坏。"}
]

lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],\s*\n\s*archive:', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_archive = am.group(1).strip().rstrip(',')
        new_body = ('\n  updated: "2026-09-13",\n  current_day: 8,\n  items: ' + j(learn_items) + ',\n'
                    '  archive: {\n    "2026-09-12": [\n' + old_items + '\n    ]'
                    + (',\n' + old_archive if old_archive else '') + '\n  }\n')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + new_body + '};' + d[lm.end():]
        print('OK LEARN_PATHS → 2026-09-13（10 条·Day 8，旧 10 条已归档为 2026-09-12）')
    else:
        print('MISS items/archive 解析', bool(im), bool(am))
else:
    print('MISS LEARN_PATHS')

# ==================== 4) 版本号 ====================
d = d.replace('var SITE_VERSION = "1.8.13";', 'var SITE_VERSION = "1.8.14";')
d = re.sub(r'版本1\.8\.13', '版本1.8.14', d)
d = re.sub(r'"update_date":\s*"2026年9月12日"', '"update_date": "2026年9月13日"', d)
print('OK 版本 1.8.13 → 1.8.14；update_date → 2026年9月13日')

open(FP, 'w', encoding='utf-8').write(d)
print('已写回 daily_data.js')
