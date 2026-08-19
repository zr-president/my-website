# 钟锐的个人数字空间 — 网站项目

## 一句话描述
这是我的个人网站项目（单 HTML 文件 + 数据文件），17 个板块每日 AI 自动更新，部署在 GitHub Pages。

## 启动方式
- 无需启动服务器，直接用浏览器打开 `index.html` 即可
- GitHub Pages 自动部署：https://zr-president.github.io/my-website/
- 推送后 1-2 分钟自动上线

## 自动更新模式（已启用）
- **GitHub Actions 每日 8:30（北京时间）自动更新**：`.github/workflows/auto-update.yml` 定时触发 → `scripts/auto_update.py` 调用 DeepSeek API（`secrets.DEEPSEEK_API_KEY`）→ 按【状态推进】策略生成当日全部板块内容 → node 校验 → 自动 commit + push
- **首次启用前需配置**：仓库 Settings → Secrets and variables → Actions → 添加 `DEEPSEEK_API_KEY`（DeepSeek 开放平台的 API Key）
- **本地手动运行**：`set DEEPSEEK_API_KEY=sk-xxx && python scripts/auto_update.py --commit`
- **手动触发一次**：GitHub 仓库 Actions 页 → AI 每日自动更新 → Run workflow
- **失败安全**：API 失败/JSON 解析失败/语法校验失败时不改动文件（自动 git checkout 回滚），不会破坏网站
- **内容策略**：自动更新做【状态推进】（明日→今日、追番第N天→第N+1天、已发生事件→持续状态），不编造无法确认的新事件数字；重大突发事件仍需人工/AI 手动更新补充

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
3. **必须更新全部 17 个板块的 INSIGHTS 内容（summary/trend/tip/verdict）**：
   stock / ai-track / movie / news / gaming / career / anime / music / novel / learning / beer / fashion / fitness / diet / car / house / life-tips
   —— 娱乐板块（anime/gaming/movie/music/novel）也必须有当日更新（即使没有大事件，也要把内容刷新为「当前状态」，如「已开播/追番中/预售已开启」）
4. 新增 knowledge_base 文件
5. 更新 OPTIMIZATION_LOG（日期 + 新增 3-5 条优化建议 + streak_days+1）
   —— **新增的 3-5 条建议中，至少 3 条必须标为「待办」（当日不实施，作为后续优化方向）**；只有当日确实实施的才标「已完成」。
   原因：优化日记页面只展示非「已完成」条目——若当天建议全标已完成，页面会只剩 0-1 条待办，用户看不到每日新增的优化方向（8/16、8/19 两次踩坑）。
   推荐结构：今日实施 1-2 条（已完成）+ 3-4 条新方向（待办），如「实施 Qwen 开源专题 + 待办技能雷达自动反馈/情绪指标条」。
6. 提交并推送到 GitHub

### 自动更新（替代手动模式）
已启用 GitHub Actions 每日 8:30 自动更新（见上文「自动更新模式」）。自动更新脚本 `scripts/auto_update.py` 的工作方式：
- 读取昨日 daily_data.js → 提取各板块摘要作为上下文 → 分 3 次调用 DeepSeek API（核心简报 / 17板块INSIGHTS / 词汇+课堂+优化建议）
- 自动处理：LEARN_PATHS archive 迁移、OPTIMIZATION_LOG 新增建议+streak+1、版本号三处同步（SITE_VERSION / index.html 缓存符 / WEBSITE_GUIDE）、knowledge_base 当日文件
- 手动运行同一脚本可复用全部逻辑：`python scripts/auto_update.py --commit`
- **注意**：自动更新的内容基于【状态推进】策略，无法联网搜索当日新事件——若当天有重大事件（如重磅发布会/大跌大涨），仍建议人工更新补充真实资讯

### 时效词检查（每次更新必做）
**禁止在内容里保留过期时效词**。更新完成后全文检查以下词，出现即必须改写：
- 「今日预售 / 今日开播 / 今日10:00 / 今晚开播 / 今日上映 / 今日发售」→ 事件已发生则改「已开启 / 已开播 / 追番中 / 预售中」
- 「周三/周四观影策略」等带星期几的建议 → 更新为当天或周末策略
- 「8月X日」明确日期 → 核对是否已过去，过去则改写为当前状态
- 每个板块 INSIGHTS 的 updated 日期必须与当日一致，内容不得残留旧日期数据
- 每日更新模板检查点：DAILY_DATA.movie 与 INSIGHTS.movie 必须同步更新，不能只改一个

### 实施优化建议
说「按照今天的优化建议去优化」或「根据优化建议更新网站」

### 编辑 daily_data.js 的安全流程
如果直接编辑 `daily_data.js` 有风险（会被坏脚本截断），建议：
1. 编辑前确认 git 状态干净
2. 编辑后 `node -e "new Function(require('fs').readFileSync('daily_data.js','utf8'))"` 校验语法
3. 或使用 `python scripts/safe_edit.py <target> <script>` 包装器

### 编辑提速经验（8/19 更新教训·必读）
**1. 先快照再动手**：开始编辑前，先 grep 关键字段确认文件实际状态，不要凭记忆写替换目标——
- `SITE_VERSION` / `daily_data.js?v=`（index.html）实际版本号
- `"update_time"` / `"update_date"`（可能被 quick-update 工作流改动，如 08:57:00）
- WEBSITE_GUIDE summary 里的版本号可能滞后于 SITE_VERSION（quick-update 只改版本号行不改 summary）
- 每个板块的 `updated:` 日期是否与预期一致

**2. 小粒度替换**：按板块逐个替换（每板块 5-6 行），不要用跨多个板块的大块 old_string——大块拼接极易因一个字符差异（全角/半角、· 符号）导致替换失败，失败后读取确认再重试更费时。

**3. 跨多天更新**：若距上次更新超过 1 天（如 8/16→8/19），先梳理中间积压的时间节点（发售日/调价生效日/公测日等），再逐日推进状态，避免一次性堆大量内容。

**4. 编辑后统一校验**：所有字段改完再一次性 `node` 校验（daily_data.js + index.html 内联 JS），避免每改一块校验一次拖慢节奏。

### 提交推送
```bash
git add -A
git commit -m "描述"
git push
```
GitHub：https://github.com/zr-president/my-website
分支：master

### 推送授权（用户已确认）
用户已授权：**本项目所有修改的文件，只要自检（JS/Python/YAML 语法校验等）通过，均可直接 git commit + push，无需再逐次询问。** 自检失败时禁止推送，需修复后重验。

## 重要约束

1. **禁止中文单引号 `' '`**——使用 `【】` 代替
2. **所有内容必须具体**——来自搜索结果，不能是泛泛而谈
3. **保持 JS 语法正确**——编辑后务必用 Node.js 校验
4. **daily_data.js 的 onDataReady() 调用必须在文件末尾**——否则全部板块不渲染
5. **版本号三处同步**：daily_data.js (SITE_VERSION) + index.html (缓存破坏符 v=) + WEBSITE_GUIDE

## 内容质量标准（每日更新必读）

1. **板块日期一致性**：更新某个板块的 summary 时，必须同时检查该板块的 trend/tip/reasoning 是否还是旧日期数据——不允许出现【同一板块内沪指点位自相矛盾】这类拼接错误（曾发生：stock.summary 写 +0.01% 收3927.18 又写 +0.32% 收3946.51）
2. **TOOLCHAIN_RADAR 必填**：每日更新必须填写工具链雷达（Claude Code + DeepSeek + Harness 相关动态），每个条目回答 4 问：发生了什么→对我意味着什么→价格/性价比变化→行动建议。宁可 2 条精确的，不要 5 条泛泛的
3. **ai-track 板块双视角**：除行业宏观外，至少 1 条是【贴近用户工具链/求职/投资】的落地解读——参考 TOOLCHAIN_RADAR 联动
4. **禁止只改标题不改正文**：更新 news_headlines / market_summary 时，同步检查 INSIGHTS.news / INSIGHTS.stock 正文，旧日期数据必须一并刷新或明确标注日期
5. **每个板块至少含一个可行动建议**：tip 字段必须是【今天/本周能做什么】，不能只描述现象
6. **结论先行（verdict 字段）**：stock / news / ai-track / career 四个板块必须带 verdict 字段——用 2-4 句大白话回答：①发生了什么本质变化 ②意味着什么、会带来什么结果 ③该不该动、行动建议 ④关注信号。禁止只罗列涨跌数字——小白用户要的是「结果和结论」，不是「数据」
7. **数据一致性**：板块内所有数字（点位/涨幅/日期）必须来自同一交易日，禁止拼接不同日期的数据（曾发生 stock.summary 同时出现两个沪指点位的错误）
8. **小白课堂去重**：LEARN_PATHS 的当天 10 条只放 items；archive 只存【历史日期】内容（把旧 items 追加到 archive[旧日期] 后再换新 items）。禁止把当天内容同时写进 archive 和 items（曾导致课堂分区同一天内容显示两次）
9. **全站时效检查**：静态详情内容（detail_content.js）存在日期标记（如"2026年X月"、"X月底"）时必须保持最新——每日更新时运行 daily_update.py 的 check_static_freshness()，发现过期标记必须同步刷新对应板块（旅游/小说连载/模型表等），禁止让静态内容滞后超过30天
10. **学习区=全站知识中枢**：学习区「今日新知」自动汇总各板块当日新知识；模型对比类内容一律动态引用 AI动态追踪 板块（AI_MODEL_COMPARISON），禁止在学习区写死静态模型表（会过期）
11. **购车/购房/穿搭等生活板块三层结构**：每个板块必须包含【科普入门（概念/参数教学）+ 实时建议 + 时机判断（当下该不该行动/买不买）】。时机判断基于通用市场逻辑（Q4冲量/政策窗口/新车上市节奏），**禁止写入钟锐的具体隐私**（存款金额/收入/失业状态/健康细节等）
12. **隐私保护（最高优先级）**：网站内容可能被分享给他人（面试官/朋友），所有公开展示的内容（detail_content.js / daily_data.js 中的 INSIGHTS/决策单/优化日记 desc / 推送内容）**禁止出现**：存款金额、收入水平、失业/求职过渡期描述、具体健康数据、家庭住址、身份证类信息。敏感信息只放 personal_config.js（该文件虽公开但为纯偏好配置），或用通用表述替代（如「预算敏感型用户」「非刚需」）。发现隐私泄露必须立即脱敏

## 已知待办

- #1-#66 均已实施完成（见 OPTIMIZATION_LOG，66/70 已完成，其中 #67-#70 为待办）
- 新增优化建议时从当前最大编号+1 开始编号，并同步 total_suggestions（自动更新脚本已自动处理）
- 常规待办：每日更新后同步版本号三处（daily_data.js SITE_VERSION / index.html 缓存符 / WEBSITE_GUIDE）——自动更新脚本已自动处理

## 用户偏好
- 工作目录：项目在桌面「钟锐的个人网站」文件夹，脚本均用相对路径定位（sync.bat 用 %~dp0，Python 用 __file__），两台机器通用
- 名词解释偏好 B站搜索链接
- INSIGHTS 每个板块包含四层科普：🔍发生了什么 → 🤔为什么 → 📊术语解释 → 💡启示
