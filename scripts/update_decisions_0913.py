# -*- coding: utf-8 -*-
"""更新 DAILY_DECISIONS（内容仍是旧腹肌计划）与 AI_OBSERVATIONS（补 9/13 一条）"""
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\daily_data.js'
d = open(FP, 'r', encoding='utf-8').read()


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


# ---------- 1) DAILY_DECISIONS：9/13（周日）当天待办 ----------
decisions = [
 {"icon":"💪","action":"建立增肌期基线数据：体重/腰围/胸围/大腿/俯卧撑最大次数 + 拍正面照","why":"新版计划从增肌出发，没有基线就无法判断 12 周后是真长肌肉还是只涨脂肪","how":"早晨空腹量腰围（肚脐水平）、体重；俯卧撑测一次最大次数（现 60 个）；拍正面+侧面照存档 → 填入健身区的 6 指标追踪表","priority":"P0"},
 {"icon":"🍽️","action":"今天是休息日：按 2300 kcal 吃，但蛋白质保持 130g 不减","why":"休息日正是肌肉修复窗口，砍蛋白等于白练；热量只减主食、不减蛋白","how":"在训练日食谱基础上去掉练前与练后加餐，午餐晚餐各加半碗主食；把那勺乳清蛋白挪到早餐","priority":"P0"},
 {"icon":"📅","action":"明天（周一）开始新版周计划：上肢推 + 腹肌A，俯卧撑要加负重","why":"你能一口气做 60 个标准俯卧撑，说明自重已完全适应——不加负重只练耐力不长肌肉","how":"背包里放 2-3kg 书 → 俯卧撑 4×8-12 做到最后 2-3 次很吃力；记得记录当天的负重与次数作为下周基准","priority":"P0"},
 {"icon":"🎓","action":"在能力训练平台点【开始 30 天计划】，把 Day 1 定在明天","why":"30 天 91 个任务覆盖 SQL/数据分析/业务分析/AI 产品四条线，解决【不知道先学什么】","how":"打开训练平台首页 → 点开始计划 → 明天起每天 40-60 分钟按天打勾；进度会自动回流到本站侧边栏","priority":"P1"},
 {"icon":"📈","action":"周末休市：把上周五的盘面结论写成一句话，等周一验证","why":"沪指收 3888.11 失守 3900，成交 1.97 万亿，AI 硬件是结构主线——结论要可验证","how":"写下：①能否收回 3900 ②AI 硬件（覆铜板/元件）是否延续 ③若跌破 3850 则调整周期延长；周一收盘后回填结果","priority":"P1"}
]

m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    new = ('var DAILY_DECISIONS = {\n  updated: "2026-09-13",\n  items: ' + j(decisions) + '\n};')
    d = d[:m.start()] + new + d[m.end():]
    print('OK DAILY_DECISIONS → 5 条（9/13 周日版）')
else:
    print('MISS DAILY_DECISIONS')

# ---------- 2) AI_OBSERVATIONS：补 9/13 一条 ----------
m2 = re.search(r'var AI_OBSERVATIONS = \[\s*\n', d)
if m2 and '能力要求从' not in d:
    item = ('  {date:"2026-09-13", topic:"AI 产品岗能力要求从「会用工具」转向「会定义边界」",'
            ' summary:"本周多个招聘需求的能力描述正在变化：过去写【熟悉大模型工具/Prompt 工程】，'
            '现在更多写【能判断什么该用与不该用模型、能定义验收标准与兜底路径】。'
            '这一转向意味着 AI 产品的门槛从【会玩工具】上移到【能对不确定性负责】。"},\n')
    d = d[:m2.end()] + item + d[m2.end():]
    print('OK AI_OBSERVATIONS 已补 1 条 2026-09-13')
else:
    print('SKIP AI_OBSERVATIONS')

open(FP, 'w', encoding='utf-8').write(d)

# 校验
import subprocess
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法:', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])
