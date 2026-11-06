# -*- coding: utf-8 -*-
"""刷新 DAILY_DATA 里被忽略的 5 个字段（9-10 月陈旧内容）

字段：news_headlines / daily_recommendation / weekly_focus / tip_of_day / movie
原则：不编造具体新闻事件与行情数字，只写可核对的日历事实、已发生事件、判断方法。
news_headlines 的 url 指向站内分区锚点（不再挂 9/11 的旧文章链接）。
"""
import io, sys, os, re, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(r'C:\Users\ZR\Desktop\钟锐的个人网站')

TODAY = '2026-11-06'
D = '11月6日（周五）'


def find_block(t, key, open_ch='{'):
    m = re.search(r'(?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*' + re.escape(open_ch), t)
    if not m:
        return None, None
    i = t.index(open_ch, m.start())
    close_ch = '}' if open_ch == '{' else ']'
    depth = 0
    instr = None
    j = i
    while j < len(t):
        c = t[j]
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


t = open('daily_data.js', encoding='utf-8').read()
orig = len(t)

# ---------- 1) news_headlines ----------
NEWS = [
  {"title": "三季报 10/31 已全部披露完毕 · A 股进入业绩空窗期（持续到明年 1 月）",
   "url": "#stock", "source": "本期观察", "category": "财经"},
  {"title": "AI 行业重心转向 Agent 工程化：失败重试 / 人工介入点 / 成本上限 / 输出验收",
   "url": "#ai-track", "source": "本期观察", "category": "科技"},
  {"title": "影之刃零 10/29 已发售 · 国产 3A 进入首周验证期（帧数 / 手感 / 主线时长）",
   "url": "#gaming", "source": "本期观察", "category": "文娱"},
  {"title": "11 月首个完整交易周（11/2-11/6）收官 · 空窗期看资金不看业绩",
   "url": "#stock", "source": "本期观察", "category": "财经"},
  {"title": "秋招进入尾声：该统计反馈率与面试转化率，而不是继续海投",
   "url": "#career", "source": "本期观察", "category": "求职"},
]
s, e = find_block(t, 'news_headlines', '[')
if s is None:
    print('❌ 找不到 news_headlines')
    sys.exit(1)
t = t[:s] + json.dumps(NEWS, ensure_ascii=False, indent=2) + t[e:]
print('✅ news_headlines：5 条（旧的是 9/11 链接，已换为站内锚点 + 当日观察）')

# ---------- 2) daily_recommendation ----------
REC = {
  "music": {"title": "年末发片季 · 先建「待听」清单 🎵",
            "desc": "11-12 月专辑集中释放 · 只记艺人名不记歌名 · 12 月按名单逐个过",
            "link": "https://music.163.com/"},
  "anime": {"title": "十月新番过半 · 弃番决策点 🎬",
            "desc": "第 5-6 集看制作是否回落 · 剧情或作画任一低于 3/5 先搁置",
            "link": "https://www.bilibili.com/"},
  "novel": {"title": "中段抽检：翻到中间读三章 📖",
            "desc": "三章能任意互换位置 = 已进入注水段 · 断舍离比硬追省时间",
            "link": "https://www.qidian.com/"},
  "cocktail": {"title": "入冬轻饮：热托蒂 🍸",
               "desc": "威士忌+蜂蜜+柠檬+热水 · 低温夜晚比冰饮更合适",
               "link": "https://s.taobao.com/search?q=威士忌"},
}
s, e = find_block(t, 'daily_recommendation', '{')
t = t[:s] + json.dumps(REC, ensure_ascii=False, indent=2) + t[e:]
print('✅ daily_recommendation：4 项（原为 9 月追番/单曲）')

# ---------- 3) weekly_focus ----------
NEW_WF = ('11 月第一周（11/2-11/6）· 三季报 10/31 已全部截止，A 股进入【业绩空窗期】（持续到明年 1 月）'
          '→ 判断依据从【看业绩】切换为【看资金是否连续净流入】：连续 3 天才算，单日放量不算 '
          '→ 影之刃零 10/29 已发售，进入首周验证期（帧数 / 手感 / 主线时长三项）'
          '→ AI 行业讨论重心从「模型能力」转向「Agent 工程化」：失败重试、人工介入点、成本上限、输出验收 '
          '→ 入冬后第一优先事项是室内湿度 40-60%，不是温度 '
          '→ 秋招进入尾声：该统计反馈率与面试转化率，而不是继续海投')
m = re.search(r'(["\']?weekly_focus["\']?\s*:\s*)(["\'])(?:\\.|(?!\2).)*\2', t)
if m:
    t = t[:m.start()] + m.group(1) + json.dumps(NEW_WF, ensure_ascii=False) + t[m.end():]
    print('✅ weekly_focus 已换（原为「9月第一周」）')
else:
    print('⚠️ weekly_focus 未匹配')

# ---------- 4) tip_of_day ----------
NEW_TIP = (D + ' 三件事：'
  '(1)【业绩空窗期开始】三季报 10/31 已披露完，到明年 1 月没有财报催化——把自选股按「已披露 / 未披露」分类，'
  '空窗期只留已披露的，规避黑天鹅；'
  '(2)【空窗期看资金不看业绩】单日放量常是事件驱动，连续 3 天净流入才是资金进场——别用增量市的思路加仓；'
  '(3)【秋招收尾】11 月该做的不是继续海投，而是统计反馈率与面试转化率，把投递量换成命中率')
m = re.search(r'(["\']?tip_of_day["\']?\s*:\s*)(["\'])(?:\\.|(?!\2).)*\2', t)
if m:
    t = t[:m.start()] + m.group(1) + json.dumps(NEW_TIP, ensure_ascii=False) + t[m.end():]
    print('✅ tip_of_day 已换（原为「9月6日周日五重叙事」）')
else:
    print('⚠️ tip_of_day 未匹配')

# ---------- 5) movie ----------
MOVIE = {
  "summary": ("<b>" + D + "电影市场【颁奖季前哨 · 冲奥片窗口】</b>——11 月到 12 月是冲奥片集中上映的窗口，"
    "这类片子的特点是<b>作者表达强、节奏偏慢</b>，用「好不好看」评价容易误判。<br><br>"
    "更有效的筛选标准是<b>「值不值得进影院」</b>：只有三类值得——① 视听设计是核心卖点 ② 有剧透风险 ③ 需要大银幕沉浸。"
    "其余等流媒体即可。<br><br>另一个观察点是<b>口碑扩散曲线</b>而不是首周票房：近年中等成本类型片（惊悚 / 剧情 / 恐怖）"
    "回报率高于超英大片，原因是观众对视觉奇观的边际效用下降，对故事本身的需求回升。"),
  "trend": ("颁奖季窗口开启|冲奥片作者表达强、节奏偏慢|中等成本类型片回报率高于超英|"
    "口碑扩散曲线比首周票房有信息量|11-12 月大片挤压排片|用「值不值得进影院」筛片"),
  "tip": (D + " 观影策略：① 把【必去影院】标准写死——只有视听设计是核心卖点、有剧透风险、需大银幕沉浸三类，"
    "其余等流媒体；② 选片看上映两周后的口碑，不看首周（首周受营销影响大）；"
    "③ 颁奖季片子节奏偏慢，用「值不值得进影院」而不是「好不好看」来筛，避免误判。"),
  "reasoning": ("🔍 发生了什么？\n"
    "11 月到 12 月是冲奥片集中上映的窗口，作者表达强、节奏偏慢；同期中等成本类型片的回报率高于超英大片。\n\n"
    "🤔 为什么重要？\n"
    "① 颁奖季片子的评价维度与商业片不同——用「好看」评价会误判\n"
    "② 观众对视觉奇观的边际效用下降，故事本身的需求回升，这改变了选片与投资逻辑\n"
    "③ 首周票房受营销影响大，两周后的口碑扩散曲线更接近真实\n\n"
    "📊 术语解释\n"
    "颁奖季：年末到次年初的评奖窗口，冲奥片集中上映\n"
    "口碑扩散曲线：评分与讨论量随时间的变化，比首周票房更能反映真实接受度\n"
    "边际效用：每多消费一单位带来的额外满足感——奇观看多了，增益递减\n\n"
    "💡 启示\n"
    "① 把标准从「好不好看」换成「值不值得进影院」，决策立刻清晰\n"
    "② 内容判断看扩散曲线而不是首周数据，这个逻辑同样适用于产品上线后的留存"),
  "updated": TODAY,
}
s, e = find_block(t, 'movie', '{')
t = t[:s] + json.dumps(MOVIE, ensure_ascii=False, indent=2) + t[e:]
print('✅ DAILY_DATA.movie：summary/trend/tip/reasoning 全部换成 11/06 版')

# ---------- 6) 修最后一个 PICKS desc ----------
old = '"用GPT-6 Astra发布写300字行业观察《AI安全与能力如何平衡》 · 面试加分"'
new = '"训练平台 = 可打开的产品 · 写清它解决了什么问题、有哪些约束 · 比行业观察更能证明落地"'
if old in t:
    t = t.replace(old, new, 1)
    print('✅ PICKS 最后一张卡 desc 已修')
else:
    m2 = re.search(r'"用GPT-6 Astra发布写300字行业观察[^"]*"', t)
    if m2:
        t = t.replace(m2.group(0), new, 1)
        print('✅ PICKS 最后一张卡 desc 已修（正则）')
    else:
        print('⚠️ 未找到该 desc')

open('daily_data.js', 'w', encoding='utf-8').write(t)
print('\n文件：%d → %d 字节' % (orig, len(t)))
