# -*- coding: utf-8 -*-
"""收尾：WEBSITE_GUIDE + changelog + 清理"""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()
old = re.search(r'summary: "欢迎来到钟锐的个人数字空间！[^"]*"', d)
new = ('summary: "欢迎来到钟锐的个人数字空间！这是一个持续进化的智能信息中枢。'
       '版本1.8.27。10/20（周二）更新：① <b>性能优化</b>——knowledge_index.js（371.8KB）改为按需加载，'
       '首屏首次加载省约 29%；统一脚本版本号；补 og:image / canonical / twitter card。'
       '② <b>内容</b>——A股 10/8 开市至今 9 个交易日、三季报进入密集披露期；'
       '健身新计划执行第 3 天（关键看有没有做到接近力竭）；秋招反馈率与补投并行；'
       '10 月只剩 11 天该收尾；影之刃零倒计时 9 天；AI 竞争焦点转向「单任务成本」。'
       '每日一词与小白课堂各刷新为 10 个领域。"')
if old:
    d = d[:old.start()] + new + d[old.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('✅ WEBSITE_GUIDE.summary 已更新')

CL = BASE + r'\knowledge_base\changelog.md'
c = open(CL, 'r', encoding='utf-8').read()
entry = """# 网站更新日志

## 2026-10-20（周二 · v1.8.27）性能优化 + 内容更新
### 一、性能优化（实测驱动）
- **knowledge_index.js 371.8 KB 改为按需加载**：审计发现它注释里就写着「if loaded (deferred async)」，
  说明本来就设计成可选，却一直在首屏全量下载
  - 移除 eager `<script defer>`，新增 `ensureKnowledgeIndex(cb)` 加载器
  - 在 `doSectionQuery()` 首次查询时触发；先出本地结果，知识库结果 ~100ms 后补上
  - **实测**：`KI_before=undefined` → 触发后 `KI_len=1573`，页面 117 个元素正常渲染
- **版本号统一**：`img_style.js` 从 `?v=1.8.15`（落后 11 个版本）修到 1.8.27；
  给 `detail_content.js` / `personal_config.js` 补 `?v=`（原本没有缓存失效标记）
- **SEO 补全**：新增 `og:image`、`twitter:card` / `twitter:title` / `twitter:description`、`rel="canonical"`
- 审计结论修正：umami 统计早已被注释（无死请求）；PICKS 图片已有 `loading="lazy"` + `alt`（无需改）

### 二、内容更新
- **今日要闻 8 卡**：A股 9 个交易日与三季报检验 · 健身新计划第 3 天 · 秋招补投与面试 ·
  10 月收尾 · 影之刃零倒计时 9 天 · 广州入秋 · 模型竞争转向单任务成本 · 秋季新番第 5 周
- **每日一词 10 条 / 10 领域**：单任务成本 · 懒加载 · 种子用户 · 接近力竭 · 业绩兑现 ·
  结构化面试 · 再平衡 · 知识错觉 · 温差适应 · 功能蔓延
- **小白课堂 10 条 / 10 领域**（旧归档为 2026-10-18，current_day 25 → 26）
- **今日待办 5 条**：三季报窗口写死结论 · 检查接近力竭 · 统计反馈率 · 10 月收尾 · 影之刃零加愿望单
- **17 分区时间事实推进**：交易日 7 → 9、倒计时 11 → 9 天、连载 71 → 73 天、
  增肌第 30 → 31 天、秋季新番第 3 → 5 周、本月已过 18 → 20 天
- **ai-track.trend 追加**「10/20 补充：竞争焦点已换成单任务成本」（Sonnet 5.5 反超 / Opus 5.5 token 效率 / Gemini 四折）
- 一致性检查 22 项通过（0 提醒）；逐字段审计三字段均不落后
- 版本 1.8.26 → 1.8.27

"""
c = re.sub(r'^# 网站更新日志\r?\n', entry, c, count=1)
open(CL, 'w', encoding='utf-8').write(c)
print('✅ changelog 已追加')

for f in ['daily_data.js.bak', 'index.html.bak', 'detail_content.js.bak']:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        os.remove(p); print('已删除', f)
