# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.23。10/18 追加更新【AI 动态追踪】：① REA（Reverse Engineer Anything）科普——'
       'GitHub 周榜第一的 MCP 服务器，讲清它的三层分工（MCP工具/Skill流程/CLI入口）、能力边界与授权前提；'
       '② 与 Jev 的 8 维对比表（REA 给 Agent 加眼睛，Jev 给模型换大脑）；③ DeepSeek-V4.1-Flash-1017 与 '
       'Meta Muse Wonder/Full 的实测数据；④ 评分表更新至 16 个模型、8 条结论、11 条调价记录。'
       '结论：REA 学思路（MCP 三层分工）优先于上手工具。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-18（周日 · v1.8.23）AI 动态追踪专项：REA 科普 + 评分表更新
- **REA（Reverse Engineer Anything）科普**：GitHub 周榜第一（总星 29.1 万 / 周增 24.9 万 / v6.4.0）
  - 本质是 **MCP 服务器**：Agent 提问 → REA 调本地工具取证 → Agent 解释，官方要求输出含【证据 + 推断 + 未知项】
  - 支持目标：原生二进制（Hopper/Ghidra/IDA）、JS/Electron、.NET、网站（Chrome）、APK（JADX+JDK）、固件、抓包
  - **三层分工**（核心知识点）：MCP 暴露工具 / Skill 教何时调用 / CLI 供人直用；只装 Skill 不会自动获得 MCP 工具
  - 边界：仅限自有或获授权软件；本机分析但结果会进入 Agent 对话上下文
  - 低门槛入口：静态 JS/Electron 检查无需任何原生引擎（`npx rea-agents@latest setup`）
- **REA vs Jev 八维对比表**：层次（工具层 vs 模型层）、解决什么、输出形态（证据 vs JSON 判断）、
  接入方式、前提条件、对幻觉的态度、依赖成本、对你的价值
  - 一句话：**REA 给 Agent 加「眼睛」，Jev 给模型换「大脑」**
- **DeepSeek-V4.1-Flash-1017**（10/17）：HLE 42.6(+5.8)、Terminal-Bench 4.0 42.3(+11.1)、ProgramBench 29.1(+8.8)、
  DeepSWE 77.0；模型名仍为 `deepseek-flash`（旧调用自动升级）；1M 上下文 + 384K 输出；「许愿式编程」自反馈 RL
- **DeepSeek Harness 0.2.1-rc.2**（10/17）：适配新模型与 Search/Fetch API（¥5/千次成功请求，11/1 前 Harness 调用免收）
- **Meta Muse Wonder / Full**（10/12）：AA 智能指数 56（六周 +8）、SWE-Marathon 57.5% 超 Opus 5.5 与 GPT-6 Astra、
  法律 Harvey 13.1（Opus 的 3.1 倍）、幻觉率 23%（Opus 59%）但知识指数仅 30
- **评分表更新**（`AI_MODEL_COMPARISON`）：
  - `updated` 2026-09-06 → 2026-10-18；模型数 14 → **16**（新增 Meta Muse Wonder / Wonder Full）
  - DeepSeek V4.1 Flash 条目重写为 **V4.1-Flash-1017**（智能 86→87、速度 90→92、综合 91）
  - `key_takeaways` 全部重写为 8 条（含 Agent 三层分工、幻觉率双刃剑、价格时段化、选型策略）
  - `price_adjustments` 新增 3 条（V4.1-Flash-1017 / Meta Muse / REA）
- **资讯区重写**：7 条（REA / DeepSeek / Harness / Meta / A股 / 游戏 / 生活）
- **要闻第 7 张改为 REA**（原为「AI 转两周复盘」）
- 一致性检查 22 项通过；视觉体检 30/30；版本 1.8.22 → 1.8.23

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

p = os.path.join(BASE, 'daily_data.js.bak')
if os.path.exists(p):
    os.remove(p); print('已删除备份')
