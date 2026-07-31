#!/usr/bin/env python3
"""Generate daily_data.js with today's update."""
import json, os

OUT = r"C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js"

# Build the content as a Python dict first, then convert to JS
# This avoids all the escaping issues

lines = []
lines.append('var SITE_VERSION = "1.1.7";')
lines.append('')
lines.append('var DAILY_DATA = {')
lines.append('  "update_time": "2026-07-31T09:35:00+08:00",')
lines.append('  "update_date": "2026年7月31日",')
lines.append('')
lines.append('  "market_summary": "美股史诗级大反攻：费城半导体暴涨8%终结五连跌 | 微软暴涨15%创史上最大单日市值增幅 | A股七连阳终结创业板跌近4% | 政治局会议定调下半年：发力提效+深化投融资改革 | 美伊冲突升级油价震荡",')
lines.append('')
lines.append('  "news_headlines": [')
lines.append('    {"title": "美股AI史诗级大反攻：微软暴涨15%创单日市值增幅纪录，费城半导体暴涨8%终结五连跌", "url": "https://wallstreetcn.com/", "source": "华尔街见闻", "category": "财经"},')
lines.append('    {"title": "中央政治局会议定调下半年：宏观政策发力提效，首提深化投融资改革提升资本市场韧性", "url": "https://www.cls.cn/", "source": "财联社", "category": "宏观"},')
lines.append('    {"title": "微软Azure增43%全年破千亿 vs Meta FCF骤降91%盘后跌7.8%，AI赚钱与烧钱分水岭定局", "url": "https://wallstreetcn.com/", "source": "华尔街见闻", "category": "财经"},')
lines.append('    {"title": "Anthropic拟融资150亿美元建德州AI数据中心，谷歌提供担保+供应TPU芯片", "url": "https://www.36kr.com/", "source": "36氪", "category": "科技"},')
lines.append('    {"title": "《蜘蛛侠：崭新之日》上映3天票房破4亿，法国西班牙英意均创首日影史纪录", "url": "https://www.cls.cn/", "source": "财联社", "category": "影视"},')
lines.append('    {"title": "三星电机MLCC明日涨价30%+澜起全球首发CXL3.2芯片，A股半导体企稳反弹预期升温", "url": "https://www.cls.cn/", "source": "财联社", "category": "财经"}')
lines.append('  ],')
lines.append('')
lines.append('  "daily_recommendation": {')
lines.append('    "music": {"title": "今日推荐：周深 — 奔腾", "desc": "7月热歌榜第2 · 星河SUMMER音乐节压轴", "link": "https://music.163.com/#/search/m/?s=周深+奔腾"},')
lines.append('    "anime": {"title": "今日补番：BLEACH 千年血战篇-祸进谭-", "desc": "最终章热血追番 · 第2话今日更新", "link": "https://www.bilibili.com/search?keyword=BLEACH+千年血战+祸进谭"},')
lines.append('    "novel": {"title": "今日阅读：剑烛大荒", "desc": "乌贼新书持续霸榜 · 山海经修真世界", "link": "https://www.qidian.com/soushu/剑烛大荒.html"},')
lines.append('    "cocktail": {"title": "今日微醺：莫吉托 Mojito", "desc": "朗姆45ml+青柠+薄荷+苏打水 · 清凉解暑", "link": "https://s.taobao.com/search?q=百加得白朗姆酒"}')
lines.append('  },')
lines.append('')
lines.append('  "weather_summary": "广州 31°C/26°C · 中雷雨局部大雨 · 湿度98% · 雷雨大风黄色预警生效中",')
lines.append('')
lines.append('  "weekly_focus": "📊 周五复盘日 · 本周AI信仰修复：微软Azure破千亿+费城半导体暴涨8%史诗级大反攻",')
lines.append('')
lines.append('  "tip_of_day": "💡 微软vs Meta财报的终极启示：同一夜公布财报，微软暴涨15%（Azure AI+43%→AI赚钱），Meta暴跌7.8%（FCF-91%→AI烧钱）。这不是技术之争，而是AI商业模式之争。微软把AI嵌入现有产品→客户自然增量付费→收入可见；Meta把AI作为成本中心→资本开支吞噬利润→投资者逃离。更深的信号：Anthropic获谷歌担保融资150亿美元建数据中心——AI基础设施军备竞赛仍在加速，但市场只奖励\\"用AI赚钱\\"而非\\"为AI烧钱\\"的企业。对个人而言，AI技能投资也应遵循\\"商业化导向\\"：优先学AI产品化和应用落地，而非纯算法炼丹。",')
lines.append('  movie: {')
lines.append("    summary: '蜘蛛侠崭新之日全球爆炸开局！上映3天内地破4亿，法国/西班牙/英国/意大利均创影史首日纪录。豆瓣7.8分+猫眼9.5分双高口碑，成家班武指+青春版彼得帕克引爆暑期档。复仇者联盟秘密战争持续霸榜，利刃出鞘3豆瓣9.1口碑炸裂。',")
lines.append("    trend: '趋势：超英全面回暖|青春超英崛起|悬疑推理强势|蜘蛛侠3天4亿冲刺16亿预测',")
lines.append("    tip: '首推：蜘蛛侠崭新之日（3天破4亿！成家班武指+青春校园风）。死侍与金刚狼解压、利刃出鞘3推理迷必看。B站搜索蜘蛛侠崭新之日观影评测。',")
lines.append("    reasoning: \"🔍 发生了什么？\\n美股AI史诗级大反攻——费城半导体暴涨8%终结五连跌，微软暴涨15%创史上最大单日市值增幅（+4500亿美元）。闪迪涨26%、美光涨18%、AMD涨13%。A股七连阳终结，创业板跌近4%科创50跌超5%。中央政治局会议定调下半年：发力提效+深化投融资改革。美伊冲突升级：美军空袭伊朗+伊军无人机袭击美军基地。\\n\\n🤔 为什么会爆发史诗级反攻？\\n① 微软财报用数据打破\\\"AI不赚钱\\\"论：Azure AI服务+43%→云收入全年首破千亿→资本开支低于预期→AI投入正在产生回报\\n② 亚马逊盘后+9%助攻：AWS云业务超预期→验证云计算+AI双轮驱动逻辑\\n③ 存储芯片需求暴增：三星利润暴增250倍+美光涨18%+闪迪涨26%→AI存储持续供不应求\\n④ 但Meta FCF-91%是反面教材：AI+元宇宙烧钱→投资者用脚投票→AI赚钱vs AI烧钱分水岭确立\\n\\n📊 术语解释\\n费城半导体指数(SOX)：涵盖30家半导体龙头，是全球芯片行业的风向标，单日涨8%是历史级别波动\\nFCF自由现金流：企业经营现金流减去资本支出，代表真正可自由支配的钱。Meta骤降91%意味着利润被AI资本开支吞噬\\n政治局会议：中共中央政治局定期会议，定调宏观政策方向，本次\\\"发力提效\\\"相比上次\\\"要用好用足\\\"明显升级\\nMLCC涨价30%：三星电机8月1日起多层陶瓷电容涨价→利好风华高科等国产替代龙头\\n\\n💡 对你的启示\\n① AI投资逻辑从\\\"信仰\\\"转向\\\"验证\\\"——微软证明AI能赚钱后暴涨15%，Meta证明AI只烧钱后暴跌7.8%，市场逻辑已根本转变\\n② A股科技股有望超跌反弹——费城半导体暴涨8%+MLCC涨价+政治局会议利好共振，但注意高开后承接力度\\n③ 关注Anthropic 150亿融资——谷歌背书说明AI军备竞赛远未结束，基础设施层投资机会巨大\",")
lines.append("    updated: '2026-07-31'")
lines.append('  }')
lines.append('};')

# Write part 1
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Part 1 written successfully")
