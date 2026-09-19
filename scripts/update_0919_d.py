# -*- coding: utf-8 -*-
"""更新第四步：WEBSITE_GUIDE 摘要 + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.16。9/19（周六）更新：健身增肌计划第1周复盘（俯卧撑已加负重，下周起按「每周只推一项」加重）；'
       'A股改为周复盘口径（3900关反复争夺 · AI硬件仍为结构主线 · 9/11判断已获验证）；'
       'AI动态追踪补入开源模型量化与私有化部署进展；每日一词与小白课堂全量刷新（跨健身/AI/运营/财经/学习/求职/生活七个领域）。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-19（周六 · 跨 5 天全量更新 · v1.8.16）
- **读取系统时钟确认日期为 2026-09-19**，站点原内容停在 9/14 → 落后 5 天（含 9/14-9/18 完整交易周）
- **今日要闻**：8 张卡（增肌第1周复盘 / A股周复盘 / V4.1 Flash 开源生态 / 求职 JD 变化 /
  Agentic Workflow / 饮食执行 / 动漫倒计时 / 秋分生活）
- **A股分区重写为周复盘口径**：4200→ 改为「9/14-9/18 周复盘 + 9/21 起预案」
  含 9/11 判断的验证结论（AI 硬件是结构主线 ✅ 成立）、量能作为关键观察变量、3900 关口的多空分歧
- **每日一词**：10 词跨 5 领域（健身/财经/AI/运营/营养/学习/生活/求职）
- **小白课堂**：10 条跨 7 领域，旧 10 条归档为 2026-09-14；current_day 8 → 13
- **今日待办**：5 条周六版（周复盘 / 体重校准 / 补训练平台进度 / 验证股市判断 / 补番）
- **时间敏感数字**：Re:Zero 追番第 33→38 天、倒计时 16→11 天
- **内容新鲜度审计**：17 个分区的内容日期全部不落后于当日（stock 由 9/14 修正为 9/21）
- 版本 1.8.15 → 1.8.16（三处同步）

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
