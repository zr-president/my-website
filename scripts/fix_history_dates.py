# -*- coding: utf-8 -*-
"""回退被误改的历史记录：
   - LEARN_PATHS.archive 的键（应为 2026-09-12，被误改成 2026-09-13）
   - AI_JUDGMENTS / AI_OBSERVATIONS 里 9/12 当天记录的 date
   同时补一条 9/13 的新观察（今日真正的更新）
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 归档键回退 ----------
before = d.count('"2026-09-13": [')
d = d.replace('"2026-09-13": [', '"2026-09-12": [')
print('✅ 归档键回退：%d 处 2026-09-13 → 2026-09-12' % before)

# ---------- 2) 判断/观察的 date 回退 ----------
c1 = d.count("date:'2026-09-13'")
d = d.replace("date:'2026-09-13'", "date:'2026-09-12'")
c2 = d.count('date:"2026-09-13"')
d = d.replace('date:"2026-09-13"', 'date:"2026-09-12"')
print('✅ 历史记录 date 回退：%d 处' % (c1 + c2))

# ---------- 3) 补一条 9/13 的新观察 ----------
# 找到 AI_OBSERVATIONS 的第一条，在其前插入
m = re.search(r'(var AI_OBSERVATIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[\s*\n)', d)
if m and "AI 产品岗能力要求" not in d:
    new_item = ("  {date:'2026-09-13', topic:'AI 产品岗能力要求从「会用工具」转向「会定义边界」',"
                " summary:'本周多个招聘需求显示，AI 产品岗的能力描述正从「熟悉大模型工具」转向「能判断什么该用/不该用模型、能定义验收标准与兜底路径」。'"
                " implication:'对转型者意味着：作品集里放一个「AI 功能 PRD（含异常与边界）」比放 Prompt 合集更有说服力。',"
                " tag:'求职'},\n")
    d = d[:m.end()] + new_item + d[m.end():]
    print('✅ 已补 1 条 2026-09-13 新观察')
else:
    print('SKIP 新观察（已存在或未找到锚点）')

open(FP, 'w', encoding='utf-8').write(d)
