import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

filepath = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find OPTIMIZATION_LOG start line
opt_start = None
opt_end = None
for i, line in enumerate(lines):
    if line.strip() == 'var OPTIMIZATION_LOG = {':
        opt_start = i
    if opt_start and line.strip() == '};' and i > opt_start + 10:
        opt_end = i
        break

print(f"OPTIMIZATION_LOG lines {opt_start}-{opt_end}")

# Count currently implemented
implemented_count = 0
for i in range(opt_start, opt_end):
    if 'status:"已完成"' in lines[i]:
        implemented_count += 1

print(f"Currently implemented: {implemented_count}")

# Build new suggestions block with 5 new entries for 8/10
new_suggestions = [
    '    {id:1, cat:"已归档", title:"AI追踪板块周报自动生成", desc:"每周一自动汇总上周AI融资/模型发布/价格变动→已集成至INSIGHTS.ai-track周度总结", priority:"P1", status:"已完成"},\n',
    '    {id:2, cat:"已归档", title:"cron更新后自动验证关键板块内容", desc:"检查DAILY_BRIEFING/INSIGHTS/PICKS非空+日期正确→daily_data.js增加校验注释标记", priority:"P1", status:"已完成"},\n',
    '    {id:3, cat:"已归档", title:"黑暗模式下增加深蓝/墨绿配色微调", desc:"dark模式下增加navy(深蓝#1a1f3a)和teal(墨绿#0d3b3b)两种新的accent变体选项", priority:"P2", status:"已完成"},\n',
    '    {id:4, cat:"已归档", title:"AI查询框增加历史搜索记录", desc:"localStorage存储最近10条查询+下拉快捷选择→侧边栏搜索框增强", priority:"P2", status:"已完成"},\n',
    '    {id:5, cat:"已归档", title:"各板块增加热门标签快速筛选", desc:"首页分类卡片显示本周最热3个标签+点击筛选相关板块", priority:"P2", status:"已完成"},\n',
    '    {id:6, cat:"已归档", title:"DAILY_BRIEFING卡片增加分享按钮", desc:"每条要闻卡片右下角增加【复制链接/分享到微信】按钮，方便转发讨论", priority:"P2", status:"已完成"},\n',
    '    {id:7, cat:"已归档", title:"每日一词(DAILY_VOCAB)板块上线", desc:"10个跨领域术语(AI/金融/科技/数据/产品)+首页展示3个+换一批+查看全部+展开实例", priority:"P1", status:"已完成"},\n',
    '    {id:8, cat:"已归档", title:"AI模型价格/能力实时对比表(百分制评分)", desc:"12款主流模型+同系列区分(Flash/Pro/Luna/Sol)+智能/性价比/速度百分制评分+最新调价标注+AI_MODEL_COMPARISON数据对象+index.html渲染表", priority:"P1", status:"已完成"},\n',
    '    {id:9, cat:"已归档", title:"板块详情页增加【返回顶部】浮动按钮", desc:"长内容板块(INSIGHTS)阅读到底部后一键返回顶部→index.html L479已实现fabTop浮动按钮+scrollY>600触发", priority:"P2", status:"已完成"},\n',
    '    {id:10, cat:"已归档", title:"知识库自动去重与合并", desc:"knowledge_base/每天新增文件自动与已有文件比对去重→scripts/dedup_kb.py实现跨日段落级去重(合并6处冗余)", priority:"P1", status:"已完成"},\n',
    '    {id:11, cat:"已归档", title:"三层路由+18板块+悬浮渐变+密码锁", desc:"7/26-31完成", priority:"P0", status:"已完成"},\n',
    '    {id:12, cat:"已归档", title:"GA+Claude双重更新+TOC+AI追踪", desc:"8/1-4完成", priority:"P0", status:"已完成"},\n',
    '    {id:13, cat:"已归档", title:"待办详情+分享+语音+简历+练歌", desc:"7/29-8/3完成", priority:"P0", status:"已完成"},\n',
    '    {id:14, cat:"已归档", title:"知识库1561条+全板块科普reasoning", desc:"7/27-8/4完成", priority:"P0", status:"已完成"},\n',
    '    {id:15, cat:"已归档", title:"防崩机制+优化日记12/12", desc:"8/5完成", priority:"P0", status:"已完成"},\n',
    '    {id:16, cat:"已归档", title:"TOC目录+AI价格+Prompt模板", desc:"8/5完成", priority:"P0", status:"已完成"},\n',
    '    {id:17, cat:"已归档", title:"SpaceX崩盘专题+中国AI霸榜+谷歌重组+Meta Muse Code+L3国标专题", desc:"8/6每日更新全部INSIGHTS reasoning+DAILY_BRIEFING重写+PICKS全面刷新", priority:"P0", status:"已完成"},\n',
    '    {id:18, cat:"已归档", title:"AI周报+暗色navy/teal配色+搜索历史+标签筛选+板块自验", desc:"8/6实现优化建议1-5", priority:"P0", status:"已完成"},\n',
    '    {id:19, cat:"已归档", title:"PICKS动画/音乐/小说/游戏/电影/学习/AI追踪全面更新", desc:"8/6基于最新搜索结果→Re:Zero倒计时/天蚕土豆新书/Sandustry/八仙12亿/中国AI霸榜", priority:"P0", status:"已完成"},\n',
    '    {id:20, cat:"已归档", title:"INSIGHTS 14板块全部更新reasoning科普格式", desc:"8/6所有板块增加🔍发生什么→🤔为什么→📊术语解释→💡启示四层科普", priority:"P0", status:"已完成"},\n',
    '    {id:21, cat:"已归档", title:"知识库5板块新增2026-08-06日文件", desc:"8/6: ai/stock/news/movie/novel五个核心板块追加今日知识", priority:"P0", status:"已完成"},\n',
    '    {id:22, cat:"已归档", title:"Grok 4.6发布+SpaceX反弹+DeepSeek涨价+Alphabet发债+英伟达降配五大专题", desc:"8/7每日更新全部INSIGHTS reasoning+DAILY_BRIEFING重写+PICKS全面刷新+VOCAB全新10词", priority:"P0", status:"已完成"},\n',
    '    {id:23, cat:"已归档", title:"PICKS动画/音乐/小说/游戏/电影/学习/AI追踪全面更新8/7版", desc:"8/7: Stray Kids发售+去你的岛首映+大唐妖探明日上映+Grok 4.6发布+SpaceX Terafab", priority:"P0", status:"已完成"},\n',
    '    {id:24, cat:"已归档", title:"INSIGHTS 17处日期+stock/ai-track/movie/news内容更新", desc:"8/7 stock reasoning重写(立秋+量价背离+DeepSeek涨价+英伟达HBM降配)", priority:"P0", status:"已完成"},\n',
    '    {id:25, cat:"已归档", title:"DAILY_VOCAB全新10词(8/7版):HBM/量价背离/价值定价/Terafab等", desc:"覆盖科技(AI/HBM/Terafab/Post-training)+金融(量价背离/负FCF/战配/超额认购)+产品(价值定价/BE美学)", priority:"P0", status:"已完成"},\n',
    '    {id:26, cat:"已归档", title:"板块详情页返回顶部浮动按钮确认", desc:"确认FAB已存在(index.html L479)且在section-detail视图正常工作——标记为已完成", priority:"P1", status:"已完成"},\n',
    '    {id:27, cat:"设计优化", title:"AI对比表综合评分增加权益权重选项", desc:"当前综合=50%智能+35%性价比+15%速度·可考虑增加【生态/多模态/开源】等维度让评分更全面", priority:"P2", status:"待实施"},\n',
    '    {id:28, cat:"数据优化", title:"Qwen3.8开源状态跟踪与数据更新", desc:"8/10千问预计开源Max+27B→需更新AI_MODEL_COMPARISON中开源状态/价格/benchmark数据·开源后价格可能调整", priority:"P1", status:"待实施"},\n',
    '    {id:29, cat:"稳定性", title:"INSIGHTS编辑增加git备份安全机制 🆕", desc:"今日INSIGHTS批量更新时脚本替换错误导致文件从568行降至13行(全损)→通过git checkout恢复。建议：每次编辑daily_data.js前自动git stash→编辑后自动语法校验→失败则回滚。或改为JSON格式用标准解析器编辑", priority:"P0", status:"待实施"},\n',
    '    {id:30, cat:"内容优化", title:"网站版本号统一管理 🆕", desc:"当前版本号散落在daily_data.js(1.2.9)、WEBSITE_GUIDE(1.2.8未同步)、index.html三处→应统一为单一变量或至少每次更新时三处同步", priority:"P1", status:"待实施"},\n',
    '    {id:31, cat:"内容优化", title:"8/10知识库文件补充(ai/stock/movie/novel) 🆕", desc:"今天新增了4个核心板块的knowledge_base文件→但部分昨日板块(如gaming/learning/career)也应补充→按【新增当日+补昨日遗漏】原则每日维护知识库目录", priority:"P1", status:"待实施"},\n',
    '    {id:32, cat:"功能优化", title:"AI模型对比表增加【安全/对齐】评分维度 🆕", desc:"呼应OpenAI Astra暂停事件→AI安全成为产业刚需→在对比表中增加【安全评级】(开源透明度/安全围栏/红队测试公开度)→让评分体系从3维扩展至4维", priority:"P2", status:"待实施"},\n',
    '    {id:33, cat:"体验优化", title:"INSIGHTS板块增加【今日更新摘要】快速定位 🆕", desc:"INSIGHTS共17个板块→每日更新6-8个→用户不知道哪些是新的。建议：在INSIGHTS首页顶部增加【今日更新: stock·ai-track·movie·learning·career·news】标签行→点击跳转对应板块", priority:"P2", status:"待实施"},\n',
]

# Find the suggestions array in current lines
suggestions_start = None
suggestions_end = None
for i in range(opt_start, opt_end):
    if 'suggestions: [' in lines[i]:
        suggestions_start = i
    if suggestions_start and i > suggestions_start and ']' in lines[i].strip() and lines[i].strip().endswith(']'):
        suggestions_end = i
        break

print(f"Suggestions array: lines {suggestions_start}-{suggestions_end}")

# Replace suggestions array
lines[suggestions_start:suggestions_end+1] = ['  suggestions: [\n'] + new_suggestions + ['  ]\n']

# Update counts
for i in range(opt_start, opt_start + 5):
    if 'total_suggestions:' in lines[i]:
        lines[i] = '  total_suggestions: 33,\n'
        print(f"Updated total_suggestions: line {i}")
    if 'total_implemented:' in lines[i]:
        lines[i] = '  total_implemented: 26,\n'
        print(f"Updated total_implemented: line {i}")
    if 'streak_days:' in lines[i]:
        lines[i] = '  streak_days: 20,\n'
        print(f"Updated streak_days: line {i}")

# Fix WEBSITE_GUIDE version 1.2.8 → 1.2.9
for i, line in enumerate(lines):
    if '版本1.2.8。新增' in line and 'WEBSITE_GUIDE' not in line:
        lines[i] = line.replace('版本1.2.8。新增', '版本1.2.9。新增')
        print(f"Fixed WEBSITE_GUIDE version: line {i}")
        break

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n✅ OPTIMIZATION_LOG updated! Total lines: {len(lines)}")
