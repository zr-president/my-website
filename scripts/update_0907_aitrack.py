# -*- coding: utf-8 -*-
"""补替换 INSIGHTS["ai-track"]（带引号键）"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
content = open(FP, 'r', encoding='utf-8').read()

def esc(v):
    return v.replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")

def replace_section(key, verdict='', summary='', trend='', tip='', reasoning=''):
    global content
    m = re.search(r'(?m)^  ' + re.escape(key) + r':\s*\{', content)
    if not m:
        print('MISS:', key); return
    i = m.start(); j = i; depth = 0; L = len(content); inq = False; q = ''
    while j < L:
        ch = content[j]
        if inq:
            if ch == q: inq = False
            elif ch == '\\': j += 1
        elif ch in ("'", '"'):
            inq = True; q = ch
        elif ch == '{': depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    end = j + 1
    while end < L and content[end] == ',': end += 1
    lines = ['  ' + key + ': {']
    for k, v in [('verdict', verdict), ('summary', summary), ('trend', trend), ('tip', tip), ('reasoning', reasoning)]:
        if v: lines.append("    " + k + ": '" + esc(v) + "',")
    lines.append("    updated: '2026-09-07'")
    lines.append('  },')
    content = content[:i] + '\n'.join(lines) + content[end:]
    print('OK', key)

replace_section('"ai-track"',
 verdict='🎯 今日结论：① 头条是【GPT-6 Astra开启新叙事】——模型竞争从Coding转向长程Agent/Computer Use，『任何你能在电脑上完成的事，Astra都替你完成』；② 用10万卡训练(Stargate德州站)+Recurrent Depth架构(层复用/隐空间推理)+API价每百万输入$10输出$50(比5.6Sol贵约2.5倍)——OpenAI重上高位定价，靠单任务成本低而非token便宜；③ 国产模型差距在长程任务/Computer Use执行层；④ 对工具链：GPT-6闭源贵，你的DeepSeek/Qwen/GLM+本地部署路线不变；⑤ 行动：把GPT-6新叙事写进行业观察+面试谈资，跟踪算力硬件(CPO/光通信)。',
 summary='9月7日 AI 行业焦点：(1)【GPT-6 Astra新叙事】——9/3发布，被称『最智能最对齐』旗舰，模型竞争从Coding转向长程Agent/Computer Use（电脑操作/端到端任务交付）；发布9小时浏览量3600万，创OpenAI自Sora以来之最；(2)【技术/成本】——Stargate德州站10万卡训练、Recurrent Depth架构(层复用+隐空间推理)、API价每百万输入$10输出$50比5.6Sol贵约2.5倍，但强调单任务成本更低(Terminal-Bench比Sol低9%、比Fable 5.1低63%)；(3)【国产差距】——国产模型日常任务已不弱，但长程Agent/Computer Use执行层是短板；(4)【算力国产化】——北京AI产投基金入股3D算力芯片商算苗科技，注册资本增至134.96万元，地方算力基金持续加码。',
 trend='9月AI趋势：(1)**GPT-6新叙事**——模型竞争从『聊天/写代码』转向『端到端执行』，Computer Use与长程Agent成新主线，能力从对话框扩展到真实工作流(填表/更新CRM/管理日历/建网站/前端QA)；(2)**竞争格局**——OpenAI在Coding追近Anthropic(回到胶着)，模型市场分层：旗舰做复杂任务、中端覆盖多数生产、小模型高频调用；(3)**算力长逻辑**——10万卡训练+Agent/Computer Use推理需求→算力需求长期强化，A股算力硬件(CPO/光通信/芯片)情绪兑现；(4)**国产追赶**——国产日常能力强但长程执行短板，差距在执行层而非所有维度；(5)**安全监控**——Recurrent Depth推理难监控，OpenAI额外投20%推理算力监控→AI安全/可解释性成新话题。',
 tip='今日AI追踪行动：(1)**30秒讲清GPT-6新叙事**——从"Coding"到"端到端Agent/Computer Use"：Astra能填表/更新CRM/管理日历/在线研究→『任何你在电脑上能做的事Astra都能做』→理解模型竞争主线之变；(2)**写300字行业观察**——《GPT-6新叙事：从Coding到任务交付》→本周作品集核心篇；(3)**求职联动**——AI Agent/Computer Use产品岗需求上升，讲清"自动化价值/长程任务"是加分；(4)**算力国产化**——北京AI产投投算苗科技→跟踪国产算力芯片/CPO/FAU无源光器件/半导体设备(量测/探针台)；(5)**工具链**——GPT-6闭源贵($10/$50)不用，DeepSeek/Qwen/GLM+本地路线不变。',
 reasoning='🔍 发生了什么？\nGPT-6 Astra 9/3发布，模型竞争从Coding转向长程Agent/Computer Use；10万卡训练、Recurrent Depth架构、API价$10/$50；国产模型差距在长程执行层；北京AI产投入股算苗科技。\n\n🤔 对AI行业意味着什么？\n① 竞争主线从"Coding"到"任务交付"——会编程≠能完成工作\n② OpenAII重上高位定价，靠单任务成本低而非token便宜\n③ 模型市场分层：旗舰/中端/小型各有定位\n④ 国产差距在执行层——长程Agent/Computer Use需补\n\n📊 术语解释\nComputer Use：电脑操作——模型直接操作系统界面/浏览器/办公工具\nRecurrent Depth：循环深度架构——同一组Transformer层反复调用，推理在隐空间完成\n端到端任务：从需求到交付的完整工作流，而非单点回答\n\n💡 对你的启示\n① GPT-6新叙事是当下最热的AI话题，写进观察+面试\n② 模型竞争转向任务交付→AI产品/Agent岗需求上升\n③ 算力硬件=GPT-6主线，A股CPO/光通信/芯片值得跟踪')
open(FP, 'w', encoding='utf-8').write(content)
print('ai-track done')
