# -*- coding: utf-8 -*-
"""2026-09-12 TOOLCHAIN_RADAR(V4.1 Flash重点) + DAILY_DATA.movie(国庆档) + PICKS.ai-track"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

# ---------- TOOLCHAIN_RADAR ----------
old = re.search(r'var TOOLCHAIN_RADAR = \{.*?\n\};', c, re.S)
new = '''var TOOLCHAIN_RADAR = {
  updated: "2026-09-12",
  headline: "DeepSeek V4.1 Flash 发布(9/10)——多个benchmark超Claude Opus 5/GPT-5.6 Sol·原生视觉·MIT开源·API大降价：开源追平闭源旗舰",
  items: [
    {
      topic: "【重磅】DeepSeek V4.1 Flash 发布（9/10）——你的主力模型该换了",
      type: "模型更新",
      summary: "DeepSeek 9月10日发布 V4.1 Flash：新架构家族最小模型，5520亿参数MoE(激活输入80亿/输出160亿)，原生支持视觉理解。多个benchmark超过 Claude Opus 5 与 GPT-5.6 Sol；AutomationBench-AA 事务Agent性能超 GPT-6 Astra 拿第一；Artificial Analysis 智能指数 v4.3 得40分(超GPT-5.6 Luna)。KV缓存token降至V4-Flash的1/3.9(显存1/4·存储1/8)，API峰值输入$0.3/缓存$0.006/输出$1.2(非峰值半价)，MIT开源可下载部署。",
      impact: "对你的实际影响：①**性能升级**——V4.1 Flash 在多个测试超闭源旗舰，日常主力能力显著提升；②**原生视觉**——终于能用它看图(网站截图/穿搭图/海报分析)——之前DeepSeek不支持图片是你的工具链短板；③**成本再降**——KV缓存降至1/3.9+API降价，Agent/大规模任务的成本门槛进一步降低；④**本地部署**——MIT开源可下载，隐私数据不出域的方案更有竞争力；⑤**风险**——输出token偏多(单任务成本看场景)，速度略逊Gemini 3.8 Flash。",
      action: "**本周务必实测（这是最高优先级）**：①获取(官网API / HuggingFace下载 / ModelScope)；②用 Harness+V4.1 Flash 跑你的高频任务(写码/中文分析/**看图**)；③对比 V4-Flash 的性能+成本；④把过程记录成「模型选型实测」→既是工具升级也是求职作品；⑤若视觉能力好用，可让它分析你的网站截图做UI评审(多模态工作流)"
    },
    {
      topic: "Agent 成为主战场——OpenAI Agents API + Agent-Native 模型",
      type: "生态观察",
      summary: "OpenAI 推出 Agents API 公开测试版(Agent开发标准化)；国内无问芯穹与基元律动联合发布行业首个 Agent-Native 模型 NeoHorse；DeepSeek V4.1 Flash 在 AutomationBench-AA(事务/财务/人事Agent)拿第一",
      impact: "对你的实际影响：①Agent从『概念演示』进入『标准化开发』→AI Agent产品岗需求上升(你的AI产品/运营方向直接受益)；②Agent-Native模型出现→产品设计要理解Agent原生架构(而非把模型硬套进旧流程)；③AutomationBench是新的评测维度→面试聊Agent别只聊概念，要聊『自动化任务完成率/成本』",
      action: "①写进行业观察：Agent从概念到标准化的演进；②求职搜索词加『AI Agent产品』『Agent应用』；③理解Agent-Native概念(为Agent场景原生设计)——面试加分"
    },
    {
      topic: "AI 治理立法化——加州签署AI安全法案",
      type: "生态观察",
      summary: "美国加州州长 Newsom 签署 AI 安全法案(获 Anthropic、OpenAI 支持)——AI安全从企业自律走向立法监管",
      impact: "对你的实际影响：①AI安全/治理/合规从『学术话题』变『法规要求』→相关岗位(安全评估/红队测试/合规)需求将上升；②企业需要能讲清『模型风险+安全评估流程』的人→这是你的差异化加分项；③政策风险提示：未来模型使用/数据合规要求会更严",
      action: "①简历技能栏补『AI安全/治理认知』；②了解红队测试/安全评估/关键资安能力等术语；③关注国内AI监管政策(工信部人工智能+软件专项等)"
    },
    {
      topic: "政策：工信部《人工智能+软件》专项行动",
      type: "生态观察",
      summary: "9/11 工信部发布专项行动实施方案：到2028年软件和信息技术服务业智能化水平显著提升、累计组织实施100项软件企业智能化技改项目，部署智能编程与算力协同；同日A股AI硬件(覆铜板/元件/MLCC)逆势走强",
      impact: "对你的实际影响：①政策驱动『软件智能化改造』→既懂业务又懂AI的人才需求上升(你的复合背景适配)；②智能编程/算力协同是政策方向→相关产品岗机会；③A股AI硬件逆势走强→AI硬件/算力岗位热度上升(投资+求职双联动)",
      action: "①关注『AI+软件』政策受益方向(智能编程/算力协同)；②把政策写进行业观察(体现宏观视角)；③A股AI硬件回踩可关注(覆铜板涨价链)"
    },
    {
      topic: "英伟达 FY27 Q2 财报持续发酵 + Anthropic 350亿算力协议",
      type: "生态观察",
      summary: "英伟达FY27 Q2营收翻倍+FY28指引+70%，Vera Rubin引爆算力供给革命；Anthropic 350亿美元算力协议(与Nvidia投资Lambda)——AI资本开支周期持续扩张",
      impact: "算力需求远未见顶→你用的DeepSeek/讯飞等模型厂商算力底座稳固→A股AI硬件(光模块/PCB/覆铜板)中期逻辑不变，回调即关注",
      action: "①A股AI硬件回调至支撑位可关注；②把『算力景气度』写进投资认知笔记"
    },
    {
      topic: "国产开源阵营：Qwen3.8-Max / GLM-5.3 / 讯飞端侧",
      type: "模型更新",
      summary: "国产开源持续扩容：Qwen3.8-Max(2.4万亿·27B笔记本可跑)、GLM-5.3-Flash(多模态·1/40价格)、科大讯飞端侧模型(离线推理)——叠加V4.1 Flash，国产开源已是工具链绝对主力",
      impact: "工具链选型自由度极高：云端重活用V4.1 Flash/Qwen/GLM，端侧离线用讯飞，隐私任务本地部署(全部可免费/低成本)",
      action: "本周实测组合：Harness+V4.1 Flash(日常主力) / Harness+Qwen3.8-27B(本地) / GLM-5.3-Flash(多模态) → 用数据定主力"
    }
  ]
};'''
if old:
    c = c.replace(old.group(0), new, 1)
    print('OK TOOLCHAIN_RADAR')

# ---------- DAILY_DATA.movie（国庆档） ----------
old_mv = re.search(r'"movie": \{[\s\S]*?\n  \}\n\};', c)
new_mv = '''"movie": {
    "summary": "2026年电影市场：4部影片定档国庆档——《小猪佩奇·完美假期》《野兽之心》《熊猫守护者》《活色生香》，陈思诚新片(张译/马丽主演)也将杀进国庆档、票房预期剑指10亿。《哪吒之魔童闹海》获第38届大众电影百花奖最佳影片奖——国产动画获主流奖项认可。《欢迎来龙餐馆》累计破20亿、居年度票房榜第三。暑期档124亿收官+9月近40部影片定档。Re:Zero S4夺还篇最终话9/30定档（倒计时18天）。",
    "trend": "国庆档4部定档+陈思诚新片|哪吒获百花奖最佳影片|龙餐馆破20亿年榜第三|暑期档124亿|9月近40部新片|Re:Zero 9/30完结",
    "tip": "9月中观影策略：①国庆档前瞻——4部已定档+陈思诚新片，头部影片陆续公布，提前加片单；②补看《哪吒之魔童闹海》(百花奖最佳影片·国产动画标杆)、《欢迎来龙餐馆》(破20亿·豆瓣8.4长尾)；③《奥德赛》诺兰IMAX热映；④Re:Zero夺还篇最终话9/30(倒计时18天)，补番窗口收窄。",
    "reasoning": "🔍 发生了什么？\\n国庆档4部影片定档+陈思诚新片杀进(张译/马丽)；《哪吒之魔童闹海》获百花奖最佳影片；龙餐馆累计破20亿居年榜第三。\\n\\n🤔 为什么重要？\\n① 国庆档是全年第二大档期——头部影片密集定档=内容供给充足\\n② 哪吒获百花奖=国产动画获主流认可，内容品质获行业背书\\n③ 龙餐馆破20亿=口碑长尾+喜剧刚需的双引擎验证\\n④ 9月是暑期到国庆的过渡档——新片供给决定国庆档前热度\\n\\n📊 术语解释\\n国庆档：10/1-10/7的黄金档期——全年票房第二大档(仅次于春节档)\\n百花奖：大众电影百花奖——观众投票的权威电影奖项\\n长尾效应：上映后期持续卖座——口碑好的影片长线续航\\n\\n💡 启示\\n① 内容品质获主流认可→文娱行业景气度回升\\n② 国庆档定档潮→宣发/内容运营岗位机会(金九银十)\\n③ 从奖项与票房双数据看内容行业趋势",
    "updated": "2026-09-12"
  }
};'''
if old_mv:
    c = c.replace(old_mv.group(0), new_mv, 1)
    print('OK DAILY_DATA.movie')

# ---------- PICKS.ai-track 头部加 V4.1 Flash ----------
old_pick = '{icon:"🤖", title:"GPT-6 Astra 正式发布 🆕", desc:"9/4发布·总裁称AGI时代到来·曾因网络安全风险暂停一个月·AI安全vs能力释放成焦点", link:"https://www.nbd.com.cn/articles/2026-09-01/4568432.html"},'
new_pick = '{icon:"🐳", title:"DeepSeek V4.1 Flash 发布 🆕", desc:"9/10发布·多个benchmark超Opus5/GPT-5.6 Sol·原生视觉·MIT开源·API降价(峰值$0.3/$1.2)", link:"https://gigazine.net/news/20260911-deepseek-v4-1-flash/"},\n    {icon:"🤖", title:"GPT-6 Astra 正式发布", desc:"9/4发布·总裁称AGI时代到来·闭源·API $10/$50·主打长程Agent/Computer Use", link:"https://m.thepaper.cn/newsDetail_forward_34013011"},'
if old_pick in c:
    c = c.replace(old_pick, new_pick, 1)
    print('OK PICKS.ai-track')

open(FP, 'w', encoding='utf-8').write(c)
print('done radar+movie+picks')
