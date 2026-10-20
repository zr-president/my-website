# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.30。10/20 新增分区【🤖 AI 能力成长】（侧栏「学习」组下）：'
       '基于桌面《资料》文件夹两份企业 AI 培训材料（《AI办公系统搭建实战》55 页 + '
       '《AI赋能办公效率倍增+数据分析》43 页）的提炼，已剔除其中的厂商产品推广页。'
       '分四块：① 能力定位——对照文档「个人使用 AI 的五个能力阶段」，判定自己在 02-03 之间，'
       '并点出「有 05 的成果但没有 05 的能力」这个错觉；② 文档精华 9 条（提示词六维度/'
       'Agent-Skill-CLI-MCP 四层分工/知识库判断标准/先想清楚再说清楚/评测驱动/反馈要给现象+预期等）；'
       '③ 五个提升方向（补验收标准 · 工具图谱 3→6 类 · 规则沉淀成 Skill · 建个人知识库 · 从看结果到定标准）；'
       '④ 本周可做 3 件事（成本 0 元）。另附「AI 编程八步法」。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-20（周二 · v1.8.30）新增分区「🤖 AI 能力成长」
### 一、素材处理
- 读取桌面《资料》文件夹两份材料：
  - `AI办公系统搭建实战.pdf`（55 页 / 19.4MB，CCE 实训营 · 每日互动 AI事业部 叶小健）
  - `AI赋能办公效率倍增+数据分析-完整版.pptx`（43 页 / 5.1MB，Richard Song）
- 提取方式：PPTX 用 zipfile+XML 解析（43 页，11,335 字）；PDF 装 `pypdf` 提取（55 页，11,888 字）
- **剔除**：PDF 第 26-40 页的「个知·智能工作站」产品推广（混合云架构 / 四版本选型 / 会议纪要 / 公文写作）
- **保留有价值部分**：第 5-21 页「个人五能力阶段」+ 第 41-54 页「AI 编程八步法」+ PPT 的提示词方法论与 Skill 设计规范

### 二、新增分区结构（4 块）
**① 能力定位：我在五级里的哪一级**
| 阶段 | 我的现状 | 判定 |
|---|---|---|
| 01 会用 AI | 每天用豆包/DSH 提问、写内容 | ✅ 已过 |
| 02 能用好 AI | 能说清目标，但**几乎不写验收标准** | ⚠️ 进行中 |
| 03 会组合工具 | 只用过 3 个工具，全在「对话+编程」同类 | ❌ 未开始 |
| 04 会编排流程 | 每次都是**一次性交代**，无 Skill/知识库/定时任务 | ❌ 未开始 |
| 05 能构建应用 | 有网站+训练平台，但**构建由 AI 完成** | ⚠️ 有成果无能力 |

判定：**真实位置在 02-03 之间**；并明确指出「拥有产品 ≠ 拥有构建能力」这个错觉。

**② 文档精华 9 条**：提示词六维度（第六维度「约束与判断标准」最值钱）／不在于长在于说清／
会组合工具三件事／Agent-Skill-CLI-MCP 四层分工／知识库价值在「随时调得出来」／
先想清楚再说清楚／评测驱动先建「无 Skill」基线（边界明确最重要）／反馈要给「现象+预期」／AI 味三特征

**③ 五个提升方向**（每条带现状对比 + 具体例子 + 收益）
1. 🔴 把「验收标准」写进每一次交代 —— 例：从「更新网站内容」升级为 4 条验收标准
2. 🔴 工具图谱从 3 个补到 6 类 —— 补检索/图像/数据分析/自动化，每类只需会一个
3. 🟡 把重复交代沉淀成 Skill（**最大杠杆**）—— 写 `weekly-site-update` 的 SKILL.md，把日期规则/一致性检查/口径/禁止项固化
4. 🟡 建个人知识库 —— 桌面 `知识库` 目录全 md，判断标准「问它问题，它敢不敢给出来源」
5. 🟢 从「看结果」升级为「定标准」—— 把事后质疑变成事前清单

**④ 本周可做 3 件事**（全部 0 元）：加验收标准 / 装一个检索工具 / 建知识库放 3 个 md

**附**：AI 编程八步法（两个前提 + 八步 + 测试用例该怎么写）

### 三、技术实现
- 新增 `<section id="ai-growth">`，插在 `learning` 之后（静态 HTML，零 JS 依赖，无渲染风险）
- 侧栏「📚 学习」组新增入口 `<a href="#ai-growth">🤖 AI 能力成长</a>`
- 版本 1.8.29 → 1.8.30；index.html 322.9 → 324.0 KB
- 内联脚本 3 块语法 0 失败；一致性检查 22 项通过；视觉体检 30/30

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

for f in ['index.html.bak', 'daily_data.js.bak']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p); print('已删除', f)

# 清理提取的临时文件
for f in [r'C:\Users\ZR\Desktop\deepseek harness\_extract_pptx.txt',
          r'C:\Users\ZR\Desktop\deepseek harness\_extract_pdf.txt']:
    if os.path.exists(f):
        print('保留提取文本备查:', os.path.basename(f))
