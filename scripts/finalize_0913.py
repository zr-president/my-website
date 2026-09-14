# -*- coding: utf-8 -*-
"""更新 WEBSITE_GUIDE.summary + 追加 changelog"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

# ---------- 1) WEBSITE_GUIDE.summary ----------
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old_sum = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new_sum = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
           '版本1.8.14。9/13：健身方案从【减脂露腹肌】调整为【增肌+腹肌双目标】——'
           '判断为瘦胖子体型（170cm/59kg·体脂15-18%），改增肌为主、新增练腿、跳绳减量、'
           '热量转轻微盈余；饮食同步改为训练日2500/休息日2300；每日一词与小白课堂全量刷新为增肌专题。"')
if old_sum:
    d = d[:old_sum.start()] + new_sum + d[old_sum.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('OK WEBSITE_GUIDE.summary 已更新')
else:
    print('MISS WEBSITE_GUIDE.summary')

# ---------- 2) changelog ----------
CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-13（健身方案转向增肌 · v1.8.14）
- **健身区重构**：从「8周腹肌专项（减脂向）」改为「增肌 + 腹肌 双目标（增肌向）」
  - 核心判断：170cm/59kg·体脂15-18% = 瘦胖子，体脂率偏高源于肌肉少而非脂肪多
  - 新增三条路线对比表（继续减脂 / 放开增肌 / 增肌+控脂 的 12 周结果）
  - 新版周计划：4 力量日 + 1 有氧日（新增下肢训练，原来完全没有）
  - 跳绳从 3-4 次/周减到 1-2 次/周（避免干扰效应）
  - 新增渐进超负荷方案：俯卧撑必须加负重（自重 60 个已完全适应）
  - 新增 6 指标追踪表 + 12 周后策略切换判断表
- **饮食区对齐**：热量从轻缺口（2300）改为训练日 2500 / 休息日 2300，蛋白 110-130g；
  修复原饮食页（2600-2800）与健身页（2300-2500）热量互相矛盾的问题
- **INSIGHTS**：fitness / diet 两条洞察全量重写，updated → 2026-09-13
- **每日内容**：今日要闻 8 张卡（含健身方案调整）、每日一词 10 条（增肌专题）、
  小白课堂 10 条（增肌/营养原理），旧 10 条归档为 2026-09-12
- 样式新增 `.wk-day.legs`（下肢训练日配色）；版本三处同步 1.8.13 → 1.8.14

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('OK changelog 已追加 2026-09-13 条目')

# ---------- 3) 清理备份 ----------
import os
for f in ['daily_data.js.bak']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p); print('已删除', f)
