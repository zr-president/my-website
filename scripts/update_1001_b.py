# -*- coding: utf-8 -*-
"""第二步：课堂 / 待办 / 日期同步 / 版本"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-10-01'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

learn = [
 {"section":"AI","emoji":"🤖","title":"推理成本：为什么「都用最好的模型」是错的？","content":"模型每回答一次都要付算力费（按 token 计）。不同模型价差可达几十倍：同一个问题，大模型要 0.02 元，小模型只要 0.0005 元。如果一天调用十万次，这个差价就是 2000 元 vs 50 元。所以模型选型不是【哪个更强】，而是【这个场景需要多强】。","takeaway":"先用最强模型验证可行性，再降级到够用的最便宜模型 —— 而不是一上来就全量用大模型。"},
 {"section":"技术","emoji":"🔧","title":"冷启动：为什么「第一次总是最慢」？","content":"冷启动指程序首次运行、缓存为空时的启动过程。它慢是因为要从零准备运行环境：下载依赖、构建索引、初始化缓存。一旦完成，后续启动只读缓存，速度可能差几十倍（例如 DSH 首次下载 200MB 要几分钟，之后几秒）。","takeaway":"冷启动是用户流失的高发环节。产品设计上要能预热就预热，绝不把重活留到用户第一次使用。"},
 {"section":"运营","emoji":"📊","title":"留存曲线：怎么看一条曲线判断产品好坏？","content":"把次日、7 日、30 日等时间点的留存率连成曲线。判断标准是【曲线在哪走平】：如果 30 日后稳定在 15-20% 不再下滑，说明找到了真正的核心用户；如果一路下滑到接近 0，说明产品只有新鲜感没有使用价值。","takeaway":"留存曲线走平的位置越高，产品的长期价值越大。看留存要看【平在哪】，而不是【起点多高】。"},
 {"section":"健身","emoji":"💪","title":"训练容量：增肌到底该加什么？","content":"训练容量 = 组数 × 次数 × 负重，是增肌最核心的可控变量。三种加法：加重量（最直接）、加次数（同重量练到更多次）、加组数（增加总量）。每周只推其中一项，才能判断哪个起了作用；同时改多项，进步或停滞都说不清原因。","takeaway":"增肌不是比谁动作花，而是比谁能持续把容量往上推。进步的单位是【周】不是【次】。"},
 {"section":"财经","emoji":"📈","title":"跳空缺口：为什么长假前必须提前定仓位？","content":"跳空缺口指开盘价直接跳过前一日价格区间，中间留下一段无成交的空白。长假是跳空高发场景 —— 七天里海外市场照常交易，而你的持仓无法调整。10/8 开盘时，价格可能已经离你上次看到的位置很远。","takeaway":"长假前定仓位，本质是承认【假期里你没有操作权】。仓位应该由你能承受多大跳空来决定。"},
 {"section":"求职","emoji":"🎓","title":"STAR 法则：怎么把一段经历讲成一种能力？","content":"STAR 是描述经历的结构：情境（Situation）→ 任务（Task）→ 行动（Action）→ 结果（Result）。关键在于【行动】部分要讲出思考过程：为什么选这个方案、排除了哪些选项、依据是什么。只讲做了什么，面试官听不出你的判断力。","takeaway":"面试官想听的是【你怎么想的】，不是【你做了什么】。同一个项目，讲清决策过程比罗列成果更有说服力。"},
 {"section":"理财","emoji":"💰","title":"复利：为什么「早开始」比「追高收益」更靠谱？","content":"复利指收益本身继续产生收益。假设同样投 10 万：年化 3% 十年后约 13.4 万，年化 6% 约 17.9 万 —— 收益率翻倍，结果只多约 1/3。但如果把期限从 10 年拉到 20 年，年化 3% 也能到约 18 万。","takeaway":"时间的杠杆大于收益率的杠杆。追求高收益往往伴随本金风险，而延长时间几乎无风险。"},
 {"section":"学习","emoji":"🧠","title":"主动回忆：为什么「反复重读」几乎没用？","content":"重读带来的是熟悉感 —— 你看一遍觉得【这个我知道】，但这种熟悉并不等于能想起来。主动回忆是合上材料，强迫自己把内容写出来或讲出来，再对照查漏。前者是识别，后者是提取，只有提取才真正强化记忆。","takeaway":"检验学会没有的标准不是【看着眼熟】，而是【合上书能讲出来】。"},
 {"section":"生活","emoji":"🍂","title":"社交时差：假期作息该怎么管才不难受？","content":"社交时差指工作日与休息日作息差异过大造成的疲惫感，本质是生物钟被反复拉扯。长假里最容易发生：平时 7 点起，假期每天 11 点起，节后像出了趟国。而昼夜节律的重新校准通常需要 3-5 天。","takeaway":"假期只需要守一个指标：起床时间浮动不超过 1 小时。其余（几点睡、午睡多久）都可以宽松。"},
 {"section":"产品","emoji":"⚖️","title":"A/B 测试：为什么「指标选错」会让结论完全反过来？","content":"A/B 测试把用户随机分组，比较不同版本。它的前提是【指标能代表目标】。经典反例：把【点击率】当指标，会导致标题越来越夸张（骗点击），而长期留存反而下降。指标选错时，数据越显著，跑偏越远。","takeaway":"做 A/B 前先问一句：这个指标涨了，真的代表用户更满意吗？答不上来就先别测。"}
]
lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_arch = re.sub(r',\s*$', '', am.group(1).strip())
        nb = ('\n  updated: "%s",\n  current_day: 23,           // 当前学到第几天\n  items: %s,\n'
              '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
              '  archive: {\n    "2026-09-27": [\n%s\n    ]%s\n  }\n') % (
            TODAY, j(learn), old_items, (',\n' + old_arch) if old_arch else '')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + nb + '};' + d[lm.end():]
        print('✅ 小白课堂 → 10 条（10 领域），旧归档为 2026-09-27')

decisions = [
 {"icon":"🎯","action":"给假期七天定三条边界：训练 / 作息 / 学习","why":"假期失控通常不是因为懒，而是因为没有【最低标准】—— 一旦某天没做到就整体放弃","how":"训练：每天最低 15 分钟自重；作息：起床时间浮动 ≤1 小时；学习：每天 40 分钟（2 道 SQL + 1 道判读）。写在手机备忘录里，每天打勾","priority":"P0"},
 {"icon":"💪","action":"增肌假期第 1 练：15 分钟自重，跑通一次","why":"第 1 天做到，后面七天才有连续性；第 1 天没做，计划大概率作废","how":"俯卧撑 3×10 / 深蹲 3×15 / 卷腹 3×15 / 平板支撑 3×30秒，不追求力竭，只求完成","priority":"P0"},
 {"icon":"📚","action":"学习最低维持量跑通一次","why":"验证 40 分钟这个量是否真的可行 —— 做不到就当场调低，别等计划废掉才发现","how":"训练平台做 2 道 SQL + 1 道 AI 判读题，用按天打勾记录，完成后停手","priority":"P0"},
 {"icon":"🎓","action":"把 DSH 桌面端对比 + Jev 接入决策整理成产品分析文档","why":"假期是唯一有大块时间做深度输出的窗口；这份文档直接服务节后投递","how":"结构：背景 → 对比维度 → 结论与依据 → 什么条件下改变结论。每份控制在 2 页，用表格呈现","priority":"P1"},
 {"icon":"📈","action":"A股假期复盘：梳理 9 月 3900 关口争夺的判断逻辑","why":"假期无法交易，正好用来检验自己的判断框架 —— 而不是盯盘","how":"回顾 9 月每一次判断的依据与结果：哪些对了、哪些是运气、哪些逻辑当时就不成立。写下来，10/8 开市前看一遍","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_DECISIONS = {\n  updated: "%s",\n  items: %s\n};' % (TODAY, j(decisions)) + d[m.end():]
    print('✅ 今日待办 → 5 条（10/1 假期第1天版）')

# 日期同步
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-09-2[0-9])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
d, n2 = re.subn(r'("update_date":\s*")([^"]+)(")', lambda m: m.group(1) + CN + m.group(3), d)
d, n3 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 日期同步：updated %d · update_date %d · update_time %d' % (n1, n2, n3))

# 文本日期替换
fixes = [('9月27日（周日）', '10月1日（周四）'), ('2026年9月27日', CN), ('9月27日', '10月1日'),
         ('9/27 第2周收官', '10/1 假期第1天'), ('追番第46天', '追番第50天'),
         ('倒计时3天', '已完结'), ('倒计时 3 天', '已完结'), ('下周（9/28-9/29 两个交易日）', '假期后（10/8 开市）'),
         ('9/28-9/29（节前最后两个交易日）操作预案', '10/8 开市操作预案')]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 文本日期：%d 处' % c)

d = d.replace('var SITE_VERSION = "1.8.19";', 'var SITE_VERSION = "1.8.20";')
d = re.sub(r'版本1\.8\.1[0-9]', '版本1.8.20', d)
print('✅ 版本 → 1.8.20')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])

IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.20', h)
open(IP, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.20')
