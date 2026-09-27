# -*- coding: utf-8 -*-
"""更新第二步：课堂 / 待办 / 日期同步 / 版本"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-09-27'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

learn = [
 {"section":"AI","emoji":"🤖","title":"多模态是什么？为什么「能看图」是分水岭？","content":"多模态指模型能同时理解文字、图像、音频、视频等多种输入。此前的做法是先用 OCR 把图片转成文字再交给模型，中间会丢信息、也会引入识别错误；原生支持视觉的模型可以直接读原图。对业务的意义在于：大量真实数据本来就是图片形式——票据、聊天截图、商品图、表格照片。","takeaway":"多模态不是【多了个功能】，而是把一整类此前无法处理的数据纳入了可分析范围。"},
 {"section":"技术","emoji":"🔧","title":"本地优先：为什么「数据存本机」是产品选择而不是技术限制？","content":"本地优先指的是数据默认存在用户设备上、功能在本机即可完整运行，而不是依赖服务器。它听起来像是技术受限，其实是产品选择：对个人工具类产品，本地优先同时做到两件事——隐私成本降到最低，功能却完全不打折。代价是换设备不同步。","takeaway":"判断该不该上云，先问一句：用户愿意为【多设备同步】付出多少隐私代价？"},
 {"section":"运营","emoji":"📊","title":"RFM 分层：怎么用三个维度把用户分开？","content":"RFM 用三个维度刻画用户：最近一次消费时间（Recency）、消费频率（Frequency）、消费金额（Monetary）。三者组合出可运营的群体：高 R 高 F 高 M 是核心用户值得维护；低 R 高 F 是【高价值但快流失】的预警人群，最该优先触达；高 R 低 F 是新人需要引导。","takeaway":"分层的目的不是把用户分类，而是让每个群体对应一个具体动作，而不是对所有人发同样的券。"},
 {"section":"健身","emoji":"💪","title":"增肌平台期：为什么第 3-4 周容易卡住？","content":"前两周进步明显（动作熟悉 + 神经适应），到第 3-4 周常出现停滞。原因通常有两个：一是容量不再上升（同重量同次数重复），二是恢复不足（吃得不够或睡得不够）。判断顺序：先检查体重是否在涨、睡眠是否达标，再考虑调整训练计划。","takeaway":"平台期优先怀疑【吃与睡】，而不是训练动作——大多数人卡住的原因不在健身房。"},
 {"section":"财经","emoji":"📈","title":"仓位管理：为什么「留现金」也是一种仓位？","content":"仓位管理决定你把多少比例的资产放在风险资产里，它独立于【买什么】的判断。留现金不是【没建仓】，而是一种主动选择——它的作用是应对不确定性（如长假七天无法交易）和保留在下跌中加仓的能力。","takeaway":"决定回撤幅度的往往不是选股，而是仓位。很多人研究半年买什么，却从没想过拿多少钱在里面。"},
 {"section":"求职","emoji":"🎓","title":"秋招节奏：为什么国庆后是关键窗口？","content":"秋季招聘的高峰通常在 9-10 月，但国庆假期后往往还有一波：企业新财年预算落地、秋招进入补录阶段，而此时大部分候选人的注意力已经分散。这意味着竞争强度可能略低于 9 月高峰。合理安排是：假期前打磨材料，节后集中投递。","takeaway":"把【准备】和【投递】分开放进不同的时间窗，比在高峰期边准备边投更有效。"},
 {"section":"理财","emoji":"💰","title":"流动性分层：钱为什么要按「什么时候用」分开放？","content":"同一个金额，按使用时间分三层：随时可能用（应急金）、1-3 年内要用（如首付）、5 年以上不用（长期增值）。三层对应完全不同的风险等级。最常见的亏钱方式就是不分层——用随时要用的钱去承担短期波动，结果被迫在低位卖出。","takeaway":"先按【什么时候用】分钱，再按【能承受多少波动】选产品。顺序反了就会出问题。"},
 {"section":"学习","emoji":"🧠","title":"间隔重复：为什么分散复习比集中刷题有效？","content":"集中学习（一天刷三遍）带来的是短期熟悉感，很快消退；间隔重复（隔 2 天、7 天、21 天各复习一次）才能形成长期记忆。原理是每次【快要忘记时再想起来】的过程，本身就在强化记忆痕迹。","takeaway":"错题本的价值不在记录，而在按间隔定期重做——只抄不重做等于没做。"},
 {"section":"生活","emoji":"🍂","title":"假期综合征：怎么把节后恢复期从 5 天压到 1 天？","content":"长假后的低效主要来自作息紊乱，而昼夜节律的重新校准需要时间，通常 3-5 天。压缩恢复期的关键是把假日期间的【起床时间浮动控制在 1 小时内】——起床时间是昼夜节律最强的锚点，它不乱，整条节律就不会乱。","takeaway":"假期不必严格自律，但起床时间这一项值得守住，它决定了节后的启动成本。"},
 {"section":"产品","emoji":"⚖️","title":"灰度发布：为什么 AI 功能尤其不能一次全量上线？","content":"灰度发布指新功能先对小比例用户开放，观察指标正常后再逐步放量。传统功能可以靠测试覆盖主要路径，但 AI 功能的效果不确定性高——它面对的是开放输入，很难穷举测试用例。因此灰度是必需的：它用真实流量替代测试用例。","takeaway":"AI 功能的上线节奏应该是 1% → 10% → 50% → 全量，每一档都要有明确的放量门槛。"}
]
lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_arch = re.sub(r',\s*$', '', am.group(1).strip())
        nb = ('\n  updated: "%s",\n  current_day: 22,           // 当前学到第几天\n  items: %s,\n'
              '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
              '  archive: {\n    "2026-09-26": [\n%s\n    ]%s\n  }\n') % (
            TODAY, j(learn), old_items, (',\n' + old_arch) if old_arch else '')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + nb + '};' + d[lm.end():]
        print('✅ 小白课堂 → 10 条（10 领域），旧 10 条归档为 2026-09-26')

decisions = [
 {"icon":"📊","action":"国庆前三线复盘：健身 / A股 / 求职各写三句话","why":"假期前是做阶段复盘的最好时机；不写下来，七天后就想不起当时的判断依据","how":"每条线写：①现在处在什么位置 ②最关键的下一步动作 ③需要在假期里维持什么（健身：容量与体重；A股：3900 站稳与否；求职：作品集进度）","priority":"P0"},
 {"icon":"⚖️","action":"早晨空腹称重，完成增肌第 2 周体重校准","why":"体重是增肌期唯一可靠的热量校准依据","how":"与上周对比：涨 0.25-0.5kg 保持；不涨加 200 kcal；涨超 0.75kg 减 200 kcal（只调主食）","priority":"P0"},
 {"icon":"📈","action":"决定节前仓位（9/28-9/29 最后两个交易日）","why":"长假七天无法交易，期间外盘波动由你被动承担；仓位应在假期前而不是假期中决定","how":"按自己的风险承受度决定是否降仓：留够现金 → 睡得着 → 才拿得住；把决定与理由写进判断台账","priority":"P0"},
 {"icon":"📚","action":"定国庆假期的学习最低维持量：每天 40 分钟","why":"假期计划过满会导致一天都不完成，完全不学则节后重启成本高；【最低维持量】比【冲刺计划】更可行","how":"定一个每天都能做到的量：如 2 道 SQL + 1 道 AI 判读题；用训练平台的按天打勾记录，不追求跑完全部任务","priority":"P0"},
 {"icon":"💪","action":"制定增肌第 3 周计划：明确本周要推的那一项","why":"第 3 周容易出现平台期，提前定好推进目标才能判断是否卡住","how":"从第 2 周记录里挑 1-2 个动作作为加重对象；其余动作保持；同时确认假期期间的训练安排（每天最低 15 分钟自重训练）","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_DECISIONS = {\n  updated: "%s",\n  items: %s\n};' % (TODAY, j(decisions)) + d[m.end():]
    print('✅ 今日待办 → 5 条（9/27 周日版）')

# 日期同步
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-09-2[0-9])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
d, n2 = re.subn(r'("update_date":\s*")([^"]+)(")', lambda m: m.group(1) + CN + m.group(3), d)
d, n3 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 日期同步：updated %d · update_date %d · update_time %d' % (n1, n2, n3))

fixes = [('9月26日（周六）', '9月27日（周日）'), ('9月26日', '9月27日'),
         ('2026年9月26日', CN), ('9月26 第 2 周收官', '9月27 第2周收官'),
         ('9/26 第 2 周收官', '9/27 第2周收官'),
         ('追番第45天', '追番第46天'),
         ('倒计时4天', '倒计时3天'), ('倒计时 4 天', '倒计时 3 天'),
         ('本周（9/22-9/26）', '上周（9/22-9/26）')]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 文本日期/天数：%d 处' % c)

d = d.replace('var SITE_VERSION = "1.8.18";', 'var SITE_VERSION = "1.8.19";')
d = re.sub(r'版本1\.8\.1[0-9]', '版本1.8.19', d)
print('✅ 版本 → 1.8.19')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])

IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.19', h)
open(IP, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.19')
