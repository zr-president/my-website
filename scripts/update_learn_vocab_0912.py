# -*- coding: utf-8 -*-
"""小白课堂 archive 迁移 + 换新10课；每日一词换新10词（9/12 版）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 提取旧 items（9/6 的 10 课）----------
m = re.search(r'(?m)^var LEARN_PATHS = \{[\s\S]*?items:\s*\[([\s\S]*?)\n  \],', c)
if not m:
    print('MISS items'); sys.exit()
old_items = m.group(1).rstrip().rstrip(',')
print('旧items长度:', len(old_items))

# ---------- 2) 新 10 课 ----------
new_items = """    {section:"AI", emoji:"🐳", title:"DeepSeek V4.1 Flash 为什么能超过闭源旗舰？", content:"9/10 DeepSeek 发布 V4.1 Flash：5520亿参数 MoE（混合专家）模型，但每次只激活一小部分（输入80亿/输出160亿）——所以它既有大模型的能力，又有小模型的成本。关键是它换了新的预训练+强化学习方法，在多个测试上超过了 Claude Opus 5 和 GPT-5.6 Sol。类比：一家公司有5520个专家，但每个任务只叫最相关的80个人来干，又快又省。", takeaway:"MoE=参数大但激活少——这是开源模型能追平闭源旗舰的核心工程思路。"},
    {section:"AI", emoji:"👁️", title:"原生视觉理解是什么？AI能看图为什么是分水岭？", content:"原生视觉理解（Native Vision）=模型从训练起就能直接理解图像，而不是外挂一个OCR或图像识别模块。V4.1 Flash 这次就带了原生视觉。为什么重要：①你可以直接截图给AI看（分析网页/图表/穿搭/海报）；②多模态任务不再需要拼凑多个工具；③对产品经理意味着——能设计『看图干活』的AI功能。类比：以前是盲人摸象（靠文字描述），现在是睁眼看世界。", takeaway:"原生视觉=AI能直接看图——这是多模态应用（设计/电商/内容）的产品创新基础。"},
    {section:"AI", emoji:"💾", title:"KV缓存是什么？为什么它能让AI成本降到1/4？", content:"AI推理时，已经算过的内容会被存进『KV缓存』（Key-Value Cache），下次遇到相同前缀就不用重算——类似你写作业时参考自己之前的草稿。V4.1 Flash 把 KV 缓存的 token 数降到了上一代的 1/3.9，显存占用降到 1/4、存储降到 1/8。这意味着：同样的任务，AI 的算力/内存成本大幅下降。对使用者意味着：长时间对话、反复调用的Agent任务会便宜非常多。", takeaway:"KV缓存=AI的『草稿本』——缓存优化直接决定AI应用的成本天花板。"},
    {section:"AI", emoji:"🖥️", title:"Computer Use 是什么？AI替你操作电脑意味着什么？", content:"Computer Use（电脑操作）=AI 直接操控你的电脑界面：填表格、更新CRM、整理日历、上网查资料、写进文档、跑前端测试。GPT-6 Astra 的核心卖点就是这个——『任何你能在电脑上完成的事，Astra 都可以替你完成』。为什么是分水岭：以前AI只是『回答问题』，现在它开始『执行任务』——从回答者变成执行者。这也是模型竞争的新主线（取代了单纯的写代码能力）。", takeaway:"Computer Use=AI从『会回答』到『会干活』——竞争从Coding转向任务执行。"},
    {section:"AI", emoji:"🎯", title:"端到端任务交付 vs 单点回答——模型竞争主线为什么变了？", content:"过去比的是『写代码』『答题』这类单点能力；现在比的是『端到端完成任务』：理解需求→拆解步骤→调用工具→交付结果。原因很简单：会编程不等于能完成工作——编程只是高价值任务中的一环。GPT-6 和 V4.1 Flash 都在拼这个（AutomationBench 就是考『财务/人事等事务性Agent能不能真干完活』）。对求职的启示：会AI工具只是起点，能『用AI交付结果』才是竞争力。", takeaway:"竞争主线从『单点能力』到『端到端交付』——衡量标准变成了任务完成率。"},
    {section:"思维", emoji:"⚖️", title:"什么是『可验证的判断』？为什么判断力比信息量重要？", content:"可验证判断=你做出的、将来能明确判定对错的预测（而不是『我觉得AI很重要』这种无法验证的感想）。例：『我判断3-6个月内开源模型会在主流benchmark追平闭源旗舰』——有主题、有期限、有对错标准。为什么比信息量重要：信息谁都能搜到，但『持续做判断+验证对错』才能形成能力资产——你能拿出『我做过20个判断，准确率70%』这种别人没有的东西。方法：写下判断→设验证日期→到期复盘→归档。", takeaway:"判断力=可验证预测+事后复盘——这是把信息消费转为能力资产的唯一路径。"},
    {section:"股市", emoji:"📉", title:"A股失守3900怎么理解？放量下跌意味着什么？", content:"9/11 沪指跌1.18%收3888.11，失守3900，成交1.97万亿（比前一天多3247亿）——这是『放量下跌』。含义：①成交放大说明买卖双方都在积极出手，但卖方更强；②超4870只个股下跌、赚钱效应仅11%，是普跌而非结构性调整；③失守关键整数关口意味着短期人气受挫。对比：缩量下跌（没人接盘阴跌）通常不慌，放量下跌要谨慎等企稳。", takeaway:"放量下跌=抛压大于承接——失守关键位后要看能否快速收回。"},
    {section:"股市", emoji:"🔧", title:"覆铜板/元件为什么能在普跌中逆势上涨？", content:"覆铜板（CCL）是PCB（电路板）的上游材料，而PCB是AI服务器/光模块的基础。它逆势涨的两个原因：①**涨价链**——建滔积层板年内第七份涨价函、中国巨石电子布涨价15-20%，涨价直接改善利润预期；②**政策催化**——工信部《人工智能+软件》专项行动，AI硬件获政策支持。这就是『结构性主线』：大盘跌但它有独立逻辑（涨价+需求+政策）。", takeaway:"逆势上涨的板块往往有独立逻辑（涨价/政策/需求）——找主线要看逻辑不只看涨跌。"},
    {section:"健身", emoji:"🔥", title:"体脂率和腹肌的关系——为什么练腹≠有腹肌？", content:"腹肌人人都有，看不见是因为被脂肪盖住了。男性体脂率降到 12-15% 左右腹肌轮廓才会显现，10% 以下明显分块。所以：①狂练卷腹只让腹肌变厚，不减掉覆盖的脂肪；②局部减脂不存在（不能只减肚子）——必须整体降体脂；③59kg 的偏瘦体型（体脂约15-18%）不该靠饿（会掉肌肉更难看），而是『控脂+增肌』同步。类比：腹肌是埋在沙子里的石头，要挖掉沙子（减脂）才能看见。", takeaway:"腹肌可见度=体脂率决定——练腹只增厚，减脂才露出来。"},
    {section:"健身", emoji:"🪢", title:"HIIT（跳绳）为什么是减脂效率最高的训练之一？", content:"HIIT=高强度间歇训练（如跳绳30秒冲刺+30秒休息循环）。为什么高效：①单位时间热量消耗高（跳绳每小时约600-1000kcal）；②『后燃效应』（EPOC）——运动后身体仍在持续消耗热量；③省时间（15-20分钟=慢跑40分钟的效果）；④同时练心肺和协调。注意：①膝盖不适改无绳跳/开合跳；②落地用前脚掌、穿缓冲鞋；③每周3-4次别过量（关节需要恢复）。", takeaway:"HIIT=时间短消耗高+后燃效应——减脂期的时间效率之王。"}"""

# ---------- 3) 替换 items + archive 迁移 + current_day + updated ----------
c = c.replace(m.group(1), "\n" + new_items + "\n", 1) if False else c

# 用精确区间替换 items 内容
start = m.start(1); end = m.end(1)
c = c[:start] + "\n" + new_items + "\n" + c[end:]

# archive 迁移：在 archive: { 后插入 "2026-09-06": [旧items],
arch_m = re.search(r'archive:\s*\{\n', c)
if arch_m:
    ins = arch_m.end()
    c = c[:ins] + '    "2026-09-06": [\n' + old_items + '\n    ],\n' + c[ins:]
    print('OK archive 迁移 2026-09-06')
else:
    print('MISS archive')

# updated + current_day
c = re.sub(r'(var LEARN_PATHS = \{\s*\n\s*updated:\s*")[^"]*(")', r'\g<1>2026-09-12\g<2>', c, count=1)
c = re.sub(r'(current_day:\s*)6', r'\g<1>7', c, count=1)
print('OK LEARN_PATHS updated/current_day')

# ---------- 4) DAILY_VOCAB 换新10词 ----------
vstart = c.find('var DAILY_VOCAB')
vj = c.find('var AI_MODEL_COMPARISON', vstart)
new_vocab = """var DAILY_VOCAB = {
  date: "2026-09-12",
  words: [
    {emoji:"🧩", category:"AI", word:"MoE(混合专家模型)", definition:"一种大模型架构：总参数量很大（如5520亿），但每次推理只激活其中一小部分（如80亿）——所以既有大模型的能力，又有小模型的成本。类比:公司有5520个专家，每个任务只叫最相关的80人来干。", example:"DeepSeek V4.1 Flash 是5520亿参数MoE（激活输入80亿/输出160亿），在多个benchmark超过Claude Opus 5。", why_matters:"MoE是开源模型追平闭源旗舰的核心思路——面试聊模型架构必问。"},
    {emoji:"👁️", category:"AI", word:"原生视觉理解(Native Vision)", definition:"模型从训练起就内建图像理解能力，而不是外挂OCR/图像识别模块。类比:以前是盲人摸象（靠文字描述），现在睁眼看世界。", example:"V4.1 Flash 带回原生视觉——可直接截图给AI分析网页/图表/穿搭/海报。", why_matters:"原生视觉是多模态应用（设计/电商/内容）的产品创新基础。"},
    {emoji:"💾", category:"AI", word:"KV缓存(KV Cache)", definition:"AI推理时把已算过的内容存下来复用，避免重复计算——类似参考自己的草稿。缓存优化直接决定AI应用的成本。", example:"V4.1 Flash 把KV缓存token降到上一代1/3.9，显存占用1/4、存储1/8，API成本大幅下降。", why_matters:"长对话/Agent反复调用场景下，KV缓存=省钱的关键。"},
    {emoji:"🖥️", category:"AI", word:"Computer Use(AI操作电脑)", definition:"AI直接操控电脑界面完成任务：填表、更新CRM、整理日历、上网查资料、写文档、跑测试。从『回答问题』升级为『执行任务』。", example:"GPT-6 Astra 号称『任何你能在电脑上完成的事，它都能替你完成』——模型竞争从Coding转向Computer Use。", why_matters:"这是模型竞争的新主线，也是AI产品岗的新方向。"},
    {emoji:"🎯", category:"AI", word:"端到端任务(End-to-End Task)", definition:"AI从理解需求→拆解步骤→调用工具→交付结果的完整闭环，而不是只回答单点问题。衡量标准是『任务完成率』而非『回答准确率』。", example:"AutomationBench 专门测财务/人事等事务性Agent能否真正干完活——V4.1 Flash 在这项拿了第一。", why_matters:"会AI工具只是起点，能『用AI交付结果』才是竞争力。"},
    {emoji:"🔧", category:"金融", word:"覆铜板(CCL)", definition:"Copper Clad Laminate，PCB（电路板）的上游基材——用铜箔+树脂+玻璃布压合而成。AI服务器/光模块需求拉动+上游涨价会直接改善利润。", example:"9/11 A股普跌中覆铜板逆势+4.31%：建滔年内第七份涨价函+中国巨石电子布涨价15-20%。", why_matters:"理解产业链上游才能看懂『逆势上涨』背后的涨价逻辑。"},
    {emoji:"📉", category:"金融", word:"放量下跌", definition:"成交额放大但指数下跌——说明买卖双方都积极出手，但卖方更强、抛压大于承接。与『缩量下跌』（无人接盘阴跌）不同，需要更谨慎。", example:"9/11 沪指-1.18%成交1.97万亿（放量3247亿），超4870只个股下跌、赚钱效应仅11%。", why_matters:"量价配合是判断市场强弱的基础——放量下跌要看能否快速收回关键位。"},
    {emoji:"🔥", category:"健身", word:"体脂率(Body Fat Percentage)", definition:"脂肪占体重的比例。男性体脂12-15%左右腹肌轮廓显现，10%以下明显分块。腹肌人人都有，看不见是因为被脂肪覆盖。", example:"170cm/59kg 能摸出腹肌轮廓但仍有赘肉=体脂约15-18%，目标是降到12-15%。", why_matters:"腹肌可见度由体脂率决定——练腹只增厚，减脂才露出来。"},
    {emoji:"🪢", category:"健身", word:"HIIT(高强度间歇训练)", definition:"短时间高强度运动+短暂休息循环（如跳绳30秒冲刺+30秒休息）。特点是单位时间消耗高+『后燃效应』（运动后仍持续消耗热量）。", example:"跳绳HIIT每小时约600-1000kcal，15-20分钟≈慢跑40分钟效果——减脂期的时间效率之王。", why_matters:"减脂的核心是热量缺口，HIIT是效率最高的工具之一。"},
    {emoji:"⚖️", category:"思维", word:"可验证判断(Falsifiable Judgment)", definition:"有主题、有期限、能明确判定对错的预测（区别于『我觉得AI很重要』这种无法验证的感想）。方法：写下判断→设验证日期→到期复盘→归档。", example:"『3-6个月内开源模型追平闭源旗舰』——9/10 V4.1 Flash 发布即验证正确；累积判断+准确率=能力资产。", why_matters:"判断力比信息量稀缺——它能把信息消费转为可展示的能力资产。"}
  ]
};

"""
c = c[:vstart] + new_vocab + c[vj:]
print('OK DAILY_VOCAB 换新10词')

open(FP, 'w', encoding='utf-8').write(c)
print('done')
