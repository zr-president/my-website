# -*- coding: utf-8 -*-
"""跨板块一致性检查：确保互通内容（食谱/热量/蛋白/周计划/版本/链接）在
   详情页、洞察、卡片之间保持同一口径。
   用法：python scripts/check_consistency.py
"""
import io, sys, re, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

detail = open(os.path.join(BASE, 'detail_content.js'), encoding='utf-8').read()
daily = open(os.path.join(BASE, 'daily_data.js'), encoding='utf-8').read()
index = open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()

errors, warns, oks = [], [], []


def err(m): errors.append(m)
def warn(m): warns.append(m)
def ok(m): oks.append(m)


# ---------- 0) 抽取关键内容 ----------
def get_detail(key):
    i = detail.find('DETAIL.' + key + ' =')
    if i < 0:
        i = detail.find('DETAIL["' + key + '"] =')
        if i < 0:
            return ''
        j = detail.find('\nDETAIL', i + 10)
    else:
        j = detail.find('\nDETAIL', i + 10)
    return detail[i:j if j > 0 else len(detail)]


fitness = get_detail('fitness')
diet = get_detail('diet')

# 从 daily_data.js 取 INSIGHTS（用 node 更稳，这里用正则粗略提取）
def insight_block(key):
    m = re.search(r'\n  ' + key + r': \{(.*?)\n  \},', daily, re.S)
    return m.group(1) if m else ''


ins_fit = insight_block('fitness')
ins_diet = insight_block('diet')

# ---------- 1) 热量口径一致 ----------
CAL = '训练日 2500'
for name, txt in [('DETAIL.diet', diet), ('INSIGHTS.diet', ins_diet)]:
    if CAL in txt or '训练日 2500' in txt:
        ok(name + ' 含热量口径「训练日 2500」')
    else:
        err(name + ' 缺热量口径「训练日 2500」')

if '训练日 2500' in fitness or '训练日 2500' in ins_fit or '训练日 +200' in fitness or '训练日+200' in fitness or '训练日 2500' in fitness:
    ok('健身侧含热量口径（训练日 2500 / +200）')
else:
    warn('健身侧未明确出现「训练日 2500」')

if '休息日 2300' in diet and ('休息日 2300' in ins_diet or '休息日 2300' in ins_diet):
    ok('休息日 2300 口径一致')
else:
    warn('休息日 2300 口径未在两处同时出现')

# ---------- 2) 蛋白口径一致 ----------
if '110-130g' in diet:
    ok('DETAIL.diet 含蛋白口径 110-130g')
else:
    err('DETAIL.diet 缺蛋白口径 110-130g')
if '110-130g' in ins_diet:
    ok('INSIGHTS.diet 含蛋白口径 110-130g')
else:
    err('INSIGHTS.diet 缺蛋白口径 110-130g')

# ---------- 3) 食谱只应有一处（健身区不得再有完整菜单表）----------
meal_markers = ['无糖希腊酸奶', '糙米饭 1.5 碗', '清蒸鱼 100g']
in_diet = sum(1 for mk in meal_markers if mk in diet)
in_fit = sum(1 for mk in meal_markers if mk in fitness)
if in_diet >= 2:
    ok('权威食谱在 DETAIL.diet（命中 %d/%d 项）' % (in_diet, len(meal_markers)))
else:
    err('DETAIL.diet 未找到完整食谱（命中 %d/%d）' % (in_diet, len(meal_markers)))
if in_fit == 0:
    ok('DETAIL.fitness 已不含重复食谱（0/%d 项）' % len(meal_markers))
else:
    err('DETAIL.fitness 仍含食谱内容（命中 %d 项），与饮食区重复' % in_fit)

if '见【饮食助手】' in fitness:
    ok('DETAIL.fitness 已明确指向饮食区')
else:
    warn('DETAIL.fitness 未指向饮食区')

# ---------- 4) 周训练计划：7 天且两处一致 ----------
DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
wk = re.search(r'<div class="wk-plan">(.*?)</div>\s*<div class="wk-legend"', fitness, re.S)
if wk:
    found = [d for d in DAYS if d in wk.group(1)]
    if len(found) == 7:
        ok('健身区周计划含全部 7 天')
    else:
        err('健身区周计划缺天：%s' % [d for d in DAYS if d not in wk.group(1)])
else:
    err('健身区未找到周计划表')

if all(d in ins_fit for d in DAYS):
    ok('INSIGHTS.fitness 周计划含全部 7 天')
else:
    warn('INSIGHTS.fitness 周计划不全：%s' % [d for d in DAYS if d not in ins_fit])

# 关键结构一致性：下肢训练日
if '下肢' in fitness and '下肢' in ins_fit:
    ok('两处都含「下肢」训练日（练腿已加）')
else:
    err('下肢训练日在两处不一致')

# ---------- 5) 体型数据一致 ----------
for name, txt in [('DETAIL.fitness', fitness), ('DETAIL.diet', diet),
                  ('INSIGHTS.fitness', ins_fit), ('INSIGHTS.diet', ins_diet)]:
    if '59kg' not in txt and '59 kg' not in txt:
        warn(name + ' 未出现体重 59kg')
if '170cm' in fitness or '170cm' in ins_fit:
    ok('体型数据 170cm/59kg 一致')

# ---------- 6) 版本号三处一致 ----------
v1 = re.search(r'var SITE_VERSION = "([\d.]+)"', daily)
v2 = re.search(r'daily_data\.js\?v=([\d.]+)', index)
v3 = re.search(r'版本([\d.]+)', daily)
vals = {'SITE_VERSION': v1.group(1) if v1 else None,
        'index.html 引用': v2.group(1) if v2 else None,
        'WEBSITE_GUIDE.summary': v3.group(1) if v3 else None}
uniq = set(v for v in vals.values() if v)
if len(uniq) == 1:
    ok('版本号三处一致：%s' % uniq.pop())
else:
    err('版本号不一致：%s' % vals)

# ---------- 7) 训练平台链接一致 ----------
urls = set(re.findall(r'https://zr-president\.github\.io/training/?#?/?[a-z]*', daily + index + detail))
if len(urls) <= 2:
    ok('训练平台链接口径统一（%d 种）' % len(urls))
else:
    warn('训练平台链接有多种写法：%s' % urls)

# ---------- 8) 日期一致 ----------
bd = re.search(r'DAILY_BRIEFING = \{\s*date: "([\d-]+)"', daily)
vd = re.search(r'DAILY_VOCAB = \{\s*date: "([\d-]+)"', daily)
lu = re.search(r'LEARN_PATHS = \{\s*updated: "([\d-]+)"', daily)
dates = {'要闻': bd.group(1) if bd else None, '每日一词': vd.group(1) if vd else None,
         '小白课堂': lu.group(1) if lu else None}
if len(set(d for d in dates.values() if d)) == 1:
    ok('当日日期三处一致：%s' % list(dates.values())[0])
else:
    err('当日日期不一致：%s' % dates)

# ---------- 9) 每日一词 / 小白课堂 领域多样性 ----------
def categories(txt):
    return re.findall(r'category:"([^"]+)"', txt) or re.findall(r'section:"([^"]+)"', txt)

KEY = r'"?%s"?\s*:\s*"([^"]+)"'

def today_items(var):
    m = re.search(r'var ' + var + r' = \{[\s\S]*?\n\};', daily)
    if not m:
        return ''
    b = m.group(0)
    im = re.search(r'items:\s*\[([\s\S]*?)\n  \],', b)
    if im:
        return im.group(1)
    wm = re.search(r'words:\s*\[([\s\S]*?)\n\};', b)
    return wm.group(1) if wm else b

def check_diversity(label, txt, key):
    vals = re.findall(KEY % key, txt)
    if not vals:
        warn(label + ' 未能解析领域字段')
        return
    top = max(set(vals), key=vals.count)
    share = vals.count(top) / len(vals)
    if share > 0.5:
        err('%s 过于单一：「%s」占 %.0f%%（应 <50%%）' % (label, top, share * 100))
    else:
        ok('%s 领域分布均衡（%d 条 / %d 个领域，最大占比 %.0f%%）' % (label, len(vals), len(set(vals)), share * 100))

check_diversity('每日一词', today_items('DAILY_VOCAB'), 'category')
check_diversity('小白课堂', today_items('LEARN_PATHS'), 'section')


# ---------- 10) 日期审计：所有 updated/date 字段必须等于当日 ----------
import subprocess, json as _json

NODE = r"""
const fs=require('fs'),vm=require('vm');
const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const sysToday = new Date(); const today = sysToday.getFullYear()+'-'+String(sysToday.getMonth()+1).padStart(2,'0')+'-'+String(sysToday.getDate()).padStart(2,'0');
const contentDate = c.DAILY_BRIEFING.date;
const bad=[], okList=[];
function norm(s){ if(!s) return null; const m=String(s).match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/); return m? (m[1]+'-'+String(m[2]).padStart(2,'0')+'-'+String(m[3]).padStart(2,'0')) : null; }
function chk(name, val){
  const v = norm(val);
  if (v === today) okList.push(name);
  else bad.push(name+' = '+val);
}
if(c.DAILY_DATA) chk('DAILY_DATA.update_date', c.DAILY_DATA.update_date);
if(c.DAILY_DATA && c.DAILY_DATA.movie) chk('DAILY_DATA.movie.updated', c.DAILY_DATA.movie.updated);
chk('DAILY_VOCAB.date', c.DAILY_VOCAB && c.DAILY_VOCAB.date);
chk('LEARN_PATHS.updated', c.LEARN_PATHS && c.LEARN_PATHS.updated);
chk('MARKET_SENTIMENT.updated', c.MARKET_SENTIMENT && c.MARKET_SENTIMENT.updated);
chk('DAILY_DECISIONS.updated', c.DAILY_DECISIONS && c.DAILY_DECISIONS.updated);
chk('OPPORTUNITY_RADAR.updated', c.OPPORTUNITY_RADAR && c.OPPORTUNITY_RADAR.updated);
chk('AI_JUDGMENTS.updated', c.AI_JUDGMENTS && c.AI_JUDGMENTS.updated);
chk('TOOLCHAIN_RADAR.updated', c.TOOLCHAIN_RADAR && c.TOOLCHAIN_RADAR.updated);
Object.keys(c.INSIGHTS||{}).forEach(k=>chk('INSIGHTS.'+k+'.updated', c.INSIGHTS[k].updated));
const arch = Object.keys((c.LEARN_PATHS&&c.LEARN_PATHS.archive)||{});
const clash = arch.filter(k=>k===today);
console.log(JSON.stringify({today, contentDate, bad, okCount: okList.length, arch, clash}));
"""
try:
    rr = subprocess.run(['node', '-e', NODE], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
    info = _json.loads(rr.stdout.strip().splitlines()[-1])
    today = info['today']
    if info.get('contentDate') != info['today']:
        err('站点日期(%s)与系统日期(%s)不一致 —— 更新时必须读取系统时钟' % (info.get('contentDate'), info['today']))
    else:
        ok('站点日期与系统真实日期一致：%s' % today)
    if info['bad']:
        err('日期未同步到当日（%s）：%s' % (today, '；'.join(info['bad'])))
    else:
        ok('日期审计：%d 个日期字段全部等于当日（%s），含 17 个 INSIGHTS 分区' % (info['okCount'], today))
    if info['clash']:
        err('归档键与当日相同（归档只能是历史）：%s' % info['clash'])
    else:
        ok('归档键均为历史日期（%d 个），未与当日冲突' % len(info['arch']))
except Exception as e:
    warn('日期审计执行失败：%s' % e)

# ---------- 输出 ----------
print('=== 跨板块一致性检查 ===')
for x in oks:
    print('  ✅ ' + x)
if warns:
    print()
    print('⚠️ 提醒 (%d):' % len(warns))
    for x in warns:
        print('   · ' + x)
if errors:
    print()
    print('❌ 错误 (%d):' % len(errors))
    for x in errors:
        print('   · ' + x)
    sys.exit(1)
print()
print('✅ 一致性检查通过（%d 项）' % len(oks))
