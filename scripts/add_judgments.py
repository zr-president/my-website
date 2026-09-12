# -*- coding: utf-8 -*-
"""突破一：新增 AI_JUDGMENTS 判断台账（主题+我的判断+时间+验证结果+准确率）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

if 'var AI_JUDGMENTS' in c:
    print('已存在，跳过')
else:
    anchor = 'var AI_OBSERVATIONS = ['
    new = """// ===== 我的 AI 判断台账（突破一：把信息消费转为能力资产）=====
// 每条 = 主题 + 我的判断(可验证的预测) + 判断日期 + 验证日期 + 结果 + 证据
// 渲染时合并内置示例 + 用户本机自记(localStorage: myJudgments) → 自动算准确率
var AI_JUDGMENTS = {
  updated: "2026-09-12",
  items: [
    {date:'2026-09-07', topic:'开源模型追平闭源旗舰', judgment:'我判断：3-6个月内，开源模型会在主流benchmark追平闭源旗舰（Opus/GPT系列），且保持成本优势', verifyDate:'2026-12-07', status:'已验证', result:'正确', evidence:'9/10 DeepSeek V4.1 Flash 发布——多个benchmark超Claude Opus 5与GPT-5.6 Sol，MIT开源、API峰值$0.3/$1.2，验证了判断（比预期更快）'},
    {date:'2026-09-04', topic:'GPT-6会引爆AI安全治理议题', judgment:'我判断：GPT-6 Astra（8月因安全暂停）发布后，"AI安全治理"会从技术圈话题变成行业/政策议题', verifyDate:'2026-09-11', status:'已验证', result:'正确', evidence:'9/9-9/11 美国加州签署AI安全法案（Anthropic/OpenAI支持）；OpenAI系统卡披露推理可监控性下降引发安全研究者关注——安全治理确实进入政策议程'},
    {date:'2026-09-11', topic:'AI硬件是A股结构主线', judgment:'我判断：AI硬件（覆铜板/元件/光通信）在普跌行情中会持续跑赢，是政策+涨价双驱动的结构主线', verifyDate:'2026-09-18', status:'待验证', result:'', evidence:'9/11 覆铜板+4.31%/元件+1.80%/MLCC+1.76% 逆势走强（沪指-1.18%），初步验证中'},
    {date:'2026-09-12', topic:'V4.1 Flash将拉低Agent应用成本', judgment:'我判断：V4.1 Flash（KV缓存降至1/3.9+API降价）会让Agent/自动化应用的推理成本显著下降，2026Q4会出现更多低价Agent产品', verifyDate:'2026-12-12', status:'待验证', result:'', evidence:'V4.1 Flash AutomationBench-AA 超 GPT-6 Astra 拿第一（事务Agent）；Agents API 标准化中'},
    {date:'2026-09-12', topic:'AI Agent岗位需求将上升', judgment:'我判断：6个月内"AI Agent产品/应用"相关岗位需求会明显上升（OpenAI Agents API标准化+Agent-Native模型出现）', verifyDate:'2027-03-12', status:'待验证', result:'', evidence:'OpenAI Agents API公开测试；无问芯穹发布Agent-Native模型NeoHorse；招聘侧待观察'}
  ]
};

"""
    if anchor in c:
        c = c.replace(anchor, new + anchor, 1)
        open(FP, 'w', encoding='utf-8').write(c)
        print('OK AI_JUDGMENTS 已插入')
    else:
        print('ANCHOR MISS')
