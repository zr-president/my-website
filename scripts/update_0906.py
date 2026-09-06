# -*- coding: utf-8 -*-
"""2026-09-06 每日更新脚本（一次性·9/4-9/6 积压事件）"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
content = open(FP, 'r', encoding='utf-8').read()
changed = []

def balanced_block(text, start):
    """从 start(指向某 key 的对象起点) 找配平大括号，字符串感知。"""
    i = text.find('{', start)
    j = i; depth = 0; L = len(text)
    while j < L:
        ch = text[j]
        if ch in ("'", '"'):
            q = ch; j += 1
            while j < L:
                if text[j] == '\\': j += 2; continue
                if text[j] == q: break
                j += 1
        elif ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    return text[start:j+1]

def replace_section(key, new_text):
    global content
    m = re.search(r'(?m)^  ' + re.escape(key) + r':\s*\{', content)
    if not m:
        print('MISS section:', key); return False
    block = balanced_block(content, m.start())
    start = m.start()
    end = start + len(block)
    # 吞掉块后的所有连续逗号（历史残留可能累积多个），避免 ',,' 与 ',,,'
    while end < len(content) and content[end] == ',':
        end += 1
    consumed = content[start:end]
    content = content.replace(consumed, new_text, 1)
    changed.append(key)
    print('OK section:', key)
    return True

# ---------- 1) DAILY_BRIEFING highlights ----------
old_brief = re.search(r'var DAILY_BRIEFING = \{.*?\n\};', content, re.S)
assert old_brief, 'briefing not found'
brief_block = old_brief.group(0)
new_brief = '''var DAILY_BRIEFING = {
  date: "2026-09-06",
  highlights: [
    {priority:1, icon:"🤖", section:"GPT-6 Astra发布", headline:"OpenAI 9/4正式发布GPT-6 Astra：总裁称『AGI时代已到来』·从8月安全暂停到正式发布的大反转", summary:"9月4日 OpenAI 正式发布 GPT-6 Astra——公司总裁公开称『AGI 时代已经到来』，被广泛评价为史上最强模型。戏剧性的是：8月初 OpenAI 曾因网络安全风险（Astra 内部评估达到『关键资安能力』等级、可自主策划网络攻击）主动暂停其研发，仅一个月后便正式发布——引发『AI 安全治理 vs 能力释放如何平衡』的全球大讨论。随发布同期的行业动作：国家人工智能基金向可灵注资14亿元、阿里更新 Qwen3.8-Max、Manus 恢复独立运营——中国 AI 资本与产品双热。", action:"深度解读", link:"#ai-track", deepLink:"https://m.163.com/dy/article/L5VO59KJ0534A4SC.html"},
    {priority:2, icon:"📉", section:"A股9月开局偏弱", headline:"A股9/4高开低走：沪指-0.30%收3930.12·日K连三黑·科创50跌2.1%·农业逆市上涨", summary:"9月4日（周五）A股三大指数高开低走：沪指跌0.30%收3930.12、日 K 线连三黑（9/2 起连续回落），科创50跌2.1%领跌，高位人气股集体调整。盘面亮点：农业板块逆市上涨（粮食股延续强势，防御属性获认可）。9 月开局整体偏弱——沪指从 3950 上方回落至 3930 一线，年线攻防持续、量能萎缩、观望情绪浓。下一交易日 9/8（周一）关注：①3930 能否企稳 ②农业/红利防御主线延续性 ③GPT-6 Astra 发布对 AI 算力/应用板块的情绪传导。", action:"深度分析", link:"#stock", deepLink:"https://www.eastmoney.com/"},
    {priority:3, icon:"🎬", section:"龙餐馆破20亿", headline:"《欢迎来龙餐馆》累计破20亿：2026第四部20亿+影片·超《给阿嬷的情书》居年票房榜第三", summary:"《欢迎来龙餐馆》累计票房突破20亿元——成为2026年第四部破20亿的影片，并超越《给阿嬷的情书》升至年度票房榜第三。沈腾×文牧野转型之作豆瓣8.4的口碑长尾持续兑现。目前年榜前列：《功夫女足》22.69亿、《八仙！》14.59亿动画冠军、龙餐馆20亿。9 月新片持续定档 + 国庆档预热临近，内容大盘热度延续。", action:"查看票房", link:"#movie", deepLink:"https://piaofang.maoyan.com/"},
    {priority:4, icon:"⛈️", section:"新台风或将生成", headline:"台风科罗旺拐弯·新台风『杜鹃』或将生成——广东秋高气爽还能维持几天", summary:"台风动态：『科罗旺』已拐弯远离广东，但新台风『杜鹃』或将生成（路径待观察）。广东近期转为多云到晴、气温回升，迎来难得的『秋高气爽』——但昼夜温差渐大，且新台风消息需持续跟进。广州未来几天多云到晴为主（33C/25C 左右），周末出行宜早不宜晚。若『杜鹃』生成并靠近，沿海地区需留意风雨影响。", action:"查看天气", link:"#life-tips", deepLink:"https://news.qq.com/rain/a/20260905A09Y9U00"},
    {priority:5, icon:"🏦", section:"国产AI资本+产品双热", headline:"国家AI基金注资可灵14亿·阿里更新Qwen3.8-Max·Manus恢复独立运营——中国AI进入资本+产品共振期", summary:"中国 AI 行业资本与产品双热：①国家人工智能基金向快手可灵注资14亿元（AI 视频生成国家队入场）；②阿里更新旗舰模型 Qwen3.8-Max；③AI 智能体产品 Manus 恢复独立运营。叠加 GPT-6 Astra 发布带动全球关注，国产 AI 生态（模型/视频/Agent）持续扩容。对求职信号：AI 应用层与产品化人才需求进入金九银十放量期。", action:"了解详情", link:"#ai-track", deepLink:"https://www.tmtpost.com/index.php/8129653.html"},
    {priority:6, icon:"💼", section:"金九银十求职窗口", headline:"9月秋招+社招双高峰：GPT-6发布催化AI岗位热度·周一黄金窗口照常", summary:"金九银十招聘季进行中：9月是秋招（2027届）+社招双高峰，GPT-6 Astra 发布进一步催化 AI 岗位热度（AI 产品/运营/Agent 应用岗需求上升）。周末建议：①把 GPT-6 Astra 事件写成 300 字行业观察（安全治理 vs 能力释放，面试必考题）；②复盘本周投递进度；③更新简历技能栏（补『了解 GPT-6 Astra 与 AI 安全治理』）；④周一 9:30-11:00 黄金窗口集中投递。", action:"准备投递", link:"#career", deepLink:"https://www.zhipin.com/"}
  ]
};'''
content = content.replace(brief_block, new_brief, 1)
changed.append('DAILY_BRIEFING')
print('OK briefing')

# ---------- 2) INSIGHTS 核心板块 ----------
def sec_obj(key, verdict=None, summary='', trend='', tip='', reasoning=''):
    def esc(v):
        return v.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")
    lines = ['  ' + key + ': {']
    if verdict: lines.append("    verdict: '" + esc(verdict) + "',")
    for k, v in [('summary', summary), ('trend', trend), ('tip', tip), ('reasoning', reasoning)]:
        if v: lines.append("    " + k + ": '" + esc(v) + "',")
    lines.append("    updated: '2026-09-06'")
    lines.append('  },')
    return '\n'.join(lines)

replace_section('stock', sec_obj('stock',
 verdict='🎯 今日结论（小白版）：① 9月开局偏弱——9/4沪指-0.30%收3930.12、日K连三黑、科创50跌2.1%，从9月初的3950上方回落，高位人气股调整；② 农业逆市上涨=资金转防御，观望情绪浓；③ 周末重磅：GPT-6 Astra发布（总裁称AGI时代到来）→周一(9/8)AI算力/应用板块或有情绪刺激，但A股AI硬件前期已调整需看资金认不认；④ 小白该不该动：不追高不恐慌，3930企稳再谈加仓，农业/红利防御仓可留；⑤ 仓位维持，等周一量能信号。',
 summary='9月4日（周五）A股三大指数高开低走：沪指-0.30%收3930.12、日K连三黑（9/2起连续回落），科创50跌2.1%领跌，高位人气股集体调整。农业板块逆市上涨（粮食股延续强势）。9月开局整体偏弱：沪指从3950上方回落至3930一线，年线攻防持续、量能萎缩、观望情绪浓。周末催化：OpenAI 9/4发布GPT-6 Astra（总裁称AGI时代到来）→下周一(9/8)A股AI算力/应用板块或有情绪传导。',
 trend='（9/4收盘复盘·周末展望）今日核心叙事：【9月开局偏弱+资金转防御+GPT-6外部催化】。(1)**日K连三黑**——沪指从3950上方回落至3930一线，9月开局低于预期→高位人气股调整、量能萎缩=存量博弈下资金在撤高就低；(2)**农业逆市**——粮食股延续强势=防御属性获认可→市场风险偏好下降的信号；(3)**GPT-6 Astra周末重磅**——OpenAI正式发布且称AGI时代到来→周一关注A股AI算力(光模块/PCB/服务器)与AI应用(传媒/游戏/办公)板块情绪，但前期调整后需看资金是否买账；(4)**下周一(9/8)关键位**——3930能否企稳(守住则震荡筑底，失守则看3900关口)。操作：不追高不恐慌，农业/红利防御仓可留，AI算力等回调企稳再分批。',
 tip='周末+周一(9/8)操作预案：(1)**周末功课**——把 GPT-6 Astra 发布对 A股 AI 板块的传导写进笔记：AI硬件(算力)与AI应用谁更受益，周一开盘验证；(2)**周一关注**——①沪指3930能否守住(关键支撑)；②AI板块高开幅度与承接(高开低走则说明资金不信、别追)；③农业/粮食防御主线是否延续；(3)**仓位**——震荡期≤5成，防御(农业/红利)与进攻(AI回调后)搭配；(4)**定投**——沪深300/科创50定投照常，3900-3930区间是分批摊低成本区域；(5)**求职联动**——GPT-6发布催化AI岗位热度，周一9:30-11:00黄金窗口照常投递。',
 reasoning='🔍 发生了什么？\n9/4沪指-0.30%收3930.12、日K连三黑，科创50跌2.1%领跌，农业逆市上涨。周末OpenAI发布GPT-6 Astra。\n\n🤔 市场逻辑发生了什么变化？\n① 9月开局偏弱=8月反弹后的连续消化——高位人气股调整+量能萎缩=资金风险偏好下降\n② 农业逆市=防御切换——涨的是粮食(避险属性)而非成长，说明进攻意愿不足\n③ GPT-6 Astra=外部新催化——但AI硬件前期已连续调整，周一需要资金重新认可\n\n📊 术语解释\n日K连三黑：连续三根阴线——短期趋势转弱的信号，需等止跌确认\n防御切换：资金从高弹性成长转向低波动(农业/红利)——市场风险偏好处在低位\n情绪传导：海外重大科技事件→A股相关板块开盘反应——高开≠能持续，看承接\n\n💡 对你的启示\n① 震荡期：不追高不恐慌，等3930企稳/放量信号\n② 定投区间：3900-3930分批摊成本是好节奏\n③ GPT-6发布=AI主题催化剂——但A股表现看资金，别只看消息\n④ 周一黄金窗口照常投递，把GPT-6写进行业观察'))

replace_section('"ai-track"', sec_obj('"ai-track"',
 verdict='🎯 今日结论：① 头条是【GPT-6 Astra正式发布】——OpenAI总裁称『AGI时代到来』，从8月安全暂停到9/4发布的大反转→理解『AI安全治理 vs 能力释放』的平衡是当下最热面试题；② 国产侧：国家AI基金注资可灵14亿+阿里更新Qwen3.8-Max+Manus恢复独立运营——中国AI资本+产品双热；③ 对工具链：GPT-6 Astra能力未开源，DeepSeek/Qwen/GLM开源阵营短期不受冲击，本地部署路线不变；④ 行动：把GPT-6 Astra写进行业观察+准备AI安全治理的面试回答。',
 summary='9月6日 AI 行业焦点：(1)【OpenAI发布GPT-6 Astra】(9/4)——总裁称『AGI时代已到来』，被评史上最强；8月初曾因网络安全风险(可自主策划网络攻击的『关键资安能力』)暂停研发，一个月后正式发布——AI安全治理与能力释放的博弈成全球焦点；(2)【国产AI资本+产品双热】——国家人工智能基金向可灵注资14亿元、阿里更新Qwen3.8-Max、Manus恢复独立运营；(3)【Anthropic 350亿算力协议】持续发酵；(4)【科大讯飞端侧模型】9/1开源后生态落地推进。',
 trend='9月AI五大趋势线：(1)**GPT-6 Astra=AI能力上限刷新**——从暂停到发布的反转，说明前沿实验室在安全评估后选择放行→『能造什么』与『该造什么』的边界仍在动态调整；(2)**AI安全治理成显学**——Astra事件让安全评估/红队测试/关键资安能力成为行业与求职高频词→AI安全产品经理/AI治理岗需求上升；(3)**中国AI资本+产品共振**——国家基金注资可灵(视频生成)、Qwen3.8-Max更新、Manus独立→国产AI从模型军备进入应用商业化；(4)**开源阵营不受冲击**——GPT-6闭源，DeepSeek/Qwen/GLM的开源+本地部署路线依然是工具链主力；(5)**算力军备延续**——Anthropic 350亿协议+英伟达指引，AI资本开支周期未见顶。',
 tip='今日追踪建议（按优先级）：(1)**30秒讲清GPT-6 Astra**——8月暂停(安全)→9/4发布(总裁称AGI时代)→理解安全评估机制与能力释放的权衡→写进简历『了解GPT-6 Astra与AI安全治理』；(2)**读可灵注资/Manus独立**——国产AI商业化案例→面试谈资+1；(3)**写300字行业观察**——主题《GPT-6 Astra发布：AI安全与能力如何平衡》→本周作品集；(4)**工具链无变化**——GPT-6闭源，日常仍用DeepSeek/Qwen/GLM+本地部署，无需切换；(5)**求职联动**——AI安全/AI治理/AI产品岗是GPT-6催化后的新增量方向。'))

replace_section('news', sec_obj('news',
 verdict='🎯 今日新闻结论：① OpenAI发布GPT-6 Astra（总裁称AGI时代到来）——全球AI里程碑，从8月安全暂停到9/4发布的大反转，『AI安全vs能力释放』成焦点；② A股9月开局偏弱（9/4沪指3930.12·日K连三黑）——农业防御、观望情绪浓，等周一企稳信号；③ 龙餐馆累计破20亿居年票房第三——内容消费韧性；④ 新台风杜鹃或将生成——广东秋高气爽进入倒计时；⑤ 金九银十招聘季+GPT-6催化——AI岗位热度上升，周一黄金窗口照常。',
 summary='1. OpenAI 9/4正式发布GPT-6 Astra：总裁称『AGI时代已到来』——8月因安全暂停研发到正式发布的大反转，AI安全治理成全球焦点。2. A股9/4高开低走：沪指-0.30%收3930.12·日K连三黑·科创50跌2.1%·农业逆市上涨·9月开局偏弱。3. 《欢迎来龙餐馆》累计破20亿：2026第四部20亿+影片·居年票房榜第三。4. 国家AI基金注资可灵14亿元+阿里更新Qwen3.8-Max+Manus恢复独立运营——国产AI资本产品双热。5. 台风科罗旺拐弯·新台风『杜鹃』或将生成——广东秋高气爽进入倒计时。6. 金九银十招聘季：GPT-6催化AI岗位热度。7. Re:Zero夺还篇追番第25天·9/30完结。',
 trend='今日核心叙事：GPT-6 Astra发布+A股9月开局偏弱+国产AI双热。(1)**GPT-6 Astra=AI里程碑**——总裁称AGI时代到来，从安全暂停到发布的反转→『该造什么』的全球讨论进入新阶段；(2)**A股9月偏弱**——日K连三黑、农业防御、观望浓→等周一3930企稳与GPT-6对AI板块的情绪传导；(3)**国产AI资本+产品共振**——可灵14亿/Manus独立/Qwen更新→中国AI进入商业化放量；(4)**内容大盘强**——龙餐馆破20亿年榜第三→国庆档预热在即；(5)**天气**——新台风杜鹃或将生成，广东秋高气爽倒计时。',
 tip='五条今日必读：(1)GPT-6 Astra发布解读——安全暂停→正式发布的大反转，理解『AI安全vs能力释放』(面试必考)；(2)A股9/4收盘复盘——3930一线防守，农业防御，等周一量能与GPT-6情绪传导；(3)龙餐馆破20亿——内容消费韧性，国庆档预热；(4)新台风杜鹃——广东秋高气爽进入倒计时，出行关注；(5)金九银十+GPT-6——AI岗位热度上升，周一黄金窗口照常投递。'))

replace_section('career', sec_obj('career',
 verdict='🎯 今日求职结论：① 金九银十进行中+GPT-6 Astra发布催化AI岗位热度——9月窗口比8月更大；② GPT-6发布带火『AI安全/AI治理』新方向——AI安全产品经理/AI治理/红队测试相关岗位需求上升；③ 可灵获14亿注资+Manus独立——AI应用商业化公司扩招，应用层岗位（产品/运营/增长）确定性最高；④ 周末功课：写GPT-6行业观察+更新简历技能栏；⑤ 周一9:30-11:00黄金窗口照常投递。',
 summary='9月金九银十招聘季进行中，GPT-6 Astra发布成为本周最强催化。重磅：①OpenAI发布GPT-6 Astra（总裁称AGI时代）→全球AI关注度骤升，AI岗位投递窗口热度放大；②『AI安全/AI治理』从冷门变热门——Astra事件让安全评估/红队测试/关键资安能力成为岗位关键词（AI安全产品经理/AI合规/AI治理新增量）；③国家AI基金注资可灵14亿+Manus恢复独立运营→AI应用商业化公司（视频生成/Agent）扩招；④阿里更新Qwen3.8-Max→国产AI生态岗位持续释放。对你的方向（AI产品运营/增长运营）：应用层确定性最高，9月是全年最大窗口。',
 trend='三类岗位增速领先：(1)**AI产品经理/运营**——GPT-6催化AI关注度，金九银十秋招+社招双高峰→9月岗位供给全年最大；(2)**AI安全/AI治理岗（新方向）**——Astra事件让安全从后台到前台→AI安全产品经理/AI治理/红队/合规需求上升，稀缺、门槛相对友好；(3)**AI应用商业化岗**——可灵(视频)/Manus(Agent)/Qwen(模型)生态扩招→AI应用产品/运营/增长是确定性主线。差异化竞争力=AI项目作品集(个人网站可现场演示)+行业观察(GPT-6安全议题)+商业ROI思维。',
 tip='周末求职行动（备战周一）：(1)**写300字行业观察**——《GPT-6 Astra发布：AI安全与能力如何平衡》→本周作品集核心篇；(2)**更新简历技能栏**——补『了解GPT-6 Astra与AI安全治理』（周一面试可讲）；(3)**新增搜索词**——『AI安全产品经理』『AI治理』『AI合规』『红队测试』——GPT-6催化后的新增量方向；(4)**复盘本周投递**——投递数vs周目标15家，面试复盘本更新；(5)**周一黄金窗口**——9:30-11:00集中投递3-5家（BOSS直聘/猎聘/脉脉同步），把可灵/Manus/GPT-6三件套写成面试谈资。',
 reasoning='🔍 发生了什么？\nGPT-6 Astra正式发布(总裁称AGI时代)+可灵获国家AI基金14亿注资+Manus恢复独立运营+金九银十招聘季。\n\n🤔 对AI求职意味着什么？\n① GPT-6发布→AI关注度与岗位热度双升\n② Astra事件→AI安全/AI治理从冷门变热门→新岗位方向\n③ 可灵14亿+Manus独立→AI应用商业化公司扩招→应用层岗需求放大\n④ 金九银十=全年最大窗口——投递量放大，差异化(作品集+观察)更重要\n\n📊 术语解释\nAGI：通用人工智能——OpenAI总裁称GPT-6 Astra已达AGI(有争议)\nAI安全治理：评估与管控前沿模型风险(红队测试/关键资安能力分级)——从学术变岗位\n红队测试：模拟攻击者测试AI安全性的方法\n\n💡 对你的启示\n① 应用层岗(AI产品/运营/增长)确定性最高——可现场演示的作品集是杀手锏\n② AI安全/AI治理是GPT-6催化的新增量方向——提前布局差异化\n③ 国产AI(可灵/Manus/千问生态)是最具成长性的雇主群\n④ 周一9:30-11:00黄金窗口：投3-5家'))

replace_section('anime', sec_obj('anime',
 summary='2026年9月6日动漫区【夺还篇完结倒计时】——Re:Zero S4【夺还篇】追番第25天（8/12开播），最终话9/30定档（还剩24天）——486在丧失记忆后的认知博弈进入收束阶段，全8集由WHITE FOX制作。国产方面：False Memory（B站独播）持续更新；Link Click S3时光代理人第三季热播。BLEACH千年血战篇-祸进谭-仍在最终章。无职转生第三季稳步更新。10月秋季新番档期前瞻开启。',
 trend='9月动漫趋势：(1)**Re:Zero完结倒计时**——最终话9/30定档，夺还篇追番第25天→486在『丧失记忆』下的自我认知博弈临近收束，完结前补番窗口只剩3周多；(2)**秋季新番前瞻**——10月档期临近，Re:Zero完结后接力阵容陆续公布→提前加追番单；(3)**国产悬疑持续**——False Memory+Link Click S3稳定输出；(4)**异世界双雄**——无职转生S3与Re:Zero构成奇幻供给。',
 tip='9月初追番策略：(1)**必追**——Re:Zero夺还篇第25天、9/30最终话，追到最新+补完前篇体验更佳；(2)**同步**——BLEACH千年血战篇、无职转生S3；(3)**前瞻**——关注10月秋季新番情报；(4)**尝鲜**——False Memory+时光代理人S3。周末广州秋高气爽，宅家/外出两相宜。'))

replace_section('gaming', sec_obj('gaming',
 summary='9月初游戏圈：影之刃零预售持续（268元起·10/29发售·国产3A商业化验证）；9/15《研究者》STILLTRACE 发布在即（悬疑解谜）；克系三连发已落地（沉没之城2/命运石之门重启/诡秘之主公测中）。金九银十+秋促临近——Steam愿望单管理、史低监控正当时。',
 trend='9月游戏四大趋势：(1)**国产3A商业化验证**——影之刃零10/29发售前预售数据=市场信心试金石；(2)**9月新作窗口**——《研究者》STILLTRACE 9/15等悬疑克系作品蓄势；(3)**克系主流化完成**——三连发落地后品类进入稳定输出；(4)**促销季临近**——秋促/国庆/双11三连促，补票最佳窗口。',
 tip='9月游戏策略：(1)影之刃零——预售窗口还在(268元起·可退款)，10/29发售前关注实机评测；(2)9/15《研究者》——悬疑解谜爱好者加愿望单；(3)克系补票——命运石之门重启/沉没之城2未入手的可入；(4)促销季——用SteamDB查史低，愿望单排队等秋促折扣。'))

# ---------- 3) OPTIMIZATION_LOG streak（固定为 32：9/2 是 31，9/6 为 32） ----------
content = re.sub(r'streak_days:\s*\d+', 'streak_days: 32', content, count=1)
if 'id:105,' not in content:
    new_opt = (
'    {id:102, cat:"内容优化", title:"GPT-6 Astra 发布专题全站同步（AI安全vs能力释放）", desc:"✅ 9/6实施：OpenAI 9/4发布GPT-6 Astra——ai-track/news/career/AI_OBSERVATIONS 全站同步【GPT-6发布】头条+AI安全治理成面试高频议题", priority:"P0", status:"已完成"},\n'
'    {id:103, cat:"AI功能", title:"AI 数字分身升级：注入 GPT-6/AI 安全语料+按板块精准回答", desc:"待办：AI 数字分身/生活助手当前只基于简历语料——可把每日 AI_OBSERVATIONS/小白课堂也注入 system prompt，让 AI 能回答『今天网站学了什么』『GPT-6 你怎么看』，并支持『去某板块』跳转", priority:"P1", status:"待办"},\n'
'    {id:104, cat:"求职功能", title:"AI 安全/AI 治理岗位雷达（GPT-6催化新增量方向）", desc:"待办：目标公司雷达(#97)扩展——新增『AI安全/AI治理/AI合规』方向关键词与岗位洞察(Astra事件后需求上升、门槛相对友好)，在求职中心给该方向的投递清单", priority:"P2", status:"待办"},\n'
'    {id:105, cat:"稳定性", title:"AI 自动更新失败监控与自愈（连续失败告警）", desc:"待办：9/3-9/4 自动更新两次失败(脚本配平bug已修)但无告警——增加 workflow 失败自动标记、连续2次失败触发 PushPlus 告警、验证修复后连续3天成功再转自动", priority:"P1", status:"待办"},\n'
) if 'id:105,' not in content else ''
    if new_opt:
        marker = '  ]\n};'
        idx = content.rfind(marker)
        content = content[:idx] + new_opt + content[idx:]

# ---------- 4) WEBSITE_GUIDE summary ----------
content = re.sub(r'(版本)[\d.]+', r'\g<1>1.6.6', content, count=1)
content = re.sub(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"',
                 'summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。版本1.6.6。9/6更新：GPT-6 Astra发布+可灵14亿注资+龙餐馆破20亿+A股9月开局偏弱。每天打开都是新的，每天都有提升。"',
                 content, count=1)

open(FP, 'w', encoding='utf-8').write(content)
print('DONE, sections changed:', changed)
