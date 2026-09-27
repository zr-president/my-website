# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.19。9/27（周日）更新：围绕国庆假期做复盘与规划——'
       '假期安排（9/28-9/29 节前最后两个交易日、10/1-10/7 休市）；A股 3900 关口第三周收官与节前仓位；'
       '增肌计划第2周收官与第3周准备；求职方面把材料准备放假期、投递放节后；'
       '并给出假期【最低维持量】策略（每天40分钟，维持节奏优于集中冲刺）。'
       '每日一词与小白课堂刷新为各 10 个领域（多模态/本地优先/RFM分层/仓位管理/间隔重复/灰度发布等）。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-27（周日 · v1.8.19）国庆假期前的复盘与规划
- **读取系统时钟**确认为 2026-09-27（周日），站点原内容 9/26 → 落后 1 天，内容实质刷新
- **今日要闻 8 卡**：假期安排（9/28-9/29 节前最后两个交易日 / 10/1-10/7 休市）·
  A股 3900 第三周收官与节前仓位 · 增肌第2周收官与第3周准备 · Re:Zero 倒计时3天 ·
  求职（材料放假期/投递放节后）· AI 一周回顾（DSH 桌面端 + Jev）·
  假期学习最低维持量 · 假期作息与昼夜节律
- **每日一词 10 条 / 10 领域**：多模态 · 本地优先 · RFM分层 · 增肌平台期 · 仓位管理 ·
  秋招节奏 · 流动性分层 · 间隔重复 · 假期综合征 · 灰度发布
- **小白课堂 10 条 / 10 领域**：多模态为何是分水岭 / 本地优先是产品选择 /
  RFM 三维分层 / 平台期先查吃与睡 / 留现金也是仓位 / 秋招节奏 /
  钱按"什么时候用"分层 / 间隔重复 / 假期综合征 / 灰度发布；旧 10 条归档为 2026-09-26
- **今日待办 5 条**：国庆前三线复盘 / 第2周体重校准 / 决定节前仓位 /
  定假期最低维持量（每天40分钟）/ 增肌第3周计划
- **修正内容过时**：stock 与 ai-track 补 9/27 当日框架（stock 改为 9/22-9/26 周复盘 + 9/28-9/29 预案）
- 内容新鲜度：17 个分区全部不落后；一致性检查 22 项通过
- 版本 1.8.18 → 1.8.19

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
