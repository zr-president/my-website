---
name: weekly-site-update
description: 更新钟锐的个人网站（C:\Users\ZR\Desktop\钟锐的个人网站）的日常内容：读系统时钟、刷新 17 个分区、更新要闻/每日一词/小白课堂/今日待办、维护 AI 模型评分表、跑全量质量校验并发布到 GitHub Pages。当用户说「更新网站」「更新我的个人网站内容」「刷新站点」「更新今日内容」时使用。
whenToUse: 用户要求更新个人网站的内容或数据时使用，包括日常全量更新、个别分区刷新、AI 评分表补录。不用于纯样式调整、单个错别字修正、或对网站做结构性重构。
---

# 个人网站更新

对一个纯前端、数据驱动的个人站点做「内容更新 + 全量质量校验 + 发布」的标准流程。

站点：`https://zr-president.github.io/my-website/`（仓库 `zr-president/my-website`，分支 `master`，Pages 由 master 直接发布）

---

## 1. 使用场景

### ✅ Use when（正向触发，任一命中即执行）

- 「更新我的个人网站」「更新网站内容」「刷新站点」
- 「今天的内容更新一下」「把 XX 板块更新到最新」
- 「评分表要补新模型」
- 用户明确要求把某份材料/分析写进网站

### ❌ Don't use when（负向触发，命中则应改做别的）

- 只是想改**一个错别字**或一行文案 → 直接 `edit`，不要跑全量流程
- 只想调整**样式/配色/布局** → 属于视觉改动，走 `index.html` 的 CSS 段，不碰数据
- 想**重构代码结构**（拆模块、改架构）→ 这是工程任务，需要先出方案
- 用户只是想**看看网站现在什么状态** → 只读检查，不要写文件
- 目标不是这个仓库（如训练平台 `钟锐的训练场`）→ 那个仓库另有部署流程（`tools/deploy.py` 同步 gh-pages）

**判断依据**：需要改动 `daily_data.js` 的内容数据 → 用本 skill；只改 `index.html` 的静态文案/CSS → 不用。

---

## 2. 硬性前置（每次必做，顺序不能变）

### ① 先读系统时钟 —— 这是本 skill 最重要的规则

```powershell
python -c "import datetime;n=datetime.datetime.now();print(n.strftime('%Y-%m-%d'),['周一','周二','周三','周四','周五','周六','周日'][n.weekday()],n.strftime('%H:%M'))"
```

**绝对禁止**用「上一次内容的日期 + 1」推算。这个坑踩过：站点连续多天显示旧日期，用户原话是「每次让网站更新，都不是最新的日期」。

### ② 记录站点当前状态

```powershell
cd 'C:\Users\ZR\Desktop\钟锐的个人网站'
node -e "const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);console.log('版本',c.SITE_VERSION,'| 日期',c.DAILY_DATA.update_date,'| 要闻',c.DAILY_BRIEFING.date);"
```

计算落后天数；落后 ≥1 天就必须**实质刷新内容**，不能只改日期标签。

### ③ 备份

```powershell
Copy-Item daily_data.js daily_data.js.bak -Force
Copy-Item index.html index.html.bak -Force
Copy-Item detail_content.js detail_content.js.bak -Force
```

---

## 3. 文件地图

| 文件 | 体积 | 作用 | 注意 |
|---|---|---|---|
| `index.html` | ~330 KB | 单页应用（含 ~197 KB 内联 JS + ~31 KB 内联 CSS） | **有两个 `</body>`**（见第 8 节） |
| `daily_data.js` | ~348 KB | 全部内容数据（24 个顶层变量） | 主战场 |
| `detail_content.js` | ~251 KB | 22 个详情页 HTML 字符串 | `DETAIL.*` 是**赋值语句** |
| `knowledge_index.js` | ~372 KB | 搜索索引（1573 条） | **必须保持懒加载** |
| `img_style.js` | ~2 KB | 图片主色映射 | 改图时才动 |
| `scripts/check_consistency.py` | — | 22 项一致性检查 | 必须全过 |
| `scripts/audit_freshness.py` | — | 日期与内容新鲜度（含逐字段） | 必须全过 |
| `scripts/visual_audit.py` | — | 10 分区 × 3 视口 = 30 组合 | 必须 0 问题 |

---

## 4. 更新流程（7 步）

### Step 1 — 更新当日内容四件套

| 变量 | 要求 |
|---|---|
| `DAILY_BRIEFING` | 8 张卡，`date` = 今天 |
| `DAILY_VOCAB` | 10 个词 / **10 个不同领域**（单一领域超 50% 会报警） |
| `LEARN_PATHS` | 10 条 / 10 领域；`current_day` +1；**旧 items 存入 `archive` 的当日键** |
| `DAILY_DECISIONS` | 5 条待办，`updated` = 今天 |

### Step 2 — 刷新 17 个分区

分区清单（`INSIGHTS`）：
```
stock anime music novel gaming learning beer fashion fitness diet career car house life-tips movie ai-track news
```

**每个分区只改这三个字段会被审计扫描**：`summary`、`trend`、`tip`。
（`verdict` **不**参与日期扫描 —— 这是踩过的坑：只改 verdict 无效）

要求：
- 三个字段的内容里都必须出现**当日日期**（如「10月20日（周二）」）
- 内容要**真的换**，不是把日期塞进去
- 时间敏感事实要推进（交易日数、倒计时天数、连载天数、增重天数…）

### Step 3 — 日期同步（26 个 `updated` 字段）

```python
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-\d\d-\d\d)\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
```

**只替换 `updated` 字段**，绝不动 `archive` 的键（那些是历史日期，改了就是篡改记录）。

### Step 4 — 升版本（三处必须一致）

1. `daily_data.js` → `var SITE_VERSION = "x.y.z";`
2. `index.html` → `daily_data.js?v=x.y.z`（同时 `detail_content.js` / `img_style.js` / `personal_config.js`）
3. `WEBSITE_GUIDE.summary` 里的「版本x.y.z」

### Step 5 — 跑三项校验（必须全绿才能继续）

```powershell
python scripts/audit_freshness.py
python scripts/check_consistency.py
python scripts/visual_audit.py
```

判据：
- audit：结论「无」+ 逐字段「✅ 三个字段的内容日期均不落后」
- consistency：`✅ 一致性检查通过（22 项）`，退出码 0
- visual：`0/30 个组合有问题`

### Step 6 — 渲染验证

```powershell
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$out = '_v.html'
$p = Start-Process -FilePath $edge -ArgumentList '--headless=new','--disable-gpu','--dump-dom','--window-size=1440,1200','--virtual-time-budget=18000',"file:///C:/Users/ZR/Desktop/钟锐的个人网站/index.html" -RedirectStandardOutput $out -PassThru -WindowStyle Hidden
$p.WaitForExit(60000); Get-Content $out -Raw -Encoding UTF8 | Select-String '今日更新已核查'
Remove-Item $out -Force
```

检查：当日日期、版本号、`今日更新已核查` 徽章、本日新增关键词。

**详情页验证**（`DETAIL` 内容只在点击时渲染）：注入 `openDetail('fitness')` 后 dump-dom。注入位置必须是**最后一个** `</body>`：
```powershell
$idx = $h.LastIndexOf('</body>')
```

### Step 7 — 发布

```powershell
git add -A
Set-Content -Path '_msg.txt' -Value $msg -Encoding UTF8
git commit -q -F '_msg.txt'
Remove-Item '_msg.txt' -Force
for($i=1;$i -le 8 -and -not $pushed;$i++){ git push origin master; if($LASTEXITCODE -eq 0){$pushed=$true}else{Start-Sleep -Seconds 10} }
```

GitHub 推送偶发失败，**必须重试循环**（最多 8 次，间隔 10 秒）。

---

## 5. 口径基线（不可变，改它必须同步所有位置）

| 项 | 值 |
|---|---|
| 身高 / 体重 | 170 cm / **60.65 kg** |
| BMI | 21.0 |
| 体脂 | 约 12-14%（照片判断） |
| 热量 | 训练日 **2600** / 休息日 **2400** kcal |
| 蛋白 | **130-140 g** |
| 目标岗位 | AI 产品运营 / AI 增长运营 / AI 产品经理 |
| 目标公司 | 字节 / 腾讯 / 美团 / 小红书 / 微众 / SHEIN / 滴滴 |

**改口径的正确做法**：`DETAIL.diet` 和 `INSIGHTS.diet` **两处都要改**，另外 `scripts/check_consistency.py` 里的常量也要跟着改（否则检查会失败）。改体能数据同理，`DETAIL.fitness` + `INSIGHTS.fitness` + 检查脚本三处。

---

## 6. 禁止项（L3 边界 —— 最容易违反）

| # | 禁止 | 原因 |
|---|---|---|
| 1 | 改动 `archive` 的日期键 | 那是历史记录，改了等于篡改 |
| 2 | 写入个人金额（存款、薪资、理财数字） | 隐私红线，站点是公开的 |
| 3 | 使用中文单引号 " " | 站点规范：改用【】 |
| 4 | 引入外部图片 URL | 必须自托管 `assets/img/*.webp`（0 外链） |
| 5 | 让 `knowledge_index.js` 回到首屏 | 已改懒加载，省 372 KB |
| 6 | 全局替换 `</body>` | 文件里有**两个**，第一个在内联 JS 字符串里，替换会破坏整个脚本块 |
| 7 | `git commit -m "..."` 带 ASCII 双引号 | PowerShell 会吞引号 → 用 `Set-Content` + `-F` |
| 8 | 用 `python -c "..."` 写含中文/引号的长脚本 | 反复踩坑 → 一律写成 `.py` 文件再执行 |

---

## 7. 已知失败清单（5 条历史 bug → 对应规则）

| # | 踩过的坑 | 现在的规则 |
|---|---|---|
| 1 | 日期用「上次 +1」，从不读时钟 | Step 1 强制 `datetime.now()`；audit 会校验站点日期 = 系统日期 |
| 2 | **只改了 `summary`，`tip` 还是旧的**（「今日行动」没更新） | 三字段都写；audit 已加**逐字段检查**（防止新 summary 掩盖旧 tip） |
| 3 | 评分表漏了新模型（Claude Opus 5.5 漏了两天） | 更新 `ai-track` 时必须同步检查 `AI_MODEL_COMPARISON` 是否有当月新模型 |
| 4 | 口径不一致（饮食写 2500、健身写 2400） | 改口径必须同时改 `DETAIL` + `INSIGHTS` + 检查脚本常量 |
| 5 | 全局替换把 `archive` 键也改了 | 日期替换只匹配 `updated` 字段 |

---

## 8. 环境级坑（代码结构，会反复遇到）

| 现象 | 真相 | 对策 |
|---|---|---|
| 正则匹配不到分区 | `stock` 等键**不带引号**（`stock: {`），`ai-track` **带引号** | 正则写 `(?:"key"\|key)\s*:\s*\{` |
| 字符串替换失败 | 部分分区用**单引号**，部分用**双引号** | 正则同时兼容 `"(?:[^"\\]\|\\.)*"` 和 `'(?:[^'\\]\|\\.)*'` |
| `DETAIL.fitness` 找不到 | 它是**赋值语句** `DETAIL.fitness = '...'`，不是对象字面量 | 匹配 `DETAIL\.<key>\s*=\s*` 再加引号体 |
| 注入脚本后页面全乱 | `index.html` 有**两个 `</body>`**（第一个在内联 JS 字符串里），全局替换会切断脚本 | 用 `LastIndexOf('</body>')` 只替换最后一个 |
| Python 脚本引号报错 | PowerShell here-string + 中文 + 转义互相冲突 | **写成 `.py` 文件**再 `python xxx.py` |
| 正则死循环 | 数组边界扫描时写成 `k += -1` | 循环内 `k += 1`，结束后 `k -= 1` |

---

## 9. 自检清单（交付前逐条打勾）

- [ ] 站点日期 = 系统真实日期（不是推算的）
- [ ] 17 个分区 × 3 字段（summary/trend/tip）都有当日日期
- [ ] 时间敏感事实已推进（交易日/倒计时/连载天数等）
- [ ] `DAILY_BRIEFING` 8 卡、`DAILY_VOCAB` 10 词 10 领域、`LEARN_PATHS` 10 条 + 旧条已归档、`DAILY_DECISIONS` 5 条
- [ ] `archive` 键未被改动
- [ ] 未写入个人金额、未用中文单引号、无外链图片
- [ ] 版本三处一致（SITE_VERSION / index.html ?v= / WEBSITE_GUIDE）
- [ ] `audit_freshness.py` → 逐字段均不落后
- [ ] `check_consistency.py` → 22 项通过、退出码 0
- [ ] `visual_audit.py` → 0/30
- [ ] 渲染验证通过（含详情页 `openDetail` 注入测试）
- [ ] changelog 已追加
- [ ] `git push` 成功
- [ ] 人工确认点 ≤2（看报告 + 说「推送」）

---

## 10. 交付标准（怎么算这次更新成功）

| 层级 | 标准 |
|---|---|
| **L1 有** | 8 张要闻卡存在 · 17 分区都有内容 · 页面能打开 · 详情页能点开 |
| **L2 对** | 站点日期 = 系统日期 · 17 分区三字段都有当日日期 · 口径与基线一致 |
| **L3 边界** | 没动 archive · 没写金额 · 没外链图 · 没用中文单引号 · 没有全局替换 `</body>` |
| **L4 可复现** | 同一 skill 跑 3 次，输出的分区数/检查项数/版本规则完全一致 |

**人工确认点（只允许这两个）**：
1. 看三项校验报告
2. 说「推送」（或提出修改）

其余步骤（备份、写内容、同步日期、升版本、跑检查、渲染验证、commit）都应由本 skill 自动完成。

---

## 11. 示例

**✅ 正确触发**
> 用户：「更新我的个人网站内容」
> → 读时钟 → 发现落后 N 天 → 全量刷新 17 分区 → 校验 → 推送

**✅ 正确触发（局部）**
> 用户：「AI 动态追踪里补一下最新模型，评分表也更新」
> → 只改 `ai-track` + `AI_MODEL_COMPARISON`，其余分区不动 → 但仍要跑全量校验（因为口径可能被牵连）

**❌ 不该触发**
> 用户：「首页那个标题字号调小一点」
> → 这是 CSS 改动，直接 `edit` `index.html`，不要动 `daily_data.js`
