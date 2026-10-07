# -*- coding: utf-8 -*-
"""第二步：课堂 / 待办 / 日期同步 / 版本"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-10-07'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

learn = [
 {"section":"AI","emoji":"🤖","title":"上下文窗口：为什么模型会「忘记」前面说过的话？","content":"上下文窗口是模型单次能处理的最大文本长度（按 token 计）。超出这个长度，最早的内容会被挤出去 —— 不是模型故意忘，而是它物理上读不到了。128K 窗口大约相当于一次能读 6-8 万字中文。","takeaway":"长任务要先想清楚【哪些信息必须全程保留】，把它们放在末尾或单独复述，而不是指望模型记住全部对话。"},
 {"section":"技术","emoji":"🔧","title":"幂等：为什么「重试」会造成重复扣款？","content":"幂等指同一操作执行一次和多次，结果相同。【把余额设为 100】是幂等的；【余额加 10】不是 —— 重试三次就加了 30。而网络请求超时不代表对方没收到，客户端重试是常规行为。","takeaway":"涉及金额、库存、订单的接口必须幂等（通常用一个唯一请求号做去重）。这是接口设计的基本功。"},
 {"section":"运营","emoji":"📊","title":"转化漏斗：怎么找到「漏得最多」的那一步？","content":"把用户从进入到完成目标拆成若干环节，逐环节计算转化率。例如 1000 访问 → 300 注册（30%）→ 90 下单（30%）→ 60 复购（67%）。比较各环节的【流失率】，流失最大的那一步就是优先优化对象。","takeaway":"【效果不好】是无从下手的描述，【注册环节流失 70%】才是可执行的问题。漏斗的作用是把问题定位到具体一步。"},
 {"section":"健身","emoji":"💪","title":"恢复期：为什么练得越勤反而没效果？","content":"训练是对肌肉的破坏，真正的增长发生在训练后的恢复期（大肌群约需 48 小时）。恢复不足时，下一次训练是在没修复的基础上继续破坏，表现会下降而不是上升。恢复的两个关键条件：足够的热量蛋白 + 足够睡眠。","takeaway":"训练频率不是越高越好。同一肌群两次训练之间要留够恢复时间，睡不够时降低强度比硬练更明智。"},
 {"section":"财经","emoji":"📈","title":"量价背离：缩量上涨到底说明什么？","content":"量价背离指价格与成交量方向不一致。典型形态是【指数创新高但成交量萎缩】。它的含义是：上涨靠的是少量资金推动，而不是广泛买盘。指数可以靠权重股拉起来，但没有成交量配合的上涨通常难以持续。","takeaway":"看指数不能只看点位，要同时看量。缩量上涨是【上涨质量差】的提示，不是买入信号。"},
 {"section":"求职","emoji":"🎓","title":"作品集：为什么它比简历更有说服力？","content":"简历是自述（【我具备分析能力】），作品集是证据（一份含背景-分析-结论的文档，读者可以自己判断你的水平）。对于转行、经验不足或跨领域的人，作品集往往能弥补简历的短板，因为它跳过了【我说我行】直接展示【我做过什么】。","takeaway":"一份结构清晰的两页产品分析，胜过十句形容词。作品集的关键不是数量，而是每份都能看出【你怎么想的】。"},
 {"section":"理财","emoji":"💰","title":"应急金：为什么它是整个理财计划的地基？","content":"应急金是专门应对失业、疾病等突发状况的现金储备，通常覆盖 3-6 个月支出，放在随时可取的地方（如货币基金）。它的作用不是赚收益 —— 收益率低得可以忽略 —— 而是让你在意外发生时不必被迫卖出长期资产。","takeaway":"先有应急金再谈投资。没有它，一次突发支出就可能让你在最差的价格卖掉长期持仓。"},
 {"section":"学习","emoji":"🧠","title":"费曼技巧：怎么检验自己是不是真的懂了？","content":"方法是用最通俗的语言把知识讲给一个外行听，不许用术语。卡住的地方、需要含糊带过的地方，就是你的理解缺口。这个方法的有效性在于：复述会让你立刻发现自己其实只是在【认得这个词】，而不是【理解了这件事】。","takeaway":"检验理解的标准是【能讲明白】，而不是【看着眼熟】。讲不通的地方就是下一步该学的地方。"},
 {"section":"生活","emoji":"🍂","title":"节后综合征：为什么它主要是作息问题而不是态度问题？","content":"长假后出现的注意力涣散、疲惫、效率低，主因是昼夜节律被打乱 —— 生物钟需要 3-5 天重新校准。把它当成【意志力不够】会带来额外的自责，反而更难受。真正有效的干预是固定起床时间，而不是靠打鸡血。","takeaway":"节后状态差是生理现象。提前一天把起床时间固定住，比任何自律方法都有效。"},
 {"section":"产品","emoji":"⚖️","title":"MVP：为什么「先做小」比「一次做全」成功率高？","content":"MVP（最小可行产品）指用最小成本做出能验证核心假设的版本。理由是：大部分产品失败源于【方向错了】而不是【功能不够】。做全再上线，一旦方向错，浪费的是全部投入；做小先验证，错的成本只有一点点。","takeaway":"先验证【用户是否真的需要】，再投入【把它做好】。顺序反了，做得越精致损失越大。"}
]
lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_arch = re.sub(r',\s*$', '', am.group(1).strip())
        nb = ('\n  updated: "%s",\n  current_day: 24,           // 当前学到第几天\n  items: %s,\n'
              '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
              '  archive: {\n    "2026-10-01": [\n%s\n    ]%s\n  }\n') % (
            TODAY, j(learn), old_items, (',\n' + old_arch) if old_arch else '')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + nb + '};' + d[lm.end():]
        print('✅ 小白课堂 → 10 条（10 领域），旧归档为 2026-10-01')

decisions = [
 {"icon":"🌙","action":"今晚把作息调回来：明早按工作日的固定时间起床","why":"今天是压缩节后恢复期的最后窗口；起床时间是昼夜节律最强的锚点","how":"今晚提前 1 小时上床（睡不着也躺着），明早到点就起，不补觉到中午。哪怕只睡 6 小时也先固定时间","priority":"P0"},
 {"icon":"📊","action":"假期三条边界执行复盘：训练/作息/学习各打了几次勾","why":"统计的意义不是评判自己，而是判断标准定得是否合理 —— 完成率低说明量太大，不是意志力问题","how":"拿张纸写下：七天里训练完成几次、有几天起床时间浮动在 1 小时内、几天完成了 40 分钟学习。完成率 <50% 的项目明天把标准调低","priority":"P0"},
 {"icon":"📈","action":"明日开市准备：核对假期外盘表现 + 写下三个观察点","why":"10/8 开盘可能有跳空，提前看清单才能按信号操作而不是按情绪；但今晚看一次就够，不要整晚盯","how":"① 查假期期间海外主要市场的实际涨跌（不猜）② 把 10/1 定的三个观察点写在一张纸上：量能能否放大 / 3900 能否站稳 / AI 硬件主线是否延续 ③ 想好每种情况下的仓位动作","priority":"P0"},
 {"icon":"🎓","action":"求职材料收尾：优先补齐最想去的 3 家","why":"节后第一波招聘窗口就在明天；等全部材料完美会错过窗口","how":"从目标公司里挑 3 家，把作品集与简历针对它们调整好。不要等全部公司都准备好 —— 先投 3-5 家试水，按反馈再改","priority":"P0"},
 {"icon":"💪","action":"定好明天回健身房的第一练内容","why":"假期后直接上极限重量容易受伤，且第一次训练的体验会影响后续坚持","how":"用假期前 70-80% 的重量重新激活，把注意力放在动作质量上；本周目标是把容量恢复到假期前水平，而不是突破","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_DECISIONS = {\n  updated: "%s",\n  items: %s\n};' % (TODAY, j(decisions)) + d[m.end():]
    print('✅ 今日待办 → 5 条（10/7 假期收官版）')

# 日期同步
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-10-0[1-6])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
d, n2 = re.subn(r'("update_date":\s*")([^"]+)(")', lambda m: m.group(1) + CN + m.group(3), d)
d, n3 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 日期同步：updated %d · update_date %d · update_time %d' % (n1, n2, n3))

fixes = [('10月1日（周四）', '10月7日（周三）'), ('2026年10月1日', CN), ('10月1日', '10月7日'),
         ('10/1-10/7 休市', '假期休市中'), ('追番第50天', '追番第56天'),
         ('（10/1 更新 · A股 10/1-10/7 休市）', '（10/7 更新 · 假期最后一天）'),
         ('（10/1 更新）', '（10/7 更新）'), ('· 10/1 沉淀', '· 假期沉淀')]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 文本日期：%d 处' % c)

d = d.replace('var SITE_VERSION = "1.8.20";', 'var SITE_VERSION = "1.8.21";')
d = re.sub(r'版本1\.8\.2[0-9]', '版本1.8.21', d)
print('✅ 版本 → 1.8.21')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])

IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.21', h)
open(IP, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.21')
