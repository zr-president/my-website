# -*- coding: utf-8 -*-
"""① 待办/要闻改为周一语境 ② 版本 1.8.15 ③ 审计改为对比系统真实日期"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
d = open(FP, 'r', encoding='utf-8').read()


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


# ---------- 1) 待办：周一版 ----------
decisions = [
 {"icon":"💪","action":"新版周计划 Day1：上肢推 + 腹肌A（俯卧撑必须加负重）","why":"今天（周一）是增肌版计划第一天；你自重俯卧撑能做 60 个，已完全适应，不加负重只练耐力","how":"背包放 2-3kg 书 → 负重俯卧撑 4×8-12 ｜ 下斜 4×10-12 ｜ 拉力绳推举 3×12-15 ｜ 拉力绳卷腹 4×15；每组最后 2-3 次要很吃力","priority":"P0"},
 {"icon":"🍽️","action":"今天是训练日：按 2500 kcal 吃，练后 30-60 分钟补蛋白+快碳","why":"增肌必须有轻微热量盈余；练后窗口期补 乳清蛋白 1 勺 + 香蕉，恢复更快、下次更有劲","how":"照饮食助手页的训练日食谱执行；练前 1 小时补 1 片全麦面包；全天饮水 ≥2.5L","priority":"P0"},
 {"icon":"🎓","action":"在能力训练平台点【开始 30 天计划】，今天跑 Day 1","why":"30 天 91 个任务覆盖 SQL/数据分析/业务分析/AI 产品四条线，解决【不知道先学什么】","how":"打开训练平台 → 开始计划 → 今天的任务：读数据集字段、做能力雷达自评、SQL L1 前 2 题；每完成一项打勾","priority":"P0"},
 {"icon":"📈","action":"A股今日开盘：验证上周五的结论（能否收回 3900）","why":"上周五沪指收 3888.11 失守 3900、成交 1.97 万亿，AI 硬件是结构主线——结论必须可验证","how":"盘后回填：①是否收回 3900 ②AI 硬件（覆铜板/元件）是否延续 ③若跌破 3850 则调整周期延长","priority":"P1"},
 {"icon":"📏","action":"建立增肌期基线数据（若昨天未做）","why":"没有基线就无法判断 12 周后是真长肌肉还是只涨脂肪","how":"早晨空腹量体重与腰围（肚脐水平）、胸围、大腿；测一次俯卧撑最大次数；拍正面+侧面照 → 填入健身区 6 指标追踪表","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + ('var DAILY_DECISIONS = {\n  updated: "' + TODAY + '",\n  items: ' + j(decisions) + '\n};') + d[m.end():]
    print('OK 待办 → 周一版 5 条')

# ---------- 2) 要闻 A股卡改周一语境 ----------
d = d.replace('昨日沪指收 3888.11（643 家涨 / 4870 家跌）', '上周五（9/11）沪指收 3888.11（643 家涨 / 4870 家跌）')
d = d.replace('今日需验证的判断：若继续跌破 3850 支撑', '今日开盘需验证：若继续跌破 3850 支撑')
d = d.replace('沪指 3888 点失守 3900 后观察企稳信号', '沪指 3888 点失守 3900：今日开盘观察能否收回')
print('OK 要闻 A股卡 → 周一语境')

# ---------- 3) 版本 1.8.15 ----------
d = d.replace('var SITE_VERSION = "1.8.14";', 'var SITE_VERSION = "1.8.15";')
d = d.replace('版本1.8.14', '版本1.8.15')
d = re.sub(r'版本1\.8\.1[0-9]', '版本1.8.15', d)
print('OK 版本 → 1.8.15')
open(FP, 'w', encoding='utf-8').write(d)

# index.html 版本引用
IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.15', h)
open(IP, 'w', encoding='utf-8').write(h)
print('OK index.html 引用 → 1.8.15')

# ---------- 4) 审计改为对比系统真实日期 ----------
CP = BASE + r'\scripts\check_consistency.py'
c = open(CP, 'r', encoding='utf-8').read()
c = c.replace("const today = c.DAILY_BRIEFING.date;",
              "const sysToday = new Date(); const today = sysToday.getFullYear()+'-'+String(sysToday.getMonth()+1).padStart(2,'0')+'-'+String(sysToday.getDate()).padStart(2,'0');\nconst contentDate = c.DAILY_BRIEFING.date;")
c = c.replace("console.log(JSON.stringify({today, bad, okCount: okList.length, arch, clash}));",
              "console.log(JSON.stringify({today, contentDate, bad, okCount: okList.length, arch, clash}));")
c = c.replace("    today = info['today']\n",
              "    today = info['today']\n"
              "    if info.get('contentDate') != info['today']:\n"
              "        err('站点日期(%s)与系统日期(%s)不一致 —— 更新时必须读取系统时钟' % (info.get('contentDate'), info['today']))\n"
              "    else:\n"
              "        ok('站点日期与系统真实日期一致：%s' % today)\n")
open(CP, 'w', encoding='utf-8').write(c)
print('OK 审计已改为对比系统真实日期')

r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
