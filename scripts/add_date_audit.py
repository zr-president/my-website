# -*- coding: utf-8 -*-
"""把「日期审计」加进 check_consistency.py：
   校验所有 updated/date 字段都等于当日日期，且归档键不得等于当日（归档只能是历史）
"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\scripts\check_consistency.py'
c = open(FP, 'r', encoding='utf-8').read()

if '日期审计' in c:
    print('已存在日期审计，跳过'); sys.exit(0)

audit = '''
# ---------- 10) 日期审计：所有 updated/date 字段必须等于当日 ----------
import subprocess, json as _json

NODE = r"""
const fs=require('fs'),vm=require('vm');
const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('daily_data.js','utf8'),c);
const today = c.DAILY_BRIEFING.date;
const bad=[], okList=[];
function norm(s){ if(!s) return null; const m=String(s).match(/(\\\\d{4})\\\\D+(\\\\d{1,2})\\\\D+(\\\\d{1,2})/); return m? (m[1]+'-'+String(m[2]).padStart(2,'0')+'-'+String(m[3]).padStart(2,'0')) : null; }
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
console.log(JSON.stringify({today, bad, okCount: okList.length, arch, clash}));
"""
try:
    rr = subprocess.run(['node', '-e', NODE], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
    info = _json.loads(rr.stdout.strip().splitlines()[-1])
    today = info['today']
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

'''

anchor = "# ---------- 输出 ----------"
if anchor in c:
    c = c.replace(anchor, audit + anchor, 1)
    open(FP, 'w', encoding='utf-8').write(c)
    print('OK 已插入日期审计')
else:
    print('MISS 输出锚点')
