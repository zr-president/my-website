# -*- coding: utf-8 -*-
"""更新 2026-10-26（周一）内容 · 第 1 批：stock / anime / music / novel / gaming / learning

做法说明（沿用踩过的坑）：
- 每个分区的 summary/trend/tip 用「定位分区块 → 解析出字符串字面量 → 原地替换」的方式改
- 兼容单引号与双引号两种写法（老数据两种混用）
- 只改这三个字段，updated 由后面的日期同步统一处理
- archive 的键绝对不动
"""
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DP = os.path.join(P, 'daily_data.js')
TODAY = '2026-10-26'

src = open(DP, encoding='utf-8').read()

# ---------------- 字符串字面量解析器 ----------------
def find_string_literal(s, pos):
    """从 pos 开始（可能是引号）解析一个 JS 字符串字面量，返回 (start_quote, end_after_quote, raw)"""
    i = pos
    while i < len(s) and s[i] in ' \t\r\n':
        i += 1
    if i >= len(s) or s[i] not in '"\'':
        return None
    q = s[i]
    j = i + 1
    out = []
    while j < len(s):
        c = s[j]
        if c == '\\':
            out.append(s[j:j+2]); j += 2; continue
        if c == q:
            return (i, j + 1, s[i:j+1])
        out.append(c); j += 1
    return None

def esc_js(text, quote='"'):
    """把文本编码成 JS 字符串字面量的内部内容"""
    text = text.replace('\\', '\\\\')
    text = text.replace('\n', '\\n')
    if quote == '"':
        text = text.replace('"', '\\"')
    else:
        text = text.replace("'", "\\'")
    return text

# ---------------- 定位分区块 ----------------
# 坑：daily_data.js 里既有 "anime": {...}（要闻卡片的字段）又有 anime: {...}（INSIGHTS 分区）。
# 只在 INSIGHTS 变量范围内搜索，避免匹配到卡片。
INS_START = src.index('var INSIGHTS')

def section_span(s, key):
    """返回 (block_start, block_end) —— 从 INSIGHTS 内 `key: {` 的左花括号到配对的右花括号"""
    pat = re.compile(r'(?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\{')
    m = pat.search(s, INS_START)
    if not m:
        return None
    start = m.end() - 1          # 指向 {
    depth = 0
    i = start
    in_str = None
    while i < len(s):
        c = s[i]
        if in_str:
            if c == '\\':
                i += 2; continue
            if c == in_str:
                in_str = None
            i += 1; continue
        if c in '"\'':
            in_str = c; i += 1; continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return (start, i + 1)
        i += 1
    return None

def set_field(s, key, field, value):
    span = section_span(s, key)
    if not span:
        raise SystemExit('❌ 找不到分区 %s' % key)
    bs, be = span
    block = s[bs:be]
    fp = re.compile(r'(["\']?' + field + r'["\']?\s*:\s*)')
    fm = fp.search(block)
    if not fm:
        raise SystemExit('❌ 分区 %s 找不到字段 %s' % (key, field))
    lit_start = fm.end()
    lit = find_string_literal(block, lit_start)
    if not lit:
        raise SystemExit('❌ 分区 %s 的 %s 不是字符串字面量' % (key, field))
    qs, qe, raw = lit
    q = raw[0]
    newlit = q + esc_js(value, q) + q
    newblock = block[:qs] + newlit + block[qe:]
    return s[:bs] + newblock + s[be:]

# ==================================================================
# 内容（2026-10-26 周一）
# ==================================================================
CONTENT = {}

CONTENT['stock'] = {
'summary': '''<b>10月26日（周一）开盘 · 10 月最后一个完整交易周</b>——10/8 恢复交易至今已 <b>13 个交易日</b>，本周（10/26-10/30）是 10 月唯一的完整交易周，也是三季报披露的最后 5 个交易日（10/31 截止）。<br><br>这个时间点的特殊性在于<b>两件事撞在一起</b>：① 三季报必须在 10/31 前披露完，本周是业绩地雷与超预期同时释放的窗口；② 月末资金面通常偏紧，机构调仓会在最后一周完成。所以本周的量能与结构，会比月中更能说明问题。''',
'trend': '''<b>本周（10/26-10/30）的三个观察点，按优先级排</b><br><br><b>① 量能站不站得住 2.2 万亿。</b>这是判断【存量博弈】还是【增量市】的第一信号。存量区间在 1.8-2 万亿，撑不起普涨；站上 2.2 万亿且能连续 3 天，才算结构变化。<br><b>② 三季报的反应方式比数字本身重要。</b>业绩超预期但股价不涨，说明预期已经提前兑现；业绩一般但股价抗跌，说明筹码结构好。<b>看反应，不看数字</b>。<br><b>③ 3900 是收盘站稳还是盘中触及。</b>回踩的深度与承接力度，决定这是有效突破还是假突破。''',
'tip': '''<b>10/26（周一）本周只做三件验证，不做预测</b><br>① <b>量能</b>——统计本周前 3 个交易日成交额，看有没有连续站上 2.2 万亿。没站上就还是存量博弈，别按增量市的思路加仓<br>② <b>三季报反应</b>——重点看「超预期但不涨」和「一般但抗跌」两类，它们比数字本身有信息量<br>③ <b>3900 的收盘价</b>——只看收盘，不看盘中触及。回踩不破才算站稳<br><b>本周不做新开仓决定</b>——月末调仓 + 三季报地雷，等 10/30 收盘后看清再动。这是纪律，不是保守。'''
}

CONTENT['anime'] = {
'summary': '''<b>10月26日（周一）动漫区【秋季新番第 7 周 · 去留已定，进入追更期】</b>——Re:Zero 夺还篇已于 9/30 收官（距今 26 天）。秋季新番开播七周，<b>三集筛选的窗口已经关闭</b>：现在还在追的，基本都是你自己认定值得看的；还在「待看列表」里躺着没动的，大概率不会再看了。<br><br>所以这周该做的不是继续加番，而是<b>把待看列表清一遍</b>——按「三集后仍然想点开」这个标准，一次性处理掉。''',
'trend': '''<b>七周之后，追番的三种状态要分开处理</b><br><br><b>① 在追的（每周固定点开）</b>——保持就好。这时候换番的成本高于收益，因为你对剧情已有沉没投入，中途弃反而浪费。<br><b>② 待看列表里躺了四周以上的</b>——直接删。四周没点开说明你其实不想看，留着只是让列表变长、让「我有 20 部要看」变成压力源。<br><b>③ 想补的完结番</b>——放到周末整块时间，别在工作日碎片时间看。连续剧的体验取决于连贯性。''',
'tip': '''<b>10/26（周一）清一次待看列表（10 分钟）</b><br>① 打开待看列表，按「最后一次点开是几周前」排序<br>② <b>四周以上没点开的，直接删</b>——不是「以后可能看」，是「其实不想看」<br>③ 剩下的按「完结 / 在追」分组：完结的排到周末，在追的保持每周固定<br>④ 秋季番已七周，三集筛选窗口关闭，<b>不再加新番</b><br><b>列表变短不是损失，是减少决策负担</b>——20 部待看带来的焦虑，比错过一部番的成本高得多。'''
}

CONTENT['music'] = {
'summary': '''<b>10月26日（周一）音乐区【10 月最后一周 · 年度歌单初稿定稿期】</b>——10 月只剩 5 天，11 月是年末大赏的集中期（大牌会押后到 11 月发片避开混战）。所以本周是<b>年度歌单初稿的最后调整窗口</b>：再往后，11-12 月的新歌会挤进来，反而不好判断。<br><br>关键方法：<b>按【耐听度】筛，不按【首周热度】筛</b>。热度会骗人，耐听度不会。''',
'trend': '''<b>年度歌单怎么做才不像「随便凑 30 首」</b><br><br><b>① 三轮筛选法。</b>第一轮把今年收藏的全听一遍，删掉「当时觉得好但现在跳过」的；第二轮按月份排序，看哪几个月几乎没有歌——那几个月你其实没在听歌，留着空档比硬凑更诚实；第三轮只留「整张专辑里我会单独找出来听」的。<br><b>② 容量控制在 20-30 首。</b>超过 30 首就不叫歌单，叫流水账。真正的年度歌单应该是「一年后我还能一口气听完」的长度。<br><b>③ 记一句为什么。</b>每首歌旁边写一句你为什么留它（某段通勤 / 某个项目 / 某次旅行），这比歌单本身有价值。''',
'tip': '''<b>10/26（周一）做年度歌单第一轮筛选（30 分钟）</b><br>① 把今年所有收藏的歌拉一个列表，从头过一遍<br>② <b>删掉「当时觉得好，现在会跳过」的</b>——这一条能砍掉一半<br>③ 按月份看空档，哪个季度几乎是空的，就让它空着<br>④ 目标压到 <b>20-30 首</b>，超过就继续删<br>⑤ 留下的每首批注一句「为什么留」<br><b>11 月大牌发片潮之前定稿</b>——再晚就会被新歌冲乱判断。'''
}

CONTENT['novel'] = {
'summary': '''<b>10月26日（周一）网文区【连载第 79 天 · 中段冲突期】</b>——天蚕土豆新书自 8/8 开载，今天已是<b>第 79 天</b>（约两个半月）。这个阶段通常已经完成世界观铺开，进入主线冲突的密集区。<br><br>追更到中段最容易犯的错是<b>把「看得下去」当成「写得好」</b>——中段的连载只要不出大问题都能看下去，但能不能成为好作品，取决于<b>伏笔回收的质量</b>。''',
'trend': '''<b>中段的三个硬指标（比追更爽不爽更重要）</b><br><br><b>① 伏笔回收率。</b>前期埋的线索，进入中段后有没有开始收。只埋不收是烂尾的标准前兆；回收得漂亮，后期口碑会自己涨。<br><b>② 冲突是否升级。</b>好的中段应该是「对手变强 / 代价变高」，而不是「重复同一种打脸」。如果第 79 天和第 40 天的冲突结构一样，说明在拖。<br><b>③ 有没有水字数的章节。</b>连续十章没有推进主线，就是水。可以跳着看，不用为「追更完整」硬啃。''',
'tip': '''<b>10/26（周一）连载第 79 天，做一次中段体检（15 分钟）</b><br>① 数一数：<b>前期埋的重要伏笔，回收了几条</b>？零回收 = 危险信号<br>② 对比现在的冲突和 40 天前：<b>对手变强了吗？代价变高了吗？</b>如果只是换了名字，就是在拖<br>③ 回看最近十章，<b>主线推进了多少</b>？超过十章没推进，可以开始跳着看<br>④ 结论只有两种：<b>继续追</b> 或 <b>放到完结再看</b>——不要「每天点开但不知道在看什么」。'''
}

CONTENT['gaming'] = {
'summary': '''<b>10月26日（周一）游戏区【影之刃零倒计时 3 天】</b>——影之刃零 <b>10/29 发售</b>（预售 268 元起），距今 3 天。这是国产 3A 商业化的关键验证：卖得好会带动更多资本进单机，卖不好说明国内付费习惯仍待培养——<b>这件事的意义超出游戏本身</b>。<br><br>同时 9/15《研究者》STILLTRACE 已发布，克系三连发（沉没之城2 / 命运之门重启 / 诡秘之主）仍在运营中。<b>秋促临近，愿望单该整理了。</b>''',
'trend': '''<b>3 天内要做的两件事，一件关于买，一件关于不买</b><br><br><b>① 关于买：等首周实机，不等首发。</b>3A 大作预购踩雷的成本很高，首周的实机评测（战斗手感、帧数优化、流程长度）比任何宣传片可靠。预售能退款的话风险可控，但仍有时间成本。<br><b>② 关于不买：整理 Steam 愿望单。</b>秋促通常在这段时间或之后启动，愿望单是唯一能让你在打折时不冲动下单的工具——<b>提前把「其实不想要了」的移出去</b>，比打折时省几十块更有效。<br><b>③ 判断标准</b>：一部游戏值不值 268，看「我会不会玩到通关」。玩不到通关的，等它进历史低价。''',
'tip': '''<b>10/26（周一）倒计时 3 天，做两件事</b><br>① <b>愿望单清理</b>——把「加了但已经不想买」的移出去。秋促快到了，留着只会诱发冲动消费<br>② <b>设一个价格提醒</b>——把真正想要的 3-5 款标上心理价位，打折时只看这几个，不看首页推荐<br>③ <b>影之刃零先别预购</b>——10/29 发售后等首周实机评测（重点看战斗手感、帧数、流程长度三项）<br><b>268 元的标准是「能通关」</b>——玩不到通关的，等历史低价。这比抢首发更划算。'''
}

CONTENT['learning'] = {
'summary': '''<b>10月26日（周一）学习重点【10 月只剩 5 天 · 收尾而不是扩张】</b>——本月已过 26 天，剩下 5 天。<b>这个阶段加载新任务的边际收益极低</b>：新东西开了头也做不完，反而会挤占收尾的时间。<br><br>正确做法是<b>把「未完成的」收敛成两种</b>：能在 5 天内做完的，排进日程；做不完的，明确说「推到 11 月」。<b>最怕的是第三种状态——挂在那里，天天想着，但不动。</b>''',
'trend': '''<b>月末收尾的三步，从「清账」开始</b><br><br><b>① 全部列出来，然后只做两分类。</b>5 天内能完成的 → 排进这周的日程；5 天内做不完的 → 明确推到 11 月，并且写一句「为什么推」。中间态（挂着不动）是最大的消耗。<br><b>② 算一次真实完成率。</b>月初定了几个目标？真正完成几个？<b>完成率低于 50% 通常不是懒，是月初定的标准超出实际可投入时间</b>——这个判断比自责有用。<br><b>③ 给 11 月定一个「少而具体」的目标。</b>三个以内，每个都要能一句话说清「做到什么算完成」。''',
'tip': '''<b>10/26（周一）月末清账（20 分钟）</b><br>① 把 10 月所有「开了头 / 想做没做」的事列出来，一条不漏<br>② <b>分成两类</b>：5 天内能完成的（排进本周）／做不完的（明确推到 11 月 + 写一句为什么）<br>③ <b>算完成率</b>：月初定了几个，完成几个。低于 50% 说明标准定高了，不是你不努力<br>④ 给 11 月定 <b>3 个以内</b>的目标，每个都能一句话说清「做到什么算完成」<br><b>这 5 天不加载任何新任务</b>——收尾做干净，比开五个新头有用。'''
}

# ==================================================================
# 执行
# ==================================================================
changed = 0
for key, fields in CONTENT.items():
    for f in ['summary', 'trend', 'tip']:
        if f not in fields:
            raise SystemExit('❌ %s 缺少字段 %s' % (key, f))
        before = src
        src = set_field(src, key, f, fields[f])
        if src != before:
            changed += 1

open(DP, 'w', encoding='utf-8').write(src)
print('✅ 第 1 批完成：%d 个字段已更新（%s）' % (changed, ' / '.join(CONTENT.keys())))
print('   文件长度：%d' % len(src))

# 语法自检
import subprocess
r = subprocess.run(['node', '--check', DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('   语法：' + ('OK' if r.returncode == 0 else 'FAIL ' + (r.stderr or '')[:300]))

# 回读确认
probe = r'''
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),c);
["stock","anime","music","novel","gaming","learning"].forEach(k=>{
  const s=c.INSIGHTS[k];
  const has26 = s.summary.includes("10月26日")||s.summary.includes("10/26")||s.summary.includes("10 月 26");
  console.log("  "+k.padEnd(10)+" summary含10-26="+has26+" tip含="+(s.tip.includes("10/26")||s.tip.includes("10月26日")));
});
'''
open(os.path.join(P, '_probe.js'), 'w', encoding='utf-8').write(probe)
r2 = subprocess.run(['node', os.path.join(P, '_probe.js'), DP], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r2.stdout or r2.stderr)
os.remove(os.path.join(P, '_probe.js'))
