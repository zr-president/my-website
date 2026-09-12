# -*- coding: utf-8 -*-
"""2026-09-12 每日更新（周六版）：DAILY_DATA头部 + BRIEFING 8卡 + MARKET_SENTIMENT
+ AI_MODEL_COMPARISON 新增 DeepSeek V4.1 Flash（9/10发布·超Opus5/GPT-5.6 Sol）
+ AGENT_STACKS 新增 V4.1 Flash 组合"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) DAILY_DATA 头部 ----------
c = c.replace('"update_time": "2026-09-07T18:55:00+08:00"', '"update_time": "2026-09-12T11:55:00+08:00"')
c = c.replace('"update_date": "2026年9月7日"', '"update_date": "2026年9月12日"')

old_ms = re.search(r'"market_summary": "([^"]*)"', c)
new_ms = ('"market_summary": "周末(9/12)A股休市·最新收盘为周五(9/11)：三大指数放量下挫·沪指-1.18%收3888.11失守3900·深成指-1.08%收13471.26·创业板指-0.49%收3322.04｜'
          '成交1.97万亿(放量3247亿)·超4870只个股下跌·赚钱效应仅11%｜AI硬件逆势走强：覆铜板+4.31%/元件+1.80%/通信设备+1.66%/MLCC+1.76%·崇达技术/嘉立创/风华高科涨停｜军工(地面兵装+4.44%)/电力逆势·有色领跌(工业金属-5.04%·北方铜业跌停)｜'
          '外围扰动：布伦特原油破109美元·中东地缘升级·碳酸锂期货跌破13万/吨·恒生科技创两个半月新低 ｜ 政策催化：工信部《人工智能+软件专项行动实施方案》(2028年100项软件企业智能化技改) ｜ 大模型：DeepSeek V4.1 Flash 9/10发布·超Opus5/GPT-5.6 Sol·原生视觉·MIT开源 ｜ 下周一(9/14)关注：①3888能否收回3900 ②AI硬件(覆铜板/元件)持续性 ③美联储9月议息"')
c = c.replace(old_ms.group(0), new_ms, 1)

# news_headlines（5条 9/12）
old_nh = re.search(r'"news_headlines": \[[\s\S]*?\n  \],', c)
new_nh = '''"news_headlines": [
    {"title": "A股9/11放量下挫：沪指-1.18%收3888.11失守3900·超4870只个股下跌·AI硬件(覆铜板/元件)逆势活跃·有色领跌", "url": "https://wap.stockstar.com/detail/IG2026091100029578", "source": "证券之星/智通财经", "category": "财经"},
    {"title": "DeepSeek V4.1 Flash 发布(9/10)：多个benchmark超Claude Opus 5/GPT-5.6 Sol·原生视觉理解·5520亿MoE·MIT开源", "url": "https://gigazine.net/news/20260911-deepseek-v4-1-flash/", "source": "GIGAZINE/DeepSeek", "category": "科技"},
    {"title": "工信部发布《『人工智能+软件』专项行动实施方案》：2028年累计100项软件企业智能化技改项目", "url": "https://wap.stockstar.com/detail/IG2026091100029578", "source": "工信部/证券之星", "category": "政策"},
    {"title": "4部影片定档2026国庆档：《小猪佩奇·完美假期》《野兽之心》《熊猫守护者》《活色生香》·陈思诚新片杀进国庆档", "url": "https://www.shobserver.com/staticsg/res/html/web/sgh/sghNewsDetail.html?id=4053660", "source": "上观新闻/新浪财经", "category": "文娱"},
    {"title": "OpenAI推出Agents API公开测试版·美国加州签署AI安全法案(Anthropic/OpenAI支持)·无问芯穹发布Agent-Native模型NeoHorse", "url": "https://finance.eastmoney.com/a/202609113872283334.html", "source": "东方财富/路透社", "category": "科技"}
  ],'''
c = c.replace(old_nh.group(0), new_nh, 1)

# ---------- 2) DAILY_BRIEFING 8卡（9/12周六版） ----------
old_brief = re.search(r'var DAILY_BRIEFING = \{.*?\n\};', c, re.S)
new_brief = '''var DAILY_BRIEFING = {
  date: "2026-09-12",
  highlights: [
    {priority:1, icon:"🐳", section:"DeepSeek V4.1 Flash", headline:"DeepSeek V4.1 Flash 发布(9/10)：多个测试超Claude Opus 5与GPT-5.6 Sol·原生视觉·MIT开源·API大降价", summary:"9月10日 DeepSeek 发布 V4.1 Flash——新架构家族最小模型，5520亿参数 MoE(激活输入80亿/输出160亿)，原生支持视觉理解。多个 benchmark 超过 Claude Opus 5 和 GPT-5.6 Sol；AutomationBench-AA 事务Agent性能超 GPT-6 Astra 拿下第一；Artificial Analysis 智能指数v4.3得40分(超GPT-5.6 Luna)。KV缓存token降至V4-Flash的1/3.9、显存1/4、存储1/8；API价峰值输入$0.3/缓存$0.006/输出$1.2(非峰值半价)；MIT开源可下载部署。", action:"深度解读", link:"#ai-track", deepLink:"https://gigazine.net/news/20260911-deepseek-v4-1-flash/"},
    {priority:2, icon:"📉", section:"A股失守3900", headline:"A股9/11放量下挫：沪指-1.18%收3888.11失守3900·超4870只个股下跌·赚钱效应仅11%", summary:"9月11日（周五）A股三大指数放量收跌：沪指跌1.18%收3888.11（失守3900）、深成指-1.08%收13471.26、创业板指-0.49%收3322.04、北证50-2.66%。两市成交1.97万亿（放量3247亿），全市场上涨643只/下跌4870只、赚钱效应仅11%。盘面分化：AI硬件（覆铜板+4.31%/元件+1.80%/通信设备+1.66%/MLCC+1.76%）与军工（地面兵装+4.44%）、电力逆势走强；有色金属领跌（工业金属-5.04%，北方铜业跌停）。外围扰动：布伦特原油破109美元、中东地缘升级、碳酸锂期货跌破13万/吨、恒生科技创两个半月新低。", action:"深度分析", link:"#stock", deepLink:"https://wap.stockstar.com/detail/IG2026091100029578"},
    {priority:3, icon:"🤖", section:"人工智能+软件政策", headline:"工信部发布《『人工智能+软件』专项行动实施方案》：2028年100项软件企业智能化技改·AI硬件获催化", summary:"9月11日工信部发布《『人工智能+软件』专项行动实施方案》：到2028年软件和信息技术服务业智能化水平显著提升、累计组织实施100项软件企业智能化技改项目，部署智能编程与算力协同。政策催化下AI硬件逆势走强：覆铜板（建滔积层板年内第七份涨价函、中国巨石电子布涨价）、元件、通信设备、MLCC领涨，崇达技术/嘉乐创/风华高科涨停。", action:"了解政策", link:"#ai-track", deepLink:"https://wap.stockstar.com/detail/IG2026091100029578"},
    {priority:4, icon:"🎬", section:"国庆档定档", headline:"4部影片定档2026国庆档：《小猪佩奇·完美假期》《野兽之心》《熊猫守护者》《活色生香》·陈思诚新片杀进", summary:"2026国庆档已定档4部影片：《小猪佩奇·完美假期》《野兽之心》《熊猫守护者》《活色生香》；陈思诚新片（张译、马丽主演）也将杀进国庆档，票房预期剑指10亿。当前市场：龙餐馆破20亿（年榜第三）、《哪吒之魔童闹海》获百花奖最佳影片——国产内容品质持续获认可，国庆档预热启动。", action:"查看定档", link:"#movie", deepLink:"https://www.shobserver.com/staticsg/res/html/web/sgh/sghNewsDetail.html?id=4053660"},
    {priority:5, icon:"🛡️", section:"AI安全立法", headline:"美国加州签署AI安全法案(Anthropic/OpenAI支持)·OpenAI推出Agents API公开测试版", summary:"AI治理双动态：①美国加州州长Newsom签署AI安全法案（获Anthropic、OpenAI支持）——AI安全从企业自律走向立法；②OpenAI推出Agents API公开测试版——Agent开发生态进一步标准化。叠加国内无问芯穹与基元律动联合发布行业首个 Agent-Native 模型 NeoHorse——Agent 成为模型/平台竞争主战场。", action:"了解AI治理", link:"#ai-track", deepLink:"https://finance.eastmoney.com/a/202609113872283334.html"},
    {priority:6, icon:"💼", section:"金九银十求职", headline:"金九银十进行中：DeepSeek V4.1 Flash开源+Agent API标准化·AI岗位持续放量", summary:"金九银十招聘季进行中。本周AI信号：①DeepSeek V4.1 Flash 以 MIT 开源、超 Opus5/GPT-5.6 Sol、原生视觉——开源模型能力再上一个台阶，本地部署/私有化方案更有竞争力；②OpenAI Agents API 公开测试→Agent 开发岗位需求上升；③工信部人工智能+软件专项行动→智能化改造岗位需求。周末建议：写300字行业观察（DeepSeek V4.1 Flash开源意义）＋更新简历技能栏＋备周一投递。", action:"准备投递", link:"#career", deepLink:"https://www.zhipin.com/"},
    {priority:7, icon:"💪", section:"腹肌训练计划", headline:"健身区升级：腹肌专项计划上线（俯卧撑60个/平板2.5min基础·跳绳+拉力绳组合）", summary:"针对『能摸出腹肌轮廓但还有赘肉』的情况，健身区新增腹肌专项计划：核心矛盾是体脂率（男性腹肌可见需体脂≤12-15%）而非腹肌肌肉量；59kg偏瘦不宜大减重，策略是『减脂+腹肌增厚同步』。方案：跳绳HIIT（30秒快跳+30秒休息×10-15组·每周3-4次）控脂 + 腹肌专项（平板变式/拉力绳卷腹/仰卧抬腿·每周3-4次）+ 俯卧撑变式升级（宽距/窄距/下斜/爆发）。8周周期。", action:"查看计划", link:"#fitness", deepLink:"#fitness"},
    {priority:8, icon:"🎬", section:"动漫完结倒计时", headline:"Re:Zero第四季【夺还篇】最终话9/30定档·完结倒计时18天", summary:"Re:Zero S4 夺还篇将于9/30播出最终话，完结倒计时18天——486在丧失记忆后的认知博弈进收束阶段。同步追更：BLEACH千年血战篇-祸进谭、无职转生S3、False Memory、时光代理人S3；10月秋季新番档期临近，接档阵容陆续公布，可提前加追番单。", action:"去追番", link:"#anime", deepLink:"https://www.bilibili.com/search?keyword=Re%E4%BB%8E%E9%9B%B6%E5%BC%80%E5%A7%8B%E7%9A%84%E5%BC%82%E4%B8%96%E7%95%8C%E7%94%9F%E6%B4%BB"}
  ]
};'''
c = c.replace(old_brief.group(0), new_brief, 1)

# ---------- 3) MARKET_SENTIMENT ----------
old_ms2 = re.search(r'var MARKET_SENTIMENT = \{.*?\n\};', c, re.S)
new_ms2 = '''var MARKET_SENTIMENT = {
  updated: "2026-09-12",
  items: [
    {label:"沪指", value:"3888.11", color:"#059669", note:"9/11收-1.18%·失守3900·放量下挫"},
    {label:"涨跌家数", value:"643↑/4870↓", color:"#dc2626", note:"9/11赚钱效应仅11%·普跌"},
    {label:"强势板块", value:"AI硬件", color:"#059669", note:"覆铜板+4.31%/元件+1.80%/军工+4.44%逆势"},
    {label:"量能", value:"1.97万亿", color:"#d97706", note:"放量3247亿·下跌放量需谨慎"}
  ]
};'''
c = c.replace(old_ms2.group(0), new_ms2, 1)

# ---------- 4) AI_MODEL_COMPARISON：新增 DeepSeek V4.1 Flash（插在 V4-Flash 之后） ----------
anchor = '''     free_tier:"✅ 完全免费(chat.deepseek.com)"
    },
'''
v41 = '''     free_tier:"✅ 完全免费(chat.deepseek.com)"
    },
    {name:"DeepSeek V4.1 Flash", emoji:"🐳", provider:"DeepSeek", series:"V4.1新架构·原生视觉", tier:"🆕 开源旗舰(9/10发布)",
     input_price:"$0.30(峰值)", output_price:"$1.20(峰值·非峰值半价)", cost_per_task:"≈$0.02",
     intelligence:86, speed:90,性价比:96, 安全:86, 综合:91,
     context:"未公开(继承1M级)", params:"5520亿MoE(激活:输入80亿/输出160亿)",
     strengths:"9/10发布·多个benchmark超Claude Opus 5与GPT-5.6 Sol·原生视觉理解(图像输入)·AutomationBench-AA事务Agent性能超GPT-6 Astra拿第一·AA智能指数v4.3得40分(超GPT-5.6 Luna)·KV缓存token降至V4-Flash的1/3.9(显存1/4·存储1/8)·MIT开源可本地部署",
     weaknesses:"任务输出token偏多(比Claude Fable 5.1多·单任务成本未必最优)·速度略逊Gemini 3.8 Flash/Muse Spark 1.3·生态适配仍在完善",
     best_for:"日常主力升级(替代V4-Flash)·多模态任务(原生视觉)·Agent/自动化工作流·成本敏感+隐私场景·本地部署",
     price_note:"🆕 9/10发布·API大幅降价：峰值输入$0.3/缓存输入$0.006/输出$1.2(对比V4-Flash曾涨价)·非峰值半价·MIT开源可免费本地部署",
     free_tier:"✅ MIT开源·HuggingFace/ModelScope可下载·官网免费"
    },
'''
if 'DeepSeek V4.1 Flash' not in c:
    c = c.replace(anchor, v41, 1)
    print('OK AI_MODEL_COMPARISON + V4.1 Flash')
else:
    print('SKIP V4.1 already exists')

# 更新 AI_MODEL_COMPARISON description
c = re.sub(r'description: "主流大模型全维度对比[^"]*"',
  'description: "主流大模型全维度对比 · 同系列区分(Flash/Pro/Luna/Sol/Max/27B/V4.1) · 百分制评分 · 综合加权评分 · 最新价格(含调价标注) · 每日更新 · 9/12更新：DeepSeek V4.1 Flash发布(9/10·5520亿MoE·原生视觉·超Opus5/GPT-5.6 Sol·MIT开源·API降价)+GPT-6 Astra(闭源·API $10/$50)"', c, count=1)

# ---------- 5) AGENT_STACKS：新增 Harness + V4.1 Flash 组合 ----------
anchor2 = '''    {agent:"DeepSeek Harness", model:"DeepSeek V4-Pro", emoji:"🐳",'''
v41_stack = '''    {agent:"DeepSeek Harness", model:"DeepSeek V4.1 Flash", emoji:"🐳",
      score:{编程:91, 性价比:97, 中文:95, 生态:78, 速度:92}, 综合:93,
      monthly_cost:"¥0-20（API大幅降价）/ 本地部署免费",
      monthly_cost_note:"峰值输入$0.3/输出$1.2·非峰值半价·MIT开源可本地跑",
      pros:"9/10新架构旗舰·多个benchmark超Opus5/GPT-5.6 Sol·原生视觉(能看图/截图)·AutomationBench-AA超GPT-6 Astra·KV缓存token降至1/3.9(成本再降)·MIT开源本地部署·官方Harness原生适配",
      cons:"输出token偏多(单任务成本看场景)·生态适配还在完善·比Gemini 3.8 Flash略慢",
      best_for:"⭐ 新的日常主力首选·多模态(看图/截图分析)·Agent自动化·隐私任务本地部署·成本敏感",
      verdict:"⭐ 强推升级：V4.1 Flash 全面超越 V4-Flash(视觉+性能+成本)，Harness+V4.1 Flash 成为中文/多模态/Agent场景的最优解——建议本周实测替换"},
    {agent:"DeepSeek Harness", model:"DeepSeek V4-Pro", emoji:"🐳",'''
if 'model:"DeepSeek V4.1 Flash"' not in c:
    c = c.replace(anchor2, v41_stack, 1)
    print('OK AGENT_STACKS + V4.1 Flash')
else:
    print('SKIP stack exists')

open(FP, 'w', encoding='utf-8').write(c)
print('DONE head+briefing+sentiment+models')
