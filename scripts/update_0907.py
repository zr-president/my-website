# -*- coding: utf-8 -*-
"""2026-09-07 每日更新（周一）——更新 DAILY_DATA 头部 + DAILY_BRIEFING 8卡 + MARKET_SENTIMENT"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

def esc(v):
    return v.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")

def abs_replace(start_marker, end_marker, new_block, label):
    global c
    i = c.find(start_marker)
    if i < 0:
        print('MISS start:', label); return False
    j = c.find(end_marker, i) + len(end_marker) if end_marker else len(c)
    # 吞掉块后连续空白/逗号前的部分——这里用精确 end_marker
    c = c[:i] + new_block + c[j:]
    print('OK', label)
    return True

# ---------- 1) DAILY_DATA 头部 ----------
# update_time / update_date / market_summary / news_headlines / tip_of_day / weekly_focus / weather_summary
c = c.replace('"update_time": "2026-09-06T11:45:00+08:00"', '"update_time": "2026-09-07T18:55:00+08:00"')
c = c.replace('"update_date": "2026年9月6日"', '"update_date": "2026年9月7日"')

# market_summary
old_ms = re.search(r'"market_summary": "([^"]*)"', c)
new_ms = ('"market_summary": "周一(9/7)A股三大指数分化·创业板指大涨：沪指+0.07%收3932.7·深成指+1.91%收13774.91·创业板指+3.41%收3398.68·科创综指+1.9%收1900.89｜两市成交1.96万亿(较前缩量868亿)·算力硬件走强：CPO/元件/光通信模块领涨·天通/共进/剑桥科技涨停｜贵金属/保险/煤炭领跌·沪指窄幅震荡守3930｜早盘CPO概念+粮食概念领涨·赚钱效应在创业板科技成长 ｜ GPT-6 Astra发布后算力硬件链情绪传导兑现 ｜ 北京AI产投基金入股3D算力芯片商算苗科技"')
c = c.replace(old_ms.group(0), new_ms, 1)

# news_headlines（5条 9/7）
old_nh = re.search(r'"news_headlines": \[[\s\S]*?\n  \],', c)
new_nh = '''"news_headlines": [
    {"title": "A股9/7周一：创业板指大涨3.41%·算力硬件走强·CPO/元件/光通信领涨·沪指+0.07%守3930", "url": "https://www.cnfin.com/gs-lb/detail/20260907/4466141_1.html", "source": "新华财经/中国金融信息网", "category": "财经"},
    {"title": "GPT-6开启新叙事：Coding之后，比长程任务执行——模型竞争从聊天/写代码转向端到端Agent与Computer Use", "url": "https://m.thepaper.cn/newsDetail_forward_34013011", "source": "澎湃/明亮公司", "category": "科技"},
    {"title": "《哪吒之魔童闹海》获第38届大众电影百花奖最佳影片奖", "url": "https://sdxw.iqilu.com/w/article/YS0yMS0xNzM0NDM3Mg.html", "source": "齐鲁网", "category": "文娱"},
    {"title": "北京AI产投基金入股3D算力芯片研发商算苗科技·注册资本增至134.96万元", "url": "https://www.cnfin.com/gs-lb/detail/20260907/4466141_1.html", "source": "新华财经", "category": "科技"},
    {"title": "市场监管总局公布第二批经营者集中反垄断审查典型案例(港口/药品/光伏)", "url": "https://www.cnfin.com/gs-lb/detail/20260907/4466141_1.html", "source": "新华社", "category": "财经"}
  ],'''
c = c.replace(old_nh.group(0), new_nh, 1)

# weather_summary（延续，天气略有变化）
c = c.replace('"weather_summary": "广州 33C/25C · 多云到晴为主', '"weather_summary": "广州 33C/25C · 多云到晴为主')

# ---------- 2) DAILY_BRIEFING 8卡（9/7周一版：GPT-6新叙事/A股大涨/算力硬件/哪吒百花奖） ----------
old_brief = re.search(r'var DAILY_BRIEFING = \{.*?\n\};', c, re.S)
new_brief = '''var DAILY_BRIEFING = {
  date: "2026-09-07",
  highlights: [
    {priority:1, icon:"🖥️", section:"GPT-6新叙事", headline:"GPT-6开启新叙事：Coding之后，比长程任务执行——模型竞争转向端到端Agent与Computer Use", summary:"9月3日 OpenAI 发布 GPT-6 Astra，被称『最智能最对齐』旗舰。核心转变：模型竞争从聊天/写代码转向 Computer Use（电脑操作）与长程 Agent——『任何你能在电脑上完成的事，Astra都替你完成』。用10万卡训练(Stargate德州站)、采用Recurrent Depth架构(层重复用/隐空间推理)、API价每百万输入$10输出$50(比5.6Sol贵约2.5倍)。市场反响强烈，发布9小时浏览量3600万，为OpenAI自Sora以来之最。对国产模型：差距主要在长程任务/Computer Use执行层。", action:"深度解读", link:"#ai-track", deepLink:"https://m.thepaper.cn/newsDetail_forward_34013011"},
    {priority:2, icon:"📈", section:"A股算力爆发", headline:"A股9/7周一：创业板指大涨3.41%·算力硬件走强·CPO/光通信领涨·沪指+0.07%守3930", summary:"9月7日（周一）A股三大指数分化：创业板指大涨3.41%收3398.68、深成指+1.91%收13774.91、沪指+0.07%收3932.7（窄幅震荡）、科创综指+1.9%收1900.89。两市成交1.96万亿（较前缩量868亿）。算力硬件全面走强：CPO概念/元件/光通信模块领涨，天通股份/共进股份/剑桥科技涨停；贵金属/保险/煤炭领跌。GPT-6 Astra发布后算力硬件链情绪兑现，赚钱效应集中在创业板科技成长。", action:"深度分析", link:"#stock", deepLink:"https://www.cnfin.com/gs-lb/detail/20260907/4466141_1.html"},
    {priority:3, icon:"🎬", section:"哪吒百花奖", headline:"《哪吒之魔童闹海》获第38届大众电影百花奖最佳影片奖", summary:"《哪吒之魔童闹海》荣获第38届大众电影百花奖最佳影片奖——国产动画再获主流奖项认可。这是继暑期档《功夫女足》《八仙！》后，国产内容品质持续获得行业奖项背书。当前电影市场：龙餐馆破20亿(年榜第三)、功夫女足22.69亿、八仙14.59亿动画冠军——内容大盘热度延续，国庆档预热在即。", action:"查看票房", link:"#movie", deepLink:"https://sdxw.iqilu.com/w/article/YS0yMS0xNzM0NDM3Mg.html"},
    {priority:4, icon:"💼", section:"AI岗位窗口", headline:"GPT-6发布催化AI岗位热度：长程Agent/Computer Use成新方向·金九银十投递窗口", summary:"GPT-6 Astra 主打长程Agent与Computer Use，AI岗位叙事从『会AI』升级为『能用AI完成复杂任务』。求职信号：①AI应用/Agent产品岗位需求上升（能讲清长程任务/自动化价值）；②『AI安全/AI治理』(安全监控/可解释性)成新话题；③金九银十窗口：9月秋招+社招双高峰，今日周一9:30-11:00黄金投递窗口照常。把GPT-6新叙事写进行业观察（端到端Agent/Computer Use价值）。", action:"准备投递", link:"#career", deepLink:"https://www.zhipin.com/"},
    {priority:5, icon:"🏦", section:"算力国产化", headline:"北京AI产投基金入股3D算力芯片商算苗科技·AI算力国产链持续加码", summary:"北京人工智能产业投资基金入股3D算力芯片研发商算苗科技，注册资本增至134.96万元——地方AI算力基金持续加码国产算力芯片。叠加GPT-6用10万卡训练强化算力长期需求逻辑，A股算力硬件(CPO/光模块/芯片)情绪传导明确。机构观点：FAU/无源光器件在CPO产业化下价值量膨胀；半导体设备国产替代关注量测/探针台等高弹性环节。", action:"了解算力链", link:"#ai-track", deepLink:"https://www.cnfin.com/gs-lb/detail/20260907/4466141_1.html"},
    {priority:6, icon:"🎮", section:"游戏预售", headline:"《影之刃零》预售中：甄子丹动作监制·国产3A商业化验证·10/29发售", summary:"《影之刃零》预售持续（268元起，10/29发售）——甄子丹出任动作监制，虚幻5暗黑武侠3A。继《黑神话：悟空》后国产3A商业化验证：预售数据=市场信心试金石。Steam愿望单可退、发售前关注实机评测；秋促/国庆/双11三连促临近，补票最佳窗口。", action:"查看预售", link:"#gaming", deepLink:"https://store.steampowered.com/app/2776930/"},
    {priority:7, icon:"🎬", section:"动漫完结倒计时", headline:"Re:Zero第四季【夺还篇】追番第25天·最终话9/30定档·完结倒计时24天", summary:"Re:Zero S4 夺还篇追番第25天（8/12开播），最终话9/30定档、还剩24天——486 在丧失记忆后的自我认知博弈进收束阶段。同步追更：BLEACH千年血战篇-祸进谭、无职转生S3、False Memory、时光代理人S3；10月秋季新番档期临近，可提前加追番单。", action:"去追番", link:"#anime", deepLink:"https://www.bilibili.com/search?keyword=Re%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E5%BC%82%E4%B8%96%E7%95%8C%E7%94%9F%E6%B4%BB"},
    {priority:8, icon:"⛅", section:"秋高气爽", headline:"台风科罗旺远离·新台风『杜鹃』或将生成——广东秋高气爽还能维持几天", summary:"深圳台风预警解除，科罗旺已拐弯远离广东，但新台风『杜鹃』或将生成（路径待观察）。广东近期多云到晴、气温回升，秋高气爽延续——但昼夜温差渐大。广州未来几天多云到晴为主（33C/25C）。本周出行宜早不宜晚，沿海留意『杜鹃』路径。", action:"查天气", link:"#life-tips", deepLink:"https://news.qq.com/rain/a/20260905A09Y9U00"}
  ]
};'''
c = c.replace(old_brief.group(0), new_brief, 1)

# ---------- 3) MARKET_SENTIMENT ----------
old_ms2 = re.search(r'var MARKET_SENTIMENT = \{.*?\n\};', c, re.S)
new_ms2 = '''var MARKET_SENTIMENT = {
  updated: "2026-09-07",
  items: [
    {label:"沪指", value:"3932.7", color:"#dc2626", note:"9/7收+0.07%·窄幅震荡守3930"},
    {label:"创业板", value:"+3.41%", color:"#059669", note:"9/7领涨3398.68·算力/科技成长强"},
    {label:"深成指", value:"+1.91%", color:"#059669", note:"9/7收13774.91"},
    {label:"强势板块", value:"算力硬件", color:"#059669", note:"CPO/元件/光通信领涨·天通/共进/剑桥涨停"}
  ]
};'''
c = c.replace(old_ms2.group(0), new_ms2, 1)

open(FP, 'w', encoding='utf-8').write(c)
print('DAILY_DATA + BRIEFING + SENTIMENT done')
