# -*- coding: utf-8 -*-
"""更新第二步：LEARN_PATHS 归档+刷新 / DAILY_DECISIONS / 全站日期同步 / 版本"""
import io, sys, re, json, datetime, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = BASE + r'\daily_data.js'
now = datetime.datetime.now()
TODAY = now.strftime('%Y-%m-%d')
CN = '%d年%d月%d日' % (now.year, now.month, now.day)
assert TODAY == '2026-09-19'


def j(o):
    return json.dumps(o, ensure_ascii=False, indent=2).replace('\n', '\n  ')


d = open(FP, 'r', encoding='utf-8').read()

# ==================== 1) LEARN_PATHS：归档旧 items + 新 10 条 ====================
learn = [
 {"section":"健身","emoji":"📈","title":"为什么增肌要「每周只推一项」？","content":"渐进超负荷有两个旋钮：次数和负重。如果同一周既加重量又加次数，你无法判断进步来自哪个，也容易因为恢复不过来而停滞。正确做法是交替推进：先把同样负重从 8 次练到 12 次，再加重让次数回落，如此循环。","takeaway":"同时拧两个旋钮 = 看不出进步也恢复不过来。一次只推一个变量，进步才可追踪。"},
 {"section":"健身","emoji":"📏","title":"训练第 1 周该记录什么？","content":"第一周的唯一任务是把基线立起来：每个动作用了多少负重、做了多少次、最后一组还剩几次余力。没有基线，第 4 周你无法判断是进步了还是在原地。体重、腰围、胸围、大腿围、俯卧撑最大次数，这五项是增肌期最有用的追踪指标。","takeaway":"记录不是为了好看，是为了让「有没有进步」变成一个可以被回答的问题。"},
 {"section":"AI","emoji":"🧮","title":"模型量化是什么？为什么它让本地部署变可行？","content":"量化是把模型权重从高精度（如 16 位浮点）压缩到低精度（如 4 位整数）的过程。代价是少量精度损失，收益是显存占用和成本大幅下降——原本需要多卡才能跑动的模型，量化后单卡甚至消费级显卡就能推理。","takeaway":"开源权重 + 量化 = 私有化部署门槛骤降。这也是 9/10 发布的开源模型能真正改变应用成本结构的原因。"},
 {"section":"AI","emoji":"🛡️","title":"AI 内容标识为什么是产品需求，而不只是法务需求？","content":"生成式 AI 的内容标识要求落地后，产品必须回答：哪些内容由 AI 生成、能否溯源、用户是否能区分、出现争议时能否拿出记录。这些都要写进 PRD 的异常与边界部分，并落到日志与人工兜底路径上。","takeaway":"合规不是上线前补的文件，而是设计功能时就要落进流程的约束。"},
 {"section":"运营","emoji":"⭐","title":"留存曲线「走平」意味着什么？","content":"留存曲线通常前期快速下降，之后趋于平缓。曲线开始走平的那个点，代表【愿意长期留下来的人】的比例；走平位置越高，产品价值越强。如果曲线一直往下掉、始终不走平，说明产品没有形成稳定的使用理由。","takeaway":"看留存不是看某一天的数字，而是找曲线在哪走平、平在多高。"},
 {"section":"运营","emoji":"📊","title":"为什么「人均消费次数」比「总消费」更能指导运营？","content":"总消费受头部用户影响极大：一个用户一次买 1 万，就能盖住一百个用户的流失。人均消费次数把规模因素剥离，直接反映【普通用户的使用频率】，而频率才是可以被运营动作影响的变量。","takeaway":"能被你的动作影响的指标才值得盯。总量指标通常是结果，频次类指标才是抓手。"},
 {"section":"财经","emoji":"📈","title":"量能配合：为什么「缩量突破」要警惕？","content":"价格突破关键位时，如果成交量没有同步放大，说明推动突破的资金有限，更多是存量博弈或情绪冲动。这种突破容易被快速反噬，形成假突破；反之放量突破意味着有新增资金认可这个价位。","takeaway":"价格告诉你方向，成交量告诉你这个方向有多少人真的认同。"},
 {"section":"学习","emoji":"🧠","title":"刻意练习：为什么刷「会做的题」没有用？","content":"重复做已经掌握的内容只会带来熟练度错觉，不会带来能力增长。刻意练习的核心是持续攻击不会的部分，并且要有即时反馈——错题本之所以有效，正是因为它把练习范围锁定在薄弱点上。","takeaway":"判断练习是否有效，看它让你不舒服的程度。全都做得很顺，说明选错了题目。"},
 {"section":"求职","emoji":"🎯","title":"AI 产品岗 JD 的变化说明了什么？","content":"岗位描述从【熟悉大模型工具】转向【能判断什么该用与不该用模型、能定义验收标准与兜底路径】。这个转向把考核重点从工具熟练度移到了判断力与方案能力——对转型者是机会，因为判断力可以通过系统训练补齐，而不是靠工龄堆出来。","takeaway":"当岗位要求从「会用」转向「会判断」，作品集的分量就超过了简历上的年限。"},
 {"section":"生活","emoji":"🏛️","title":"秋分前后为什么是全年最容易感冒的两周？","content":"昼夜温差接近 9℃ 时，白天出汗、夜间受凉的概率同时上升，而身体的体温调节适应需要时间。加上这个阶段空调还在用、窗户又常开，冷热切换频繁。早晚加一件薄外套、运动后及时换掉湿衣，比事后吃药划算得多。","takeaway":"季节交替期的健康策略不是「扛」，而是减少身体的调节负担。"}
]

lm = re.search(r'var LEARN_PATHS = \{([\s\S]*?)\n\};', d)
if lm:
    body = lm.group(1)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', body)
    am = re.search(r'archive:\s*\{([\s\S]*)\}\s*$', body)
    if im and am:
        old_items = im.group(1).strip()
        old_arch = re.sub(r',\s*$', '', am.group(1).strip())
        new_body = ('\n  updated: "%s",\n  current_day: 13,           // 当前学到第几天\n'
                    '  items: %s,\n'
                    '  // 历史累积库：archive 只存【历史】日期（当天内容放 items，不进 archive）\n'
                    '  archive: {\n    "2026-09-14": [\n%s\n    ]'
                    '%s\n  }\n') % (
            TODAY, j(learn), old_items, (',\n' + old_arch) if old_arch else '')
        d = d[:lm.start()] + 'var LEARN_PATHS = {' + new_body + '};' + d[lm.end():]
        print('✅ 小白课堂 → 10 条（9/19），旧 10 条已归档为 2026-09-14')

# ==================== 2) DAILY_DECISIONS（9/19 周六）====================
decisions = [
 {"icon":"💪","action":"增肌第 1 周复盘：整理各动作的负重与次数，定下下周加重目标","why":"没有基线就没有进步标准；下周要按「每周只推一项」加重，必须先知道这周的起点","how":"翻出这周的训练记录 → 逐个动作写下：负重 × 次数 × 组数 → 挑 1-2 个动作作为下周加重的对象（其余保持）","priority":"P0"},
 {"icon":"⚖️","action":"体重校准：早晨空腹称重，判断热量该加还是该减","why":"增肌期唯一的热量校准依据就是体重变化速度，光靠感觉无法判断","how":"空腹称重并与上周对比：涨 0.25-0.5kg = 保持；不涨 = 每天加 200 kcal；涨超 0.75kg = 减 200 kcal（只调主食）","priority":"P0"},
 {"icon":"🎓","action":"补上本周训练平台进度，至少完成 2 天任务","why":"9/14-9/19 这一周的计划任务若中断，30 天节奏会被打散","how":"打开训练平台 → 按天补做未完成的任务 → SQL 与数据集实验室优先（两个方向的硬门槛）","priority":"P0"},
 {"icon":"📈","action":"周末复盘：验证「AI 硬件是结构主线」这个判断是否成立","why":"9/11 提出的判断需要一个明确结论，验证过才叫判断，没验证只是观点","how":"回看这一周：①3900 关口是否有效站稳 ②AI 硬件（覆铜板/光模块）相对强度是否延续 ③量能是否配合 → 把结论回填到判断台账","priority":"P1"},
 {"icon":"🎬","action":"Re:Zero 补番：最终话 9/30，倒计时 11 天","why":"夺还篇是全季认知博弈密度最高的段落，补番窗口正在收窄","how":"按动漫区的观看顺序补到最新；把 9/30 加进日历提醒","priority":"P1"}
]
m = re.search(r'var DAILY_DECISIONS = \{\s*\n\s*updated:\s*"[^"]+",\s*\n\s*items:\s*\[[\s\S]*?\n\s*\]\s*\n\};', d)
if m:
    d = d[:m.start()] + 'var DAILY_DECISIONS = {\n  updated: "%s",\n  items: %s\n};' % (TODAY, j(decisions)) + d[m.end():]
    print('✅ 今日待办 → 5 条（9/19 周六版）')

# ==================== 3) 全站日期同步 ====================
pat = re.compile(r'(["\']?updated["\']?\s*:\s*)(["\'])(2026-09-1[0-9])\2')
d, n1 = pat.subn(lambda m: m.group(1) + m.group(2) + TODAY + m.group(2), d)
d, n2 = re.subn(r'("update_date":\s*")([^"]+)(")', lambda m: m.group(1) + CN + m.group(3), d)
d, n3 = re.subn(r'("update_time":\s*")([^"]+)(")',
                lambda m: m.group(1) + now.strftime('%Y-%m-%dT%H:%M:%S+08:00') + m.group(3), d)
print('✅ 日期同步：updated %d 处 · update_date %d 处 · update_time %d 处' % (n1, n2, n3))

# 摘要里的当日表述
fixes = [('9月14日（周一）', '9月19日（周六）'), ('9月14日', '9月19日'),
         ('2026年9月14日', CN), ('目标调整（9/14）', '目标调整（9/19）')]
c = 0
for a, b in fixes:
    if a in d:
        c += d.count(a); d = d.replace(a, b)
print('✅ 摘要日期文本：%d 处' % c)

# ==================== 4) 版本 ====================
d = d.replace('var SITE_VERSION = "1.8.15";', 'var SITE_VERSION = "1.8.16";')
d = re.sub(r'版本1\.8\.1[0-9]', '版本1.8.16', d)
print('✅ 版本 → 1.8.16')

open(FP, 'w', encoding='utf-8').write(d)
r = subprocess.run(['node', '--check', FP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:200])

# index.html 版本引用
IP = BASE + r'\index.html'
h = open(IP, 'r', encoding='utf-8').read()
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=1.8.16', h)
open(IP, 'w', encoding='utf-8').write(h)
print('✅ index.html 引用 → 1.8.16')
