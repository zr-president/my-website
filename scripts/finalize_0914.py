# -*- coding: utf-8 -*-
"""追加 changelog + 清理备份"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-14（修正日期滞后 · 周一 · v1.8.15）
- **根因修复**：此前"每日更新"是拿【上次内容日期 +1】推算，从未读取系统时钟
  → 站点长期比真实日期滞后（本次发现 9/14 时站点仍是 9/13）
- 新增 `scripts/update_today.py`：从【系统时钟】取日期，同步全站 26 个日期字段
  （17 个 INSIGHTS 分区 + 要闻/词汇/课堂 + 市场情绪/决策单/机会雷达/判断台账/工具链/影片）
- 一致性检查新增两项硬校验：
  ① 站点日期必须等于系统真实日期（不等则报错）
  ② 归档键必须是历史日期，不得与当日相同
- 周一语境调整：待办改为训练日/Day1 开练/A股开盘验证；要闻 A股卡改"上周五收 3888.11"口径；
  学习摘要「9月13日（周日）」→「9月14日（周一）」；动漫倒计时 16 天/追番第 33 天
- 前序（同日早些时候）：
  - 统一跨板块口径：食谱只保留饮食区一份权威版，健身区改为要点+指向；新增 check_consistency.py
  - 修正内容过于单一：每日一词/小白课堂恢复全领域分布（健身3+AI3+运营2+财经1+…）
  - 健身方案转向增肌（+腹肌双目标）、饮食热量口径对齐
- 版本 1.8.14 → 1.8.15

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('OK changelog 已追加')

for f in ['daily_data.js.bak', 'detail_content.js.bak']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p); print('已删除', f)
