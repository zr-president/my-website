# 钟锐的个人数字空间 — 网站项目

## 一句话描述
这是我的个人网站项目（单 HTML 文件 + 数据文件），17 个板块每日 AI 自动更新，部署在 GitHub Pages。

## 启动方式
- 无需启动服务器，直接用浏览器打开 `index.html` 即可
- GitHub Pages 自动部署：https://zr-president.github.io/my-website/
- 推送后 1-2 分钟自动上线

## 核心文件

| 文件 | 作用 | 约行数 |
|------|------|--------|
| `index.html` | 主文件：HTML 结构 + CSS 样式 + 全部 JS 渲染逻辑 | ~2200 |
| `daily_data.js` | 数据文件：所有动态内容的数据源（INSIGHTS/PICKS/VOCAB/QUIZ/模型对比/优化日记） | ~580 |
| `knowledge_base/` | 按分类+日期命名的 Markdown 知识库，每日自动攒 | — |
| `scripts/` | 辅助脚本（去重 dedup_kb.py、安全编辑 safe_edit.py 等） | — |

## 数据流架构

```
daily_data.js 加载
  └→ 定义所有全局变量（INSIGHTS / PICKS / DAILY_VOCAB / AI_MODEL_COMPARISON 等）
  └→ 末尾调用 onDataReady() ← index.html 中的回调
       └→ 触发所有渲染函数：renderAllPicks / renderBriefing / renderVocab / renderModelComparison 等
```

**关键规则**：所有显示在网站上的文字内容都在 `daily_data.js` 里，`index.html` 只负责渲染。日常更新只改 `daily_data.js`。

## 全局变量清单（daily_data.js）

| 变量 | 内容 |
|------|------|
| `SITE_VERSION` | 网站版本号 |
| `DAILY_BRIEFING` | 每日 6 条要闻 |
| `DAILY_VOCAB` | 每日一词（10 个术语，含 emoji/category/word/definition/example/why_matters）|
| `DAILY_QUIZ` | 每日一练（6 种题型轮换）|
| `INSIGHTS` | 17 个板块的今日分析（summary/trend/tip/reasoning/updated）|
| `PICKS` | 各板块精选推荐 |
| `AI_MODEL_COMPARISON` | 11 款 AI 模型对比表（含 安全 维度）|
| `OPTIMIZATION_LOG` | 优化建议日记（33 条） |
| `INSIGHTS_TODAY_UPDATED` | 今日更新了哪些板块的数组 |
| `WEBSITE_GUIDE` | 网站使用指南 |
| `HOME_SECTIONS` | 首页显示的板块列表 |

## 常用操作

### 每日更新网站
说「X月X号更新」即可，Claude 会：
1. 搜索当日最新资讯
2. 更新 DAILY_BRIEFING / DAILY_VOCAB / PICKS / INSIGHTS（含 reasoning）
3. 更新 stock / ai-track / movie / learning / career / news 等核心板块
4. 新增 knowledge_base 文件
5. 更新 OPTIMIZATION_LOG（日期 + 新增 3-5 条优化建议 + streak_days+1）
6. 提交并推送到 GitHub

### 实施优化建议
说「按照今天的优化建议去优化」或「根据优化建议更新网站」

### 编辑 daily_data.js 的安全流程
如果直接编辑 `daily_data.js` 有风险（会被坏脚本截断），建议：
1. 编辑前确认 git 状态干净
2. 编辑后 `node -e "new Function(require('fs').readFileSync('daily_data.js','utf8'))"` 校验语法
3. 或使用 `python scripts/safe_edit.py <target> <script>` 包装器

### 提交推送
```bash
git add -A
git commit -m "描述"
git push
```
GitHub：https://github.com/zr-president/my-website
分支：master

## 重要约束

1. **禁止中文单引号 `' '`**——使用 `【】` 代替
2. **所有内容必须具体**——来自搜索结果，不能是泛泛而谈
3. **保持 JS 语法正确**——编辑后务必用 Node.js 校验
4. **daily_data.js 的 onDataReady() 调用必须在文件末尾**——否则全部板块不渲染
5. **版本号三处同步**：daily_data.js (SITE_VERSION) + index.html (缓存破坏符 v=) + WEBSITE_GUIDE

## 已知待办

- #27: AI对比表综合评分增加权益权重选项（P2）
- #28: Qwen3.8开源状态跟踪与数据更新（P1）

## 用户偏好
- 工作目录：`C:\Users\ZR\Desktop\钟锐的个人网站\`
- 名词解释偏好 B站搜索链接
- INSIGHTS 每个板块包含四层科普：🔍发生了什么 → 🤔为什么 → 📊术语解释 → 💡启示
