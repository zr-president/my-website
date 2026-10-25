# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.34。10/25（周日）更新：① <b>隐私脱敏</b>——公开内容里的健康诊断名称（甲状腺结节 / 肾结石）'
       '全部移除，改为中性的「低草酸」「易结石体质」表述，实用建议（饮水 2.5L、草酸、复查周期）完整保留；'
       'personal_config.js 里页面从未使用的健康字段已删除。'
       '② <b>内容</b>——10 月最后一个交易周与三季报 10/31 截止；影之刃零倒计时 4 天；'
       '健身改版第 8 天（自检 RIR）；求职算反馈率；10 月只剩 6 天该收尾；'
       '本周 AI 侧记录「用 Astra 做方案评审」这次实践。17 个分区三字段全部刷新。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-25（周日 · v1.8.34）隐私脱敏 + 内容更新
### 一、隐私脱敏（响应 Codex/Astra 审查报告的 P0 发现，并做了扩大处理）
- **核实结果**：报告指出的 `personal_config.js` 确实含健康字段且线上 HTTP 200 可访问
- **但问题范围更大**：诊断名称同时出现在 4 个公开文件
  | 位置 | 内容 | 线上 |
  |---|---|---|
  | `daily_data.js` | 甲状腺结节 ×2 | HTTP 200 |
  | `detail_content.js` | 饮食页副标题写明诊断 | HTTP 200 |
  | `index.html` | 生活助手 system prompt + 健康提醒 | 公开 |
  | `personal_config.js` | dietary 数组（页面从未使用） | HTTP 200 |
- **处理原则**：保留实用建议，去掉诊断名称
  - `肾结石·甲状腺结节·增肌食谱` → `低草酸·高蛋白·增肌食谱`
  - `🦋 甲状腺结节：不需要限碘…` → `🦋 饮食注意：无需限碘…`
  - `肾结石患者夏天怎么喝水` → `易结石体质夏天怎么喝水`
  - `肾结石` → `结石风险` / `易结石体质`（保留饮水、草酸、复查等全部建议）
- **结果**：甲状腺 0 处、肾结石 0 处残留
- **`personal_config.js`**：删除 `height_cm` / `weight_kg` / `dietary` / `fitness_goal` / `fitness_week`（页面从未使用，纯死数据）
- ⚠️ **遗留**：Git 历史（2 个提交：`c7e7595`、`5f51fdb`）仍含旧字段。公开仓库可翻历史，需 force push 才能彻底清除——未执行，等确认

### 二、内容更新（落后 5 天）
- **今日要闻 8 卡**：10 月最后交易周 + 三季报 10/31 截止 / 影之刃零倒计时 4 天 /
  健身改版第 8 天 / 求职算反馈率 / 10 月收尾 / Astra 方案评审实践 / 秋季新番第 6 周 / 广州深秋作息
- **每日一词 10 条 / 10 领域**：模型分工 · 执行隔离 · 分母口径 · 力竭距离(RIR) · 业绩预告修正 ·
  初筛通过率 · 机会成本 · 收尾效应 · 光照锚定 · 方案评审
- **小白课堂 10 条 / 10 领域**（旧归档为 2026-10-20，current_day 26 → 27）
- **今日待办 5 条**：三季报写死结论 / 算反馈率 / 第 8 天 RIR 自检 / 写 Astra 评审素材 / 10 月收尾
- **17 分区推进**：交易日 9 → 12、倒计时 9 → 4 天、增肌第 31 → 36 天、连载 73 → 78 天、
  新番第 5 → 6 周、本月已过 20 → 25 天

### 三、核查
- 一致性检查：22 项通过（0 提醒）
- 逐字段审计：summary / trend / tip 三字段均不落后
- 视觉体检：30/30
- 渲染验证：2026-10-25 / 倒计时 4 天 / 12 个交易日 / 第 8 天 / 1.8.34 均正常
- **健康字段渲染检查：甲状腺 ✅已清除 / 肾结石 ✅已清除**
- 版本 1.8.33 → 1.8.34

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

for f in ['daily_data.js.bak', 'index.html.bak', 'personal_config.js.bak']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p); print('已删除', f)
