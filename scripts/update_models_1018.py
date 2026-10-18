# -*- coding: utf-8 -*-
"""补齐 2026-09-22 ~ 10-16 的新模型：Claude Opus 5.5 / Sonnet 5.5 /
   Gemini 4 Argon / GPT-6.1 Sol Ultrafast / Reflection Beam
   数据来源：Artificial Analysis(9/22)、量子位(9/30)、光明网(10/14)、第一财经(10/9)、Reflection 官方(10/16)
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

# ---------------- 1) Sonnet 4.6 → Sonnet 5.5 ----------------
old_sonnet = re.search(r'\{name:"Claude Sonnet 4\.6".*?\n    \},', d, re.S)
new_sonnet = '''{name:"Claude Sonnet 5.5", emoji:"🎵", provider:"Anthropic", series:"中端·代码反超旗舰", tier:"🆕 中杯打大杯(9/30)",
     input_price:"$2.00", output_price:"$10.00", cost_per_task:"≈$0.20",
     intelligence:86, speed:88,性价比:92, 安全:89, 综合:88,
     context:"1M", params:"未公开",
     strengths:"9/30 发布·Terminal-Bench 4.0 达 70.6% <b>反超 Opus 5.5(66.4%)</b>，上代 Sonnet 5 仅 10.3%·GDPval-AA 1844 Elo(Opus 5.5 为 1846)·OSWorld 2.1 80.1%·工具调用少约 1/3、Shell 运行次数近乎减半·Base44 实测平均 3.6 轮达到 Opus 5 需 7.7 轮的效果·首个仅看截图通关《宝可梦·红》的 Sonnet·真实成本最高再降 30%、速度 +30%",
     weaknesses:"复杂开放式长判断仍不如 Opus 5.5·通用智能指数非榜首·1M 上下文实际长文表现待验证",
     best_for:"日常 Coding·修 Bug·写文档/PPT/表格·边界明确的工程任务·性价比敏感的生产环境",
     price_note:"🆕 9/30 发布：$2/$10 每百万 token（正好是 Opus 5.5 的一半）·缓存读取 $0.20 不变·Anthropic 强调「同样钱能干多少活」：Terminal-Bench 只开 Medium 已超 Sonnet 5 最好成绩，成本不到 1/10",
     free_tier:"✅ 免费档可用（限量）"
    },'''
if old_sonnet:
    d = d[:old_sonnet.start()] + new_sonnet + d[old_sonnet.end():]
    print('✅ Claude Sonnet 4.6 → Sonnet 5.5')
else:
    print('❌ 未找到 Sonnet 4.6 条目')

# ---------------- 2) 在 Opus 5 之前插入 Opus 5.5 ----------------
opus55 = '''{name:"Claude Opus 5.5", emoji:"👑", provider:"Anthropic", series:"旗舰·深度推理(9/22)", tier:"🆕 智能指数榜首",
     input_price:"$4.00", output_price:"$20.00", cost_per_task:"≈$1.00",
     intelligence:95, speed:68,性价比:78, 安全:92, 综合:85,
     context:"1M", params:"未公开",
     strengths:"9/22 发布·<b>AA 智能指数 58 分(榜上最高)</b>·HLE 61.4%(前纪录 59.1%)·SciCode 66.9%·Terminal-Bench 4.0 59.6% 与 GPT-6 Astra 持平(+11 高于 Opus 5)·AA-Briefcase 1822 Elo(+143)·GDPval-AA 1846 Elo·十项评测中六项领先·五档 effort(low/medium/high/xhigh/max)·长任务知识工作第一",
     weaknesses:"输出 token 偏多(约 119k/任务，Opus 5 为 73k)·CritPt / AA-LCR / GDP.pdf 三项落后·速度中等·贵于 Sonnet 5.5 一倍",
     best_for:"高难度推理·复杂开放式长任务·专业交付物(报告/分析)·需要判断力的 Agent 工作·安全关键场景",
     price_note:"🆕 9/22 发布即降价 20%：$4/$20（Opus 5 为 $5/$25）·缓存写入 $5/1M(5分钟TTL)·<b>缓存读取 $0.20/1M（较 Opus 5 降 60%，等于未缓存输入的 95% 折扣）</b>·max effort 也在性价比前沿",
     free_tier:"❌ 需 Pro($20/月)或 Max"
    },
    '''
anchor = '{name:"Claude Opus 5",'
if anchor in d:
    d = d.replace(anchor, opus55 + anchor, 1)
    print('✅ 已插入 Claude Opus 5.5')
else:
    print('❌ 未找到 Opus 5 锚点')

# ---------------- 3) Fable 5 → Fable 5.1 ----------------
d = d.replace('{name:"Claude Fable 5",', '{name:"Claude Fable 5.1",', 1)
d = d.replace('strengths:"创意写作业界最强·叙事质量极高·角色扮演/对话生成一流·长篇连贯性卓越"',
              'strengths:"创意写作业界最强·叙事质量极高·角色扮演/对话生成一流·长篇连贯性卓越·5.1 版此前是 HLE 纪录保持者(59.1%，后被 Opus 5.5 的 61.4% 打破)"', 1)
print('✅ Claude Fable 5 → Fable 5.1')

# ---------------- 4) Gemini 4 Argon（插在 Gemini 3.6 Flash 之后）----------------
gem4 = '''
    {name:"Gemini 4 Argon", emoji:"🔷", provider:"Google", series:"Gemini 4 系列首发", tier:"🆕 前沿(10/13)",
     input_price:"限时五折(官方价未统一)", output_price:"限时五折", cost_per_task:"视任务",
     intelligence:88, speed:82,性价比:87, 安全:85, 综合:87,
     context:"未公开(长上下文重点)", params:"未公开(官方刻意不强调参数)",
     strengths:"10/13 DeepMind 上线·Gemini 4 系列首个前沿模型·定位从「炫技」转向「干活」：软件工程 / 企业知识工作 / 网络防御三大场景·<b>API 限时五折</b>·macOS 版整合智能体编程界面·主打多模态 + 智能体 + 长上下文三合一",
     weaknesses:"官方未公布具体评测分数·生态刚上线·中文场景待验证·「限时五折」结束后的实际成本未知",
     best_for:"软件工程·企业知识管理·安全防御类任务·Google 生态(Workspace/macOS)·多模态 + Agent 组合场景",
     price_note:"🆕 10/13 发布·API 限时五折（信号是推理成本快速下降）·官方未强调参数量，评价标准转向「能不能把活干好」",
     free_tier:"✅ Gemini 应用可用"
    },'''
old_g = re.search(r'\{name:"Gemini 3\.6 Flash".*?\n    \},', d, re.S)
if old_g:
    d = d[:old_g.end()] + gem4 + d[old_g.end():]
    print('✅ 已插入 Gemini 4 Argon')
else:
    print('❌ 未找到 Gemini 3.6 Flash')

# ---------------- 5) GPT-6.1 Sol Ultrafast（插在 GPT-6 Astra 之后）----------------
gpt61 = '''
    {name:"GPT-6.1 Sol Ultrafast", emoji:"⚡", provider:"OpenAI", series:"Sol 超快版", tier:"🆕 速度优先(10/9)",
     input_price:"未公开", output_price:"未公开", cost_per_task:"—",
     intelligence:92, speed:93,性价比:76, 安全:78, 综合:87,
     strengths:"10/9 由 OpenAI 开发者侧推出·定位是 GPT-6.1 Sol 的<b>超快版本</b>，在保留 Sol 推理能力的前提下拉高吞吐·适合延迟敏感的批量任务",
     weaknesses:"官方未公布基准与定价·docs 信息极少·闭源，无法本地部署·「Ultrafast」通常意味着单 token 更贵、但按任务算可能更省",
     best_for:"延迟敏感场景·高吞吐批处理·需要 Sol 级推理但要更快返回的工作流",
     price_note:"🆕 10/9 发布·价格未公开·关注点应是「单任务总成本」而不是单 token 价格",
     free_tier:"❌ 未开放免费"
    },'''
old_a = re.search(r'\{name:"GPT-6 Astra".*?\n    \},', d, re.S)
if old_a:
    d = d[:old_a.end()] + gpt61 + d[old_a.end():]
    print('✅ 已插入 GPT-6.1 Sol Ultrafast')
else:
    print('❌ 未找到 GPT-6 Astra')

# ---------------- 6) Reflection Beam（追加到 models 末尾）----------------
beam = '''
    // ===== Reflection（2026-10-16 新增·开放权重）=====
    {name:"Reflection Beam", emoji:"🔭", provider:"Reflection AI", series:"开放权重旗舰", tier:"🆕 开源阵营(10/16)",
     input_price:"开放权重(自托管)", output_price:"开放权重(自托管)", cost_per_task:"自托管成本",
     intelligence:62, speed:80,性价比:90, 安全:80, 综合:75,
     strengths:"10/16 发布·<b>501B 参数开放权重</b>·AA 智能指数 30，<b>美国开放权重模型中排第 2</b>·定位对标中国开源模型·可本地部署",
     weaknesses:"智能指数 30 与闭源前沿(Opus 5.5 的 58)差距明显·501B 自托管门槛高（需要多卡）·生态与工具链尚早",
     best_for:"需要完全自主可控的部署·美国合规背景下的开源替代·研究与微调基座",
     price_note:"🆕 10/16 发布·开放权重，无 API 价格；实际成本是自托管的算力，501B 规模不适合个人",
     free_tier:"✅ 开放权重可下载"}'''
i_comp = d.find('var AI_MODEL_COMPARISON')
m_open = re.search(r'models:\s*\[', d[i_comp:])
i_arr = i_comp + m_open.end()
depth, k = 1, i_arr
while k < len(d) and depth > 0:
    if d[k] == '[': depth += 1
    elif d[k] == ']': depth -= 1
    k += 1
k -= 1
d = d[:k] + ',' + beam + '\n  ' + d[k:]
print('✅ 已追加 Reflection Beam')

# ---------------- 7) description / key_takeaways ----------------
old_d = re.search(r'description:\s*"主流大模型全维度对比[^"]*"', d)
new_d = ("主流大模型全维度对比 · 同系列区分(Flash/Pro/Luna/Sol/Max/27B/V4.1/Muse/Argon) · 百分制评分 · 综合加权评分 · "
  "最新价格(含调价标注) · 每日更新 · <b>10/18 补录 9 个新版本</b>：① Claude Opus 5.5(9/22·AA智能指数58榜首·降价20%) "
  "② Claude Sonnet 5.5(9/30·Terminal-Bench 70.6% 反超旗舰·价格一半) ③ Gemini 4 Argon(10/13·限时五折·转向「干活」) "
  "④ GPT-6.1 Sol Ultrafast(10/9·速度优先) ⑤ Reflection Beam(10/16·501B开放权重) "
  "⑥ DeepSeek-V4.1-Flash-1017(10/17) ⑦ Meta Muse Wonder / Full(10/12) ⑧ Claude Fable 5.1。"
  "评分含推算值（官方未公布分数的模型已标注），口径见 scoring_guide")
if old_d:
    d = d[:old_d.start()] + 'description: ' + json.dumps(new_d, ensure_ascii=False) + d[old_d.end():]
    print('✅ description 已更新')

kt = '''key_takeaways: [
    "👑 智能指数榜首易主: Claude Opus 5.5(9/22) 拿下 AA 智能指数 58 分——HLE 61.4%·SciCode 66.9%·十项评测六项领先，且同时降价 20%($4/$20)·缓存读取降 60%",
    "🎵 中杯反超大杯: Claude Sonnet 5.5(9/30) Terminal-Bench 4.0 达 70.6%，<b>高于 Opus 5.5 的 66.4%</b>，价格只有一半($2/$10)·工具调用少 1/3、Shell 次数近乎减半",
    "🔷 谷歌重回前沿: Gemini 4 Argon(10/13) 刻意不谈参数量，只讲「软件工程/企业知识/网络防御」三个场景·API 限时五折·竞争从跑分转向落地",
    "🔭 开源追赶到哪了: Reflection Beam(10/16) 501B 开放权重，AA 智能指数 30，是美国开放权重第 2——但与闭源前沿(58)仍有代差",
    "📊 评价标准变了: 从「谁的跑分高」转向「完成一个任务要花多少钱」——Sonnet 5.5 只开 Medium 就超 Sonnet 5 最好成绩且成本 1/10；Opus 5.5 输出 token 是 Astra 的 4 倍但单任务成本持平",
    "🐳 国产性价比: DeepSeek V4.1-Flash-1017 综合 91 分仍最高——Terminal-Bench 42.3·DeepSWE 77.0(接近 Opus 5.5 的 79.0 区间)·闲时价格再减半",
    "🌌 幻觉率与知识广度是两件事: Meta Muse Wonder Full 幻觉率 23%(Opus 5.5 系 59%)但知识指数仅 30——高置信度场景选它，广度问答仍选 Opus/Astra",
    "🎯 选型策略: 日常主力 DeepSeek V4.1-Flash-1017(91)·性价比 Coding 用 Claude Sonnet 5.5(88)·高难度长任务用 Opus 5.5(85)·多模态用 Gemini 4 Argon/GLM-5.3-Flash·本地隐私 Qwen3.8-27B / Reflection Beam"
  ],'''
old_kt = re.search(r'key_takeaways:\s*\[[\s\S]*?\n  \],', d)
if old_kt:
    d = d[:old_kt.start()] + kt + d[old_kt.end():]
    print('✅ key_takeaways 已更新（8 条）')

# ---------------- 8) price_adjustments 追加 ----------------
m_pa = re.search(r'price_adjustments:\s*\[\s*\n', d)
if m_pa:
    add = '''    {model:"Claude Opus 5.5", date:"2026-09-22", change:"🆕 发布 + 降价 20%（$5/$25 → $4/$20）+ 缓存读取降 60%（$0.50 → $0.20）", reason:"AA 智能指数 58 分登顶·HLE 61.4%·SciCode 66.9%·Terminal-Bench 4.0 59.6% 与 GPT-6 Astra 持平·十项评测六项领先·五档 effort 中四档在性价比前沿", impact:"智能与成本同时改善·缓存读取相当于未缓存输入的 95% 折扣·长会话/重复上下文的 Agent 场景成本大幅下降"},
    {model:"Claude Sonnet 5.5", date:"2026-09-30", change:"🆕 中端模型代码能力反超旗舰，价格仅一半", reason:"Terminal-Bench 4.0 70.6%（Opus 5.5 为 66.4%，上代 Sonnet 5 仅 10.3%）·GDPval-AA 1844·OSWorld 2.1 80.1%·工具调用少 1/3、Shell 次数近乎减半", impact:"「中杯打大杯」成为现实：日常 Coding 不必再上旗舰·真实成本最高再降 30%、速度 +30%·Anthropic 开始用「单任务成本」而非单价做卖点"},
    {model:"Gemini 4 Argon", date:"2026-10-13", change:"🆕 Gemini 4 系列首发 + API 限时五折", reason:"DeepMind 不再强调参数规模，聚焦软件工程/企业知识工作/网络防御三类真实任务·macOS 版整合智能体编程界面", impact:"前沿模型竞争从「炫技」转向「干活」·限时五折预示推理成本持续下行·多模态+Agent+长上下文三合一路线"},
    {model:"GPT-6.1 Sol Ultrafast", date:"2026-10-09", change:"🆕 推出 Sol 的超快版本", reason:"OpenAI 开发者侧发布·在保留 Sol 推理能力前提下拉高吞吐·面向延迟敏感场景", impact:"官方未公布基准与定价·需以「单任务总成本」而非单 token 价格评估"},
    {model:"Reflection Beam", date:"2026-10-16", change:"🆕 501B 参数开放权重模型", reason:"Reflection AI 首个模型·AA 智能指数 30·美国开放权重模型第 2·定位对标中国开源生态", impact:"开源阵营继续追赶但与闭源前沿(58)仍有代差·501B 自托管门槛高，个人用户不现实"},
'''
    d = d[:m_pa.end()] + add + d[m_pa.end():]
    print('✅ price_adjustments 已追加 5 条')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:400])
