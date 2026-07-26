// ===== 数据分析能力教程 - 供 detail_content.js 使用 =====
// 用法：将下面的字符串赋值给 DETAIL 对象，例如 DETAIL.learning = <以下内容>;

'<h2>📊 AI产品运营 · 数据分析能力完整教程</h2><p class="detail-subtitle">从零到独立做运营数据分析 · 覆盖SQL / Excel / A/B测试 / 学习资源</p>'+

'<h3>🎯 为什么运营必须学数据分析？</h3>'+
'<div class="highlight-box"><p><strong>一句话：</strong>不靠数据说话，你的工作成果无法量化，晋升汇报没有底气，产品决策只能"我觉得"。<br>'+
'<strong>运营数据分析的三大核心场景：</strong>① 日常监控——DAU/留存/转化率正常吗？② 问题诊断——哪个环节流失最严重？③ 效果评估——这次活动到底带来了多少增量？<br>'+
'<strong>学习路径：</strong>SQL取数 → Excel做报表 → A/B测试验证效果。按顺序学，30天可独立出分析报告。</p></div>'+

'<h3>🗄️ 第一章：SQL速成——运营必备的取数能力</h3>'+
'<p>SQL（Structured Query Language）是数据库的通用语言。运营不需要学会建表，但<strong>必须能自己取数</strong>。以下4个语法点覆盖运营日常90%的需求。</p>'+

'<h4>1.1 SELECT + WHERE + ORDER BY —— 查询与筛选</h4>'+
'<p><strong>语法速记：</strong>SELECT 列名 FROM 表名 WHERE 条件 ORDER BY 排序列 DESC/ASC</p>'+
'<table class="data-table"><tr><th>场景</th><th>SQL示例</th><th>说明</th></tr>'+
'<tr><td>查昨天注册用户</td><td><code>SELECT user_id, nickname, created_at<br>FROM users<br>WHERE created_at >= '2026-07-25'<br>  AND created_at < '2026-07-26'<br>ORDER BY created_at DESC</code></td><td>用日期范围而非 DATE() 函数，可以命中索引更快</td></tr>'+
'<tr><td>DAU最高的10天</td><td><code>SELECT date, COUNT(DISTINCT user_id) AS dau<br>FROM user_visits<br>GROUP BY date<br>ORDER BY dau DESC<br>LIMIT 10</code></td><td>DISTINCT 去重是关键——一个用户一天内可能多次访问</td></tr>'+
'<tr><td>找出付费超过1000元的用户</td><td><code>SELECT user_id, SUM(amount) AS total_pay<br>FROM orders<br>WHERE status = 'paid'<br>GROUP BY user_id<br>HAVING total_pay > 1000<br>ORDER BY total_pay DESC</code></td><td>聚合后的筛选必须用 HAVING，不能用 WHERE</td></tr>'+
'</table>'+

'<h4>1.2 JOIN —— 关联多张表</h4>'+
'<p>用户信息在一张表，行为数据在另一张表——<strong>JOIN是运营分析的核心技能</strong>。</p>'+
'<table class="data-table"><tr><th>JOIN类型</th><th>行为</th><th>运营场景</th><th>SQL要点</th></tr>'+
'<tr><td><strong>INNER JOIN</strong></td><td>取两表交集</td><td>查"注册后有过购买行为的用户"——只保留两边都匹配的行</td><td><code>FROM users u<br>INNER JOIN orders o ON u.id = o.user_id</code></td></tr>'+
'<tr><td><strong>LEFT JOIN</strong></td><td>保留左表全部</td><td>查"所有用户及其最后登录时间"——即使从未登录过的用户也要保留（便于算留存）</td><td><code>FROM users u<br>LEFT JOIN logins l ON u.id = l.user_id</code><br>未匹配的右表字段为 NULL</td></tr>'+
'<tr><td><strong>LEFT JOIN + IS NULL</strong></td><td>找"未发生"的记录</td><td>查"注册7天仍无任何关键行为的用户"——激活失败的预警名单</td><td><code>WHERE l.user_id IS NULL</code>加在LEFT JOIN之后，精准找"有A无B"</td></tr>'+
'</table>'+
'<div class="callout"><p><strong>常见坑：</strong>JOIN之前先确认关联键是否唯一——如果右表一个用户对应多条记录，JOIN后会"多出行"导致数据翻倍。不确定时，先对右表GROUP BY再JOIN。</p></div>'+

'<h4>1.3 GROUP BY + HAVING —— 聚合分析</h4>'+
'<p><strong>语法速记：</strong>SELECT 分组维度, 聚合函数(列) FROM 表 GROUP BY 分组维度 HAVING 聚合条件</p>'+
'<table class="data-table"><tr><th>运营场景</th><th>SQL写法</th><th>关键技巧</th></tr>'+
'<tr><td>过去7天每天新增用户数</td><td><code>SELECT DATE(created_at) AS day, COUNT(*) AS new_users<br>FROM users<br>WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)<br>GROUP BY day<br>ORDER BY day</code></td><td>时间窗口 + GROUP BY日期——运营日报的经典查询；CURDATE()取当天避免硬编码</td></tr>'+
'<tr><td>各渠道转化率对比</td><td><code>SELECT channel,<br>  COUNT(DISTINCT u.id) AS registrations,<br>  COUNT(DISTINCT o.user_id) AS payers,<br>  ROUND(COUNT(DISTINCT o.user_id)*100.0/COUNT(DISTINCT u.id),2) AS conversion_rate<br>FROM users u<br>LEFT JOIN orders o ON u.id = o.user_id<br>GROUP BY channel<br>HAVING registrations > 100</code></td><td>注册量<100的渠道样本太小，用HAVING过滤——避免被极端数据误导</td></tr>'+
'<tr><td>高价值用户行为特征</td><td><code>SELECT user_id,<br>  COUNT(*) AS sessions,<br>  AVG(duration_sec) AS avg_duration,<br>  SUM(is_share) AS shares<br>FROM user_behavior<br>WHERE user_id IN (SELECT user_id FROM orders WHERE amount > 500)<br>GROUP BY user_id</code></td><td>用子查询圈定高价值用户群，再分析其行为模式——为精细化运营提供数据依据</td></tr>'+
'</table>'+

'<h4>1.4 SQL窗口函数（进阶加分）</h4>'+
'<p>当面试官问"如何计算用户次日留存率"，窗口函数是最优雅的答案。</p>'+
'<table class="data-table"><tr><th>函数</th><th>作用</th><th>运营场景</th></tr>'+
'<tr><td><code>ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY date)</code></td><td>给每个用户的访问按时间编号</td><td>取出每个用户的首次/第N次行为——识别用户所处生命周期阶段</td></tr>'+
'<tr><td><code>LAG(date) OVER(PARTITION BY user_id ORDER BY date)</code></td><td>获取上一条记录的日期</td><td>计算相邻两次访问的间隔天数——识别流失前兆（间隔突然变长）</td></tr>'+
'<tr><td><code>SUM(amount) OVER(PARTITION BY user_id ORDER BY date ROWS UNBOUNDED PRECEDING)</code></td><td>累计求和</td><td>用户累计消费金额——判断是否达到VIP升级阈值</td></tr>'+
'</table>'+

'<h4>📝 推荐练习平台</h4>'+
'<ul>'+
'<li><a href="https://www.nowcoder.com/ta/sql" target="_blank"><strong>牛客网SQL题库</strong></a> — 从入门到进阶，有"SQL实战"板块，题目按难度分级，支持在线执行看结果</li>'+
'<li><a href="https://leetcode.cn/problemset/database/" target="_blank"><strong>LeetCode Database</strong></a> — 全英文题目，企业面试原题集中地，刷完50道应付大厂面试足够</li>'+
'<li><a href="https://sqlzoo.net" target="_blank"><strong>SQLZoo</strong></a> — 英文但零门槛，交互式教程，从SELECT开始手把手教，适合完全零基础</li>'+
'<li><strong>练习建议：</strong>每天2道SQL题，先自己写再看答案，强调"理解业务逻辑>记住语法"</li>'+
'</ul>'+

'<h3>📊 第二章：Excel数据透视表——3分钟从数据到报表</h3>'+
'<p>SQL取完数据导出CSV，下一步就是在Excel里做分析。<strong>数据透视表是运营最常用的分析工具，没有之一。</strong></p>'+

'<h4>2.1 3分钟操作流程：原始数据 → 可视化报表</h4>'+
'<div class="highlight-box"><p>'+
'<span class="step-num">1</span> <strong>选中数据区域</strong> → 点击任意数据单元格，Ctrl+A全选（确保无空行空列打断）<br>'+
'<span class="step-num">2</span> <strong>插入透视表</strong> → 菜单栏"插入" → "数据透视表" → 选择"新工作表"（保持源数据干净）<br>'+
'<span class="step-num">3</span> <strong>拖拽字段</strong> → 右侧"透视表字段"面板：把"日期"拖到"行"，把"订单金额"拖到"值"，把"渠道"拖到"列"<br>'+
'<span class="step-num">4</span> <strong>设置值计算方式</strong> → 点击值区域的字段 → "值字段设置" → 选求和/计数/平均值<br>'+
'<span class="step-num">5</span> <strong>插入透视图</strong> → 点击透视表任意位置 → "数据透视图" → 选折线图（趋势）或柱状图（对比）→ 一键生成</p></div>'+

'<h4>2.2 运营常用的4种值计算</h4>'+
'<table class="data-table"><tr><th>计算类型</th><th>使用场景</th><th>操作方式</th></tr>'+
'<tr><td><strong>求和</strong></td><td>各渠道总营收、活动总订单金额</td><td>默认，将金额字段拖入"值"区域即可</td></tr>'+
'<tr><td><strong>计数</strong></td><td>各渠道注册人数、各页面访问次数</td><td>值字段设置 → 计算类型选"计数"（注意：文本字段默认就是计数）</td></tr>'+
'<tr><td><strong>分组（按日/周/月）</strong></td><td>把每天的零散数据汇总为周趋势</td><td>右键日期列 → "组合" → 选择"月"和"年"（可按多层级同时分组）</td></tr>'+
'<tr><td><strong>同比/环比</strong></td><td>本月DAU对比上月涨了多少</td><td>值字段设置 → "值显示方式" → "差异百分比" → 基准字段选日期，基准项选"上一个"</td></tr>'+
'</table>'+
'<div class="callout"><p><strong>效率技巧：</strong>原始数据新增行后，透视表不会自动更新——右键透视表 → "刷新"。如果数据量持续增长，建议把原始区域转成"表格"（Ctrl+T），透视表引用表格名，新增数据自动纳入透视范围。</p></div>'+

'<h3>🔬 第三章：A/B测试统计学基础</h3>'+
'<p>A/B测试是运营决策的"法官"——新功能上不上、文案用哪个、推送什么时间发，<strong>不是你觉得好，是数据说好</strong>。</p>'+

'<h4>3.1 p值——一句人话解释</h4>'+
'<div class="highlight-box"><p><strong>p值 = 假设A和B其实没差别，你还能观察到当前这么大差别的概率。</strong><br>说人话：p值越小 → "纯属巧合"的概率越低 → A和B的差异越可信。<br>'+
'<strong>例子：</strong>新版注册页转化率12%，旧版10%。p=0.03 → 仅有3%的概率这个差异是随机波动造成的 → 基本确认新版确实更好。<br>'+
'<strong>行业标准：</strong>p < 0.05 算"统计显著"（即95%以上的把握）。但p=0.049和0.051没有本质区别——<strong>不要迷信0.05这个阈值</strong>。</p></div>'+

'<h4>3.2 置信区间——效果的真实范围</h4>'+
'<p><strong>定义：</strong>95%置信区间表示"如果重复实验100次，有95次真实效果会落在这个区间内"。<br>'+
'<strong>运营解读：</strong>新版转化率提升2%（95%置信区间：[0.5%, 3.5%]）→ 我们95%确定新版至少能提升0.5%，最多提升3.5%。区间不含0 → 效果显著；区间过宽 → 样本量不够，结论不稳。</p>'+

'<h4>3.3 样本量计算——至少要多少用户</h4>'+
'<p>这是运营最常被问的问题："实验要跑多久？"答案是<strong>先算样本量，再算天数</strong>。</p>'+
'<table class="data-table"><tr><th>参数</th><th>含义</th><th>典型取值</th><th>影响</th></tr>'+
'<tr><td>基准转化率</td><td>对照组当前转化率</td><td>10%（视产品而定）</td><td>转化率越低，所需样本量越大</td></tr>'+
'<tr><td>最小可检测效果（MDE）</td><td>你关心的最小提升幅度</td><td>相对提升10%（即10%→11%）</td><td>想检测越小的提升，需要越多样本</td></tr>'+
'<tr><td>显著性水平 α</td><td>容忍的误报率</td><td>5%（0.05）</td><td>行业默认值，一般不需要改</td></tr>'+
'<tr><td>统计功效（Power）</td><td>真有差异时能检测出来的概率</td><td>80%（0.8）</td><td>80%意味着20%可能漏掉真实效果</td></tr>'+
'</table>'+
'<p><strong>快速估算公式（运营版）：</strong></p>'+
'<div class="highlight-box"><p>'+
'每组所需样本量 ≈ 16 × 转化率×(1-转化率) / (MDE)<sup>2</sup><br>'+
'<strong>举例：</strong>基准转化率10%，期望检测2%的绝对提升（即10%→12%）。<br>'+
'计算：16 × 0.1×0.9 / (0.02)<sup>2</sup> = 16 × 0.09 / 0.0004 = <strong>每组3600人，共7200人</strong><br>'+
'如果每天新增1000用户 → 需要至少7天 → 保险起见跑14天（覆盖完整周周期）</p></div>'+
'<p><strong>在线工具：</strong><a href="https://www.evanmiller.org/ab-testing/sample-size.html" target="_blank">Evan Miller样本量计算器</a>，输入转化率和MDE，自动算所需样本。</p>'+

'<h4>3.4 常见陷阱——不要过早停掉实验</h4>'+
'<table class="data-table"><tr><th>陷阱</th><th>会怎样</th><th>怎么避免</th></tr>'+
'<tr><td><strong>Peeking（偷看）</strong></td><td>每天看一次p值，碰到p<0.05就停——这种做法会让误报率从5%飙升到30%以上。相当于考试时反复改答案直到蒙对</td><td><strong>预设样本量，达成前不看p值</strong>。或者用序贯检验（Sequential Testing），每次检查时自动调高显著性门槛</td></tr>'+
'<tr><td><strong>新奇效应</strong></td><td>改版后前两天数据飙升——用户只是对新界面好奇，一周后打回原形</td><td>至少跑<strong>一个完整用户使用周期</strong>（通常7-14天），等新奇效应消退再看数据</td></tr>'+
'<tr><td><strong>辛普森悖论</strong></td><td>总体数据：新版转化率更高。但按设备拆开：手机端和PC端新版分别都更差——因为新版的用户构成中手机比例更高（手机本身转化率高）</td><td><strong>按核心维度（设备/渠道/新旧用户）做分组分析</strong>，确认每个子群的方向一致</td></tr>'+
'<tr><td><strong>多重检验</strong></td><td>同时测10个指标（转化率/点击率/停留时长/分享率…），总有一个"碰巧"显著。从10个指标里挑一个显著的汇报——这是数据造假</td><td>实验前<strong>注册核心指标（Primary Metric）</strong>，次要指标只是参考。或者用Bonferroni校正（α/指标数）</td></tr>'+
'</table>'+
'<div class="callout"><p><strong>运营A/B测试检查清单：</strong>① 实验前：确定核心指标、计算所需样本量、预估实验天数；② 实验中：不偷看、不干预、不临时改指标；③ 实验后：检查分组均衡性（两组用户结构是否相似），再做统计检验。</p></div>'+

'<h3>📚 第四章：推荐学习资源</h3>'+

'<h4>4.1 书籍——建立分析思维框架</h4>'+
'<table class="data-table"><tr><th>书名</th><th>适合阶段</th><th>核心价值</th><th>关键词</th></tr>'+
'<tr><td><strong>《精益数据分析》</strong><br>Alistair Croll / Benjamin Yoskovitz</td><td>入门必读</td><td>提出"一个指标就够了"——不同商业模式（SaaS/电商/媒体/双边市场）各自只有一个第一指标。读完你会知道自己的产品<strong>现阶段最该盯哪个数</strong></td><td>OMTM、海盗指标AARRR、虚荣指标vs可执行指标</td></tr>'+
'<tr><td><strong>《SQL必知必会》</strong><br>Ben Forta</td><td>SQL零基础</td><td>200页小书，周末两天读完，覆盖日常取数全部语法。每章5分钟，读完立刻能用</td><td>短小精悍、即学即用</td></tr>'+
'<tr><td><strong>《Trustworthy Online Controlled Experiments》</strong><br>Kohavi / Tang / Xu</td><td>进阶A/B测试</td><td>微软/Google/LinkedIn实验平台负责人的合著——就是这帮人在制定行业标准。中文版《关键迭代》</td><td>实践出真知、在线实验圣经</td></tr>'+
'</table>'+

'<h4>4.2 视频课程——零基础快速入门</h4>'+
'<ul>'+
'<li><a href="https://search.bilibili.com/all?keyword=戴师兄+SQL入门" target="_blank"><strong>B站戴师兄《SQL入门》</strong></a> — 中文讲解，节奏舒适，从安装MySQL到写出复杂查询，配合实战案例。还有进阶的《SQL进阶教程》</li>'+
'<li><strong>可汗学院《Statistics and Probability》</strong> — 英文但配中文字幕，用动画解释置信区间、假设检验，没有任何公式恐惧</li>'+
'<li><strong>Coursera《Google Data Analytics Certificate》</strong> — 谷歌官方数据分析认证，覆盖SQL/Tableau/R，适合系统性学习，有中文字幕</li>'+
'</ul>'+

'<h4>4.3 工具——用了就能出结果</h4>'+
'<table class="data-table"><tr><th>工具</th><th>类型</th><th>适用场景</th><th>核心能力</th></tr>'+
'<tr><td><strong>Google Analytics 4</strong></td><td>免费</td><td>网站/小程序用户行为分析</td><td>自动事件追踪、漏斗分析、用户分层（新用户vs回访用户）、自定义报告——部署一行代码即可</td></tr>'+
'<tr><td><strong>神策数据</strong></td><td>SaaS（付费）</td><td>国内App/小程序深度分析</td><td>用户路径分析（桑基图）、留存魔法数字、自定义指标——比GA更符合国内产品逻辑，已有3000+企业客户</td></tr>'+
'<tr><td><strong>GrowingIO</strong></td><td>SaaS（付费）</td><td>增长团队的数据底座</td><td>无埋点自动采集（开发不配合也能用）、A/B测试模块、智能预警——适合数据基础薄弱但想快速起步的团队</td></tr>'+
'<tr><td><strong>Metabase</strong></td><td>开源免费</td><td>小团队自建数据看板</td><td>SQL查询可视化、仪表盘、定时邮件报表——一个运维同事部署一下，全公司都能自助取数</td></tr>'+
'</table>'+

'<h3>🗺️ 运营数据分析学习路线图（30天计划）</h3>'+
'<div class="highlight-box"><p>'+
'<span class="step-num">第1周</span> <strong>SQL基础</strong> — 每天2小时。SELECT/WHERE/JOIN/GROUP BY，配合牛客网每天3道题。周末用一天读完《SQL必知必会》。<br>'+
'<span class="step-num">第2周</span> <strong>Excel实战</strong> — 把自己产品最近一个月的数据导出，用透视表做一份日报模板（含趋势图+渠道对比+Top10用户）。<br>'+
'<span class="step-num">第3周</span> <strong>A/B测试理论</strong> — 读《精益数据分析》核心章节，学p值/置信区间/样本量计算。拿公司一个已完成的实验复现分析过程。<br>'+
'<span class="step-num">第4周</span> <strong>综合实战</strong> — 选一个真实运营问题（如"为什么最近7天转化率下降了"），用SQL取数→Excel分析→输出结论报告。独立走完完整流程。<br>'+
'<strong>里程碑：</strong>30天后你应该能独立完成：取数（SQL）→ 做报表（Excel透视表+透视图）→ 验证假设（A/B测试解读）→ 输出结论。</p></div>'+

'<div class="callout"><p><strong>给AI产品运营的特别提醒：</strong>AI产品的数据分析有一个独特的挑战——<strong>用户与模型的交互质量难以量化</strong>。除了传统的DAU/留存/转化率，你还需要关注：对话轮次中位数、回复有用率（点赞率）、指令遵循准确率、以及模型幻觉对用户体验的影响。建议在常规指标之外，建立一套"AI产品专有数据看板"，把产品经理和算法工程师拉进来一起定义指标口径。</p></div>';
