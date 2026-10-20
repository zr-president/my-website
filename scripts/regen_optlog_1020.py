# -*- coding: utf-8 -*-
"""重新生成优化日记的建议：保留历史（已完成/已归档），替换全部待办为 12 条新建议
   设计原则：
   ① 实用性 —— 纯前端可做、零后端、不依赖注册账号
   ② 创新性 —— 做出【机制】而不是加【板块】（行为闭环 / 可信度 / 可分享）
   ③ 求职价值 —— 每条都能在面试里讲成「我做过的一个产品决策」
"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()

NEW = [
 # ===== P0：本月做，求职直接受益 =====
 (112, "求职功能", "JD 匹配度体检器：粘贴岗位描述 → 本地打分 → 指出缺口", "P0", "待办",
  "投递前 60 秒自检，避免盲投。做法：粘贴任意 JD → 用本地能力映射表（SQL/指标拆解/A-B实验/AI产品/增长/工具链/行业理解）逐项关键词命中打分 → 输出「已匹配 N 项 / 缺失 M 项 / 简历该补哪一句」。纯前端规则引擎，无需 API、可离线。创新点：它不是简历生成器，而是【投递前的反向体检】——先看缺口，再决定投不投"),

 (113, "求职功能", "「招聘视角」30 秒模式：一键切成 HR 看得懂的一屏", "P0", "待办",
  "招聘方不会探索 17 个板块。做法：一键切换独立视图（如 #hire），一屏内只留 定位（我是谁+要什么）+ 3 个最强证据 + 作品集入口 + 联系方式，其余全部收起，可独立分享链接。与 #106 Hero 改造的区别：#106 是首屏信息密度优化，本条是【给陌生人看的专用视图】。价值：把「信息中枢」和「求职名片」拆成两种用途"),

 (114, "体验优化", "「今日行动」可打勾 + 连续天数：把「读到」变成「做到」", "P0", "待办",
  "现状：今日行动只是静态文本，读完即结束。做法：tip 渲染成可勾选 checklist → localStorage 持久化 → 顶部显示「连续执行 X 天」。成本极低（约 80 行代码），但形成行为闭环。价值：① 你真会去做 ② 面试可讲「我用 streak 机制解决内容型产品的执行力问题」"),

 # ===== P1：下月，做出差异化 =====
 (115, "求职功能", "作品集一键导出：一页 PDF + 1080×1920 分享长图", "P1", "待办",
  "做法：① window.print() + 专用 print CSS，把「AI 观察 + 产品分析 + 能力雷达」排成一页纸，Ctrl+P 存 PDF；② Canvas 绘制分享长图。零依赖、零后端。用途：邮件附件投递 / 朋友圈曝光 / 面试现场直接给人看。价值：把「网站」变成「可发送的资产」"),

 (116, "数据优化", "逐条数据来源与更新角标：从「今日已核查」升级为「本条更新于X·来源Y」", "P1", "待办",
  "现状：全站只有一个模糊的「今日更新已核查」徽章。做法：给 INSIGHTS 每个分区加 sources 数组，渲染时在角落显示来源与时间戳。价值：面试官问「这些数据哪来的」时能当场点开——这是可信度，也是产品思维（AI 产品最缺的就是可追溯性）"),

 (117, "机制创新", "观点演化时间线：保留 7 次快照，能切换「7 天前 vs 现在」", "P1", "待办",
  "做法：每次更新把该分区 summary 哈希后存入 localStorage（仅保留最近 7 次），提供「看变化」入口。价值：① 自己复盘判断有没有迭代 ② 面试可展示「我对一件事的看法是如何随证据修正的」——比结论本身更有说服力。创新点：多数人只展示结论，你展示的是【判断的进化过程】"),

 (118, "内容优化", "周报自动生成 + 分享长图：本周我关注的 7 件事", "P1", "待办",
  "做法：汇总近 7 天 DAILY_BRIEFING → 生成周报页 + Canvas 长图，一键保存。零后端（数据本来就在本地）。用途：小红书/朋友圈持续曝光 + 证明「连续输出能力」。价值：日更的成本已经付出，周报是【同一份内容的第二次变现】"),

 (119, "性能优化", "内联 JS 200KB 外置 + 历史数据拆分（每日更新只重下 48KB）", "P1", "待办",
  "实测：首屏 1.28MB（index.html 307KB 含 200.5KB 内联 JS + 4 个脚本 976KB）。做法：① 内联 JS 拆成 app.js → 内容更新时 HTML 只重下 48KB（现在每次都重下 307KB）；② OPTIMIZATION_LOG(22KB) + LEARN_PATHS.archive(34KB) 拆到 history_data.js 按需加载 → 首屏再 -56KB。预期：首屏 1.28MB → 约 0.95MB，重复访问省 200KB+"),

 # ===== P2：有空再做 =====
 (120, "学习机制", "间隔重复复习（SM-2）：每天从历史题库抽 3 题", "P2", "待办",
  "做法：从 DAILY_QUIZ / LEARN_PATHS 历史库按 SM-2 算法每日抽 3 题，答错的更早再出现。纯前端实现，无需后端。价值：把「学过」变成「记住」——面试前两周的复习效率远高于重新通读。呼应 #101 学习路径：路径解决「学什么」，此题解决「记住没」"),

 (121, "功能优化", "PWA 离线可用：通勤/断网也能看今日内容", "P2", "待办",
  "做法：加 manifest.json + Service Worker，缓存今日内容与核心 JS。收益：① 地铁上可读（国内网络不稳）② 面试现场断网也能演示——这本身是个好故事。注意：GitHub Pages 支持 HTTPS，满足 SW 要求"),

 (122, "视觉优化", "可访问性补全：aria-label + 键盘导航 + 焦点可见", "P2", "待办",
  "实测现状：整站 aria-label 为 0、h1 有 2 个（侧栏品牌 + 主区）、无 :focus-visible 样式。做法：补约 20 处 aria-label、h1 收敛为 1 个、加键盘焦点样式、检查 Tab 顺序。价值：既是基础质量，也是「产品细节」的面试谈资（多数个人站完全不管可访问性）"),

 (123, "求职功能", "投递看板规则提醒：7 天无回应→跟话术；面试前 1 天→备 STAR", "P2", "待办",
  "现状：#107 投递作战台只是状态记录，不会主动提醒。做法：加本地规则引擎——投递 7 天无回应 → 提示「该跟进」并生成跟进话术模板；面试前 1 天 → 提示「准备 3 个 STAR 案例」；连续 5 天零动作 → 提示「本周投递量为 0」。无需后端，纯规则。价值：把看板从「记录工具」变成「执行助手」"),
]

# ---------- 解析现有条目（保留 已完成 / 已归档）----------
entries = re.findall(r'\{id:(\d+), cat:"([^"]*)", title:"((?:[^"\\]|\\.)*)", desc:"((?:[^"\\]|\\.)*)", priority:"([^"]*)", status:"([^"]*)"\}', d)
print('解析到现有条目: %d 条' % len(entries))
keep = [e for e in entries if e[5] in ('已完成', '已归档')]
drop = [e for e in entries if e[5] not in ('已完成', '已归档')]
print('保留(已完成/已归档): %d 条 | 替换掉: %d 条 → %s' % (
    len(keep), len(drop), [e[0] for e in drop]))

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

# ---------- 重建数组 ----------
lines = []
for e in keep:
    lines.append('    {id:%s, cat:"%s", title:"%s", desc:"%s", priority:"%s", status:"%s"},' % (
        e[0], e[1], e[2], e[3], e[4], e[5]))
for (i, cat, title, pri, st, desc) in NEW:
    lines.append('    {id:%d, cat:"%s", title:"%s", desc:"%s", priority:"%s", status:"%s"},' % (
        i, cat, esc(title), esc(desc), pri, st))

new_arr = '  suggestions: [\n' + '\n'.join(lines) + '\n  ]'

# ---------- 替换 suggestions 数组 ----------
i_opt = d.find('var OPTIMIZATION_LOG')
m = re.search(r'suggestions:\s*\[', d[i_opt:])
s = i_opt + m.start()
depth, k = 1, i_opt + m.end()
while k < len(d) and depth > 0:
    if d[k] == '[': depth += 1
    elif d[k] == ']': depth -= 1
    k += 1
e_arr = k
d = d[:s] + new_arr + d[e_arr:]

# ---------- 更新统计字段 ----------
total = len(keep) + len(NEW)
implemented = len([e for e in keep if e[5] == '已完成'])
d = re.sub(r'(var OPTIMIZATION_LOG = \{\s*\n  date: ")[^"]*(")', r'\g<1>2026-10-20\g<2>', d, count=1)
d = re.sub(r'(total_suggestions:\s*)\d+', r'\g<1>%d' % total, d, count=1)
d = re.sub(r'(total_implemented:\s*)\d+', r'\g<1>%d' % implemented, d, count=1)
d = re.sub(r'(streak_days:\s*)\d+', r'\g<1>44', d, count=1)
print('统计：total=%d · implemented=%d · streak=44' % (total, implemented))

# 版本
d = d.replace('var SITE_VERSION = "1.8.28";', 'var SITE_VERSION = "1.8.29";')
d = re.sub(r'版本1\.8\.2[0-9]', '版本1.8.29', d)

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:400])

v = subprocess.run(['node', '-e', r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const L=c.OPTIMIZATION_LOG;
console.log('date:', L.date, '| total:', L.total_suggestions, '| implemented:', L.total_implemented, '| streak:', L.streak_days);
console.log('suggestions:', L.suggestions.length, '条');
const st={}; L.suggestions.forEach(s=>st[s.status]=(st[s.status]||0)+1);
console.log('状态:', JSON.stringify(st));
console.log('');
console.log('=== 新增建议 ===');
L.suggestions.filter(s=>s.id>=112).forEach(s=>console.log('  #'+s.id+' ['+s.cat+'] ['+s.priority+'] '+s.title));
"""], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(v.stdout or v.stderr[:400])
