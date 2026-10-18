# -*- coding: utf-8 -*-
"""更新资讯区 summary + 要闻第 7 张（AI→REA）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

news = ('<b>10月18日 AI 资讯速览</b>：<br>'
  '① <b>REA（Reverse Engineer Anything）</b>登 GitHub 周榜第一——总星 29.1 万、周增 24.9 万，'
  'MCP 服务器形式把应用/网页/二进制分析交给 Agent，官方要求输出含证据与未知项；v6.4.0（10/11）。<br>'
  '② <b>DeepSeek-V4.1-Flash-1017</b>（10/17）上线——Terminal-Bench 4.0 42.3(+11.1)、ProgramBench 29.1(+8.8)、'
  'DeepSWE 77.0；模型名仍为 deepseek-flash，旧调用自动升级；1M 上下文 + 384K 输出。<br>'
  '③ <b>DeepSeek Harness 0.2.1-rc.2</b>（10/17）——适配新模型与 Search/Fetch API；'
  'Search/Fetch 每千次成功请求 ¥5，11/1 前通过 Harness 调用免收，账户级 5 QPS。<br>'
  '④ <b>Meta Muse Wonder / Full</b>（10/12）——AA 智能指数 56（六周 +8），'
  'SWE-Marathon 57.5% 超 Opus 5.5 与 GPT-6 Astra，幻觉率 23%（Opus 59%），Full 仅订阅制。<br>'
  '⑤ <b>A股</b>：10/8 开市至今 7 个交易日，国庆前三个观察点可开始验证；10 月下旬三季报密集披露。<br>'
  '⑥ <b>游戏</b>：影之刃零 10/29 发售，倒计时 11 天。<br>'
  '⑦ <b>生活</b>：广州入秋转折期，白天 28-30C、夜间 22-24C，温差 6-8C。')

i = d.find('var INSIGHTS = {')
e = i + re.search(r'\n\};', d[i:]).end()
seg = d[i:e]
pat = re.compile(r'((?:"news"|news)\s*:\s*\{)([\s\S]*?)(\n  \})')
m = pat.search(seg)
ok = False
if m:
    body = m.group(2)
    sm = re.search(r'("?summary"?\s*:\s*)(?:"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', body)
    if sm:
        nb = body[:sm.start()] + sm.group(1) + json.dumps(news, ensure_ascii=False) + body[sm.end():]
        seg = seg[:m.start()] + m.group(1) + nb + m.group(3) + seg[m.end():]
        ok = True
d = d[:i] + seg + d[e:]
print('资讯区 summary:', 'OK' if ok else 'MISS')

# 要闻第 7 张
old_head = '"headline": "AI 跟踪从【每天看】转为【每两周复盘】：三个值得关注的信号"'
new_head = '"headline": "REA 登上 GitHub 周榜第一：一个 MCP 如何让 Agent「看懂」软件"'
if old_head in d:
    d = d.replace(old_head, new_head); print('要闻第7张标题: OK')
else:
    print('要闻第7张标题: MISS')

old_sum = ('9-10 月跟踪的两条线（DSH 桌面端、Jev 决策模型）结论未变：DSH 继续用网页版，Jev 现在不接入。'
           '这类基础设施型变化不需要每天盯，每两周看一次足够。三个值得关注的信号：'
           '① 桌面端是否发布 rc → 正式版（正式版才值得重新评估）② Jev 是否出现带后端的产品案例（决定它的适用边界）'
           '③ PTC（程序化工具调用）是否成为 Agent 工程的主流做法。')
new_sum = ('REA（Reverse Engineer Anything）以 29 万星登 GitHub 周榜第一，周增 24.9 万。'
           '它本质是一个 MCP 服务器：让 Agent 能读应用、网页、二进制，并给出证据位置。'
           '最值得学的不是「逆向」这个用途，而是它的三层分工——MCP 提供工具、Skill 提供调查流程、CLI 提供人工入口。'
           '这是 2026 下半年 AI 产品设计最值得记住的结构。另附：DeepSeek-V4.1-Flash-1017（10/17）你已经在用（模型名仍为 deepseek-flash）；'
           'Meta Muse Wonder Full 幻觉率仅 23%，但知识广度偏低。')
if old_sum in d:
    d = d.replace(old_sum, new_sum); print('要闻第7张正文: OK')
else:
    print('要闻第7张正文: MISS')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:250])
