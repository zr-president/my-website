# -*- coding: utf-8 -*-
"""更新 AI 评分表 + AI 动态追踪（REA / DeepSeek V4.1-Flash-1017 / Meta Muse Wonder）
   数据来源（2026-10-12 ~ 10-18 公开报道），均为二手信息，已在页面标注
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
TODAY = '2026-10-18'
d = open(FP, 'r', encoding='utf-8').read()


def js(o):
    return json.dumps(o, ensure_ascii=False)


# ============ 1) 评分表：updated / description ============
d = d.replace('var AI_MODEL_COMPARISON = {\n  updated: "2026-09-06",',
              'var AI_MODEL_COMPARISON = {\n  updated: "2026-10-18",', 1)
old_desc = re.search(r'description:\s*"主流大模型全维度对比[^"]*"', d)
new_desc = ("主流大模型全维度对比 · 同系列区分(Flash/Pro/Luna/Sol/Max/27B/V4.1/Muse) · 百分制评分 · 综合加权评分 · "
            "最新价格(含调价标注) · 每日更新 · <b>10/18 更新</b>：① DeepSeek-V4.1-Flash-1017 上线(10/17·"
            "Terminal-Bench 4.0 42.3↑11.1·DeepSWE 77.0·“许愿式编程”端到端生成) ② Meta Muse Wonder / Muse Wonder Full 发布"
            "(10/12·AA智能指数56·SWE-Marathon 57.5%超越Opus 5.5与GPT-6 Astra·幻觉率仅23%) ③ REA 成为 GitHub 周榜第一"
            "(MCP逆向分析·周增24.9万星)。评分含推算值，已在 scoring_guide 标注口径")
if old_desc:
    d = d[:old_desc.start()] + 'description: ' + js(new_desc) + d[old_desc.end():]
    print('✅ 评分表 description 已更新')

# ============ 2) 评分表：V4.1 Flash → V4.1-Flash-1017 ============
old_entry = re.search(r'\{name:"DeepSeek V4\.1 Flash".*?\n    \},', d, re.S)
new_entry = '''{name:"DeepSeek V4.1-Flash-1017", emoji:"🐳", provider:"DeepSeek", series:"V4.1 迭代版(10/17)", tier:"🆕 开源旗舰·Agent优化",
     input_price:"¥1.00/¥2.00(缓存未命中)", output_price:"¥4.00/¥8.00(闲时/高峰)", cost_per_task:"≈$0.02",
     intelligence:87, speed:92,性价比:97, 安全:86, 综合:91,
     context:"1M(输出上限384K)", params:"5520亿MoE(激活:输入80亿/输出160亿)",
     strengths:"10/17 上线·代码/Agent/视觉全面提升：Terminal-Bench 4.0 42.3(+11.1)·ProgramBench 29.1(+8.8)·HLE 42.6(+5.8)·DeepSWE v1.1 77.0·Automation-Bench 60.5·NL2Repo 68.2·官方称为“性能—费用帕累托改进”(同时降延迟与输出长度)·“许愿式编程”带自反馈RL可端到端生成可运行项目·原生视觉·1M上下文+384K输出·MIT开源",
     weaknesses:"基准为官方自测(harmess 不同不可直接拼排名)·知识广度仍是短板·中文长文写作未验证·输出仍偏长·生态适配仍在完善",
     best_for:"日常主力(替代V4-Flash)·仓库级代码修改·多步Agent任务·多模态编程·联网检索流程·成本敏感+隐私场景·本地部署",
     price_note:"🆕 10/17 上线：模型名仍为 deepseek-flash，旧名 deepseek-v4-flash 自动路由到新版。闲时输入¥1/输出¥4·高峰(工作日9-12/14-18)输入¥2/输出¥8·缓存命中输入¥0.02/¥0.04。MIT开源可本地部署",
     free_tier:"✅ MIT开源·HuggingFace/ModelScope可下载·官网免费"
    },'''
if old_entry:
    d = d[:old_entry.start()] + new_entry + d[old_entry.end():]
    print('✅ 评分表 V4.1-Flash-1017 条目已重写')

# ============ 3) 评分表：追加 Meta Muse Wonder / Full ============
meta_models = '''
    // ===== Meta Muse 系列（2026-10-12 新增）=====
    {name:"Meta Muse Wonder", emoji:"🌀", provider:"Meta", series:"Muse · 标准版", tier:"🆕 长任务编程新秀",
     input_price:"$4.00(¥28)", output_price:"$20.00(¥140)", cost_per_task:"≈$0.08",
     intelligence:80, speed:78,性价比:68, 安全:85, 综合:76,
     context:"1M", params:"未公开",
     strengths:"SWE-Marathon 53.1%·DeepSWE v1.1 78.8%(超GPT-6 Astra 74.1%)·Terminal-Bench 4.0 57%·Coding Agents Index 63·Active Memory(长会话记住偏好与约束)·Active Focus(遇阻主动换策略并自检)·原生多模态(文本/高分辨率图/超长视频/连续音频)·1M上下文不加价",
     weaknesses:"AA知识指数偏低(约30)·幻觉率23%的代价是拒答变多·API价格中上($4/$20)·中文场景未验证·生态刚起步·总量数据均来自第三方测评",
     best_for:"长任务编程·多文件仓库修改·需反复运行验证的Agent工作·专业工作(金融/法律)·超长上下文分析",
     price_note:"2026-10-12 发布·输入$4/输出$20 每百万token·缓存输入$0.20·1M上下文不额外加价·Meta Model API 与 Muse Code 均已上线",
     free_tier:"❌ 无免费额度"},
    {name:"Meta Muse Wonder Full", emoji:"🌌", provider:"Meta", series:"Muse · 高配版", tier:"专业工作旗舰",
     input_price:"订阅制($50/$200每月)", output_price:"含在订阅内", cost_per_task:"按订阅折算",
     intelligence:84, speed:72,性价比:60, 安全:88, 综合:74,
     context:"1M", params:"未公开",
     strengths:"AA智能指数56(与Claude Sonnet 5.5并列·上代Spark 1.3为48·六周涨8分)·SWE-Marathon 57.5%(超Opus 5.5 11.2pt)·Harvey法律LAB-AA 13.1分(Opus 5.5的3.1倍)·幻觉率仅23%(Astra 51%/Opus 59%)·ProofBench输出token少40%(450万→270万)·解题步骤120→62·Vals综合64.57排第五(超所有OpenAI模型)",
     weaknesses:"无独立API(仅 Muse Code 订阅)·知识广度低于Astra(43)与Opus(46)·订阅制无法按量弹性·$50/月起门槛·价格折算成本高",
     best_for:"高置信度专业工作(法律/合规/金融)·超长任务软件开发·对幻觉零容忍的场景·需要少token完成复杂推理",
     price_note:"⚠️ 仅通过 Muse Code 订阅开放：Power $50/月(基础档20倍用量) / Maximum $200/月(80倍)·独立API未公布时间表",
     free_tier:"❌ 无免费额度"}'''
# 插到 models 数组末尾（最后一个 } 之后、] 之前）
i_comp = d.find('var AI_MODEL_COMPARISON')
m_open = re.search(r'models:\s*\[', d[i_comp:])
i_arr = i_comp + m_open.end()
depth, k = 1, i_arr
while k < len(d) and depth > 0:
    if d[k] == '[': depth += 1
    elif d[k] == ']': depth -= 1
    k += 1
i_arr_end = k - 1   # 指向 ]
# 在 ] 之前插入
seg = d[i_arr:i_arr_end]
d = d[:i_arr] + seg.rstrip() + ',\n' + meta_models + '\n  ' + d[i_arr_end:]
print('✅ 评分表已追加 Meta Muse Wonder / Muse Wonder Full（共 16 个模型）')

# ============ 4) 评分表：key_takeaways ============
old_kt = re.search(r'key_takeaways:\s*\[[\s\S]*?\n  \],', d)
new_kt = '''key_takeaways: [
    "🔍 本周最强信号: REA(morluto/rea)登 GitHub 周榜第一——29万星/周增24.9万·MCP 把逆向分析工具交给 Agent→Agent 竞争点从「能不能写代码」移到「能不能稳定完成一套工程动作」",
    "🛠️ Agent 三层分工成型: MCP 暴露工具 / Skill 教 Agent 何时调用 / CLI 供人直接用——REA 是这个范式的教科书案例·面试高频题",
    "🐳 DeepSeek V4.1-Flash-1017: Terminal-Bench 4.0 42.3(+11.1)·ProgramBench +8.8·同时降延迟与输出长度→竞争从「榜单分数」转向「完成任务要多少时间/输出/工具调用」",
    "🌌 Meta Muse Wonder Full: AA智能指数56(六周+8)·SWE-Marathon 57.5%超Opus 5.5 11pt·幻觉率仅23%(Opus 59%)→高置信度专业工作首次有国产外替代",
    "⚖️ 幻觉率是双刃剑: Muse Full 23%靠的是「不确定就拒答」·但知识指数仅30(Astra 43/Opus 46)→合规场景选它·广度问答仍选Opus/Astra",
    "💰 价格时段化: deepseek-flash 高峰(工作日9-12/14-18)输入¥2/输出¥8·闲时减半→批量任务排到夜间可省一半",
    "🆓 Search/Fetch 免费用: DeepSeek Search/Fetch 每千次成功请求¥5·2026-11-01 前通过 Harness/Claude Code/Codex 调用暂不收费·5 QPS 限制",
    "🎯 选型策略: 日常主力 DeepSeek V4.1-Flash-1017(91分)·长任务编程 Meta Muse Wonder·高置信度专业工作 Muse Full·多模态 GLM-5.3-Flash·本地隐私 Qwen3.8-27B"
  ],'''
if old_kt:
    d = d[:old_kt.start()] + new_kt + d[old_kt.end():]
    print('✅ 评分表 key_takeaways 已更新')

# ============ 5) 评分表：price_adjustments 追加 ============
m_pa = re.search(r'price_adjustments:\s*\[\s*\n', d)
if m_pa:
    add = '''    {model:"DeepSeek V4.1-Flash-1017", date:"2026-10-17", change:"🆕 上线·代码/Agent/视觉全面提升且同时降延迟与输出长度", reason:"官方称「性能—费用帕累托改进」：Terminal-Bench 4.0 42.3(+11.1)、ProgramBench 29.1(+8.8)、HLE 42.6(+5.8)、DeepSWE 77.0；带自反馈RL支持「许愿式编程」", impact:"模型名不变(deepseek-flash)旧调用自动升级·1M上下文+384K输出·MIT开源；竞争焦点从榜单分数转向「完成任务的时间/输出/工具调用数」"},
    {model:"Meta Muse Wonder / Full", date:"2026-10-12", change:"🆕 发布·AA智能指数56(Wonder Full)·六周自48涨8分", reason:"Meta 投入吉瓦级算力的 Prometheus 数据中心·14个月基础设施重构·用长周期多文件真实编程任务强化训练·搭载 Active Memory 与 Active Focus", impact:"SWE-Marathon 57.5% 超越 Claude Opus 5.5(46.3%)与 GPT-6 Astra(42.5%)·幻觉率23%(Astra 51%/Opus 59%)·Full 仅订阅制 $50/$200 每月·前沿模型竞争重回三强格局"},
    {model:"REA (morluto/rea)", date:"2026-10-11", change:"🆕 v6.4.0·GitHub 周榜第一(29万星·周增24.9万)", reason:"Reverse Engineer Anything：用 MCP 把应用/网页/二进制分析能力交给 Agent，本地运行、结果含证据与未知项", impact:"Agent 工具生态的分层范式落地(MCP工具/Skill流程/CLI直用)·逆向分析门槛大幅降低·同时带来授权与隐私边界问题(结果会进入Agent上下文)"},
'''
    d = d[:m_pa.end()] + add + d[m_pa.end():]
    print('✅ 评分表 price_adjustments 已追加 3 条')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])
