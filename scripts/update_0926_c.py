# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.18。9/26（周六）更新：AI动态追踪改为双主题——①DSH 桌面端（9/25 官方预览版，Electron 复用同一套 Web UI，'
       '需实名认证+充值）与网页版的逐项对比及推荐（结论：继续用网页版）；②Jev 接入决策（结论：现在不接入，因尚无带后端的判断密集型系统）；'
       '另附 PTC 程序化工具调用为何能降低 Agent 延迟。每日一词与小白课堂刷新为 9/8 个领域；健身进入增肌第3周；A股 3900 关口第三周争夺。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-09-26（周六 · v1.8.18）DSH 桌面端对比 + Jev 接入决策
- **读取系统时钟**确认为 2026-09-26，站点原内容 9/23 → 落后 3 天，内容实质刷新
- **AI 动态追踪改为双主题**：
  - **① DSH 桌面端 vs 网页版**（9/25 官方预览版 V0.1.7-rc.1）：
    Electron 实现，复用现有 Web UI 与 Agent/会话/工具/插件逻辑（入口扩展而非能力分叉）；
    Win x64 + macOS arm64（已过 Apple 公证），暂无 Linux；
    与网页版最大差异：需充值 + **需实名认证**；新增四种 Agent 档位（标准/PTC/极简/创造）
    与可视化插件面板；任务式回答区显示 Token 数/工具调用次数/耗时
    → **推荐：继续用网页版**（实名隐私成本 / 求职期现金流 / 网页版已可完整访问本机工作区 / rc 预览版稳定性）
  - **② Jev 接入决策**：结论 **现在不接入**（目前无带后端的判断密集型系统）；
    给出三条接入时机条件（有后端产品 / 批量任务 / 判断成本敏感）
  - 附 **PTC（程序化工具调用）** 原理：用一段代码批量编排工具，把往返次数从 N 次压到 1 次
- **今日要闻 8 卡**：DSH 桌面端 / Jev 决策 / PTC 技术看点 / A股周复盘 / 健身第2周收官 /
  求职作品建议 / Re:Zero 倒计时4天 / 国庆假期安排
- **每日一词 10 条 / 9 领域**：PTC、隐私成本、决策模型、超量恢复、节前效应、
  激活率、技术判断力、应急金、假期节律紊乱、多端复用架构
- **小白课堂 10 条 / 8 领域**：含 PTC 原理、Electron 复用、隐私成本、决策模型分工、
  理解价值 vs 使用价值、超量恢复、节前效应、激活率、技术判断力、假期节奏；
  旧 10 条归档为 2026-09-23；current_day 17 → 21
- **今日待办 5 条**：DSH/Jev 整理成产品分析作品 / 增肌第2周收官复盘 / 称重校准 / 节前仓位 / 训练平台进度
- 内容新鲜度：17 个分区全部不落后；一致性检查 22 项通过
- 版本 1.8.17 → 1.8.18

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
