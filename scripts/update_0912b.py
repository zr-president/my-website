# -*- coding: utf-8 -*-
"""补插 AI_MODEL_COMPARISON 的 DeepSeek V4.1 Flash 行（上次判重条件过宽被跳过）"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
c = open(FP, 'r', encoding='utf-8').read()

if 'name:"DeepSeek V4.1 Flash"' in c:
    print('already inserted')
else:
    anchor = '''     free_tier:"✅ 完全免费(chat.deepseek.com)"
    },
'''
    if anchor not in c:
        print('ANCHOR MISS')
    else:
        v41 = '''     free_tier:"✅ 完全免费(chat.deepseek.com)"
    },
    {name:"DeepSeek V4.1 Flash", emoji:"🐳", provider:"DeepSeek", series:"V4.1新架构·原生视觉", tier:"🆕 开源旗舰(9/10发布)",
     input_price:"$0.30(峰值)", output_price:"$1.20(峰值·非峰值半价)", cost_per_task:"≈$0.02",
     intelligence:86, speed:90,性价比:96, 安全:86, 综合:91,
     context:"未公开(继承1M级)", params:"5520亿MoE(激活:输入80亿/输出160亿)",
     strengths:"9/10发布·多个benchmark超Claude Opus 5与GPT-5.6 Sol·原生视觉理解(图像输入)·AutomationBench-AA事务Agent性能超GPT-6 Astra拿第一·AA智能指数v4.3得40分(超GPT-5.6 Luna)·KV缓存token降至V4-Flash的1/3.9(显存1/4·存储1/8)·MIT开源可本地部署",
     weaknesses:"任务输出token偏多(比Claude Fable 5.1多·单任务成本未必最优)·速度略逊Gemini 3.8 Flash/Muse Spark 1.3·生态适配仍在完善",
     best_for:"日常主力升级(替代V4-Flash)·多模态任务(原生视觉)·Agent/自动化工作流·成本敏感+隐私场景·本地部署",
     price_note:"🆕 9/10发布·API大幅降价：峰值输入$0.3/缓存输入$0.006/输出$1.2·非峰值半价·MIT开源可免费本地部署",
     free_tier:"✅ MIT开源·HuggingFace/ModelScope可下载·官网免费"
    },
'''
        c = c.replace(anchor, v41, 1)
        open(FP, 'w', encoding='utf-8').write(c)
        print('OK inserted AI_MODEL_COMPARISON V4.1 Flash')

# 确认描述是否已更新
if 'DeepSeek V4.1 Flash发布(9/10' not in c:
    c = open(FP, 'r', encoding='utf-8').read()
    c = re.sub(r'description: "主流大模型全维度对比[^"]*"',
      'description: "主流大模型全维度对比 · 同系列区分(Flash/Pro/Luna/Sol/Max/27B/V4.1) · 百分制评分 · 综合加权评分 · 最新价格(含调价标注) · 每日更新 · 9/12更新：DeepSeek V4.1 Flash发布(9/10·5520亿MoE·原生视觉·超Opus5/GPT-5.6 Sol·MIT开源·API降价)+GPT-6 Astra(闭源·API $10/$50)"', c, count=1)
    open(FP, 'w', encoding='utf-8').write(c)
    print('OK description updated')
else:
    print('desc already ok')
