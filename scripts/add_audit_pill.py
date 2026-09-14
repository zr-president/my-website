# -*- coding: utf-8 -*-
"""在首页 Hero 加两枚实时徽章：内容日期 + 更新核查状态（点击可跳到核查明细）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) Hero 徽章 ----------
old = ('<span class="zh-pill">📅 每日更新</span>\n'
       '\t\t\t<span class="zh-pill">🕘 每天 6:00 自动刷新</span>')
new = ('<span class="zh-pill" id="zhDatePill" title="站点内容日期">📅 每日更新</span>\n'
       '\t\t\t<span class="zh-pill" id="zhAuditPill" title="点击查看核查明细">🔍 核查中…</span>\n'
       '\t\t\t<span class="zh-pill">🕘 每天 6:00 自动刷新</span>')
if old in h:
    h = h.replace(old, new, 1)
    print('OK Hero 徽章已加（zhDatePill / zhAuditPill）')
else:
    print('MISS Hero 徽章锚点')

# ---------- 2) 让核查函数同时更新徽章 ----------
old2 = "  box.innerHTML=h;\n}\n"
new2 = ("  box.innerHTML=h;\n\n"
        "  /* 同步更新 Hero 徽章 */\n"
        "  var pDate=document.getElementById('zhDatePill');\n"
        "  if(pDate) pDate.textContent='📅 内容日期 '+today;\n"
        "  var pAudit=document.getElementById('zhAuditPill');\n"
        "  if(pAudit){\n"
        "    pAudit.textContent = allOk ? '✅ 今日更新已核查（'+fields.length+' 项 + '+secRows.length+' 分区）'\n"
        "                               : '❌ 更新核查异常 '+(dateBad.length+lagBad.length)+' 项';\n"
        "    pAudit.style.background = allOk ? 'rgba(16,185,129,.42)' : 'rgba(220,38,38,.45)';\n"
        "    pAudit.style.cursor = 'pointer';\n"
        "    pAudit.onclick = function(){ var s=document.getElementById('update-audit'); if(s) s.scrollIntoView({behavior:'smooth',block:'start'}); };\n"
        "  }\n"
        "}\n")
if '同步更新 Hero 徽章' not in h:
    # 只替换 zh_renderUpdateAudit 里的结尾
    i = h.find('function zh_renderUpdateAudit')
    if i > 0:
        j = h.find('\n  box.innerHTML=h;\n}\n', i)
        if j > 0:
            h = h[:j] + '\n  box.innerHTML=h;\n\n  /* 同步更新 Hero 徽章 */\n  var pDate=document.getElementById(\'zhDatePill\');\n  if(pDate) pDate.textContent=\'📅 内容日期 \'+today;\n  var pAudit=document.getElementById(\'zhAuditPill\');\n  if(pAudit){\n    pAudit.textContent = allOk ? \'✅ 今日更新已核查（\'+fields.length+\' 项 + \'+secRows.length+\' 分区）\' : \'❌ 更新核查异常 \'+(dateBad.length+lagBad.length)+\' 项\';\n    pAudit.style.background = allOk ? \'rgba(16,185,129,.42)\' : \'rgba(220,38,38,.45)\';\n    pAudit.style.cursor = \'pointer\';\n    pAudit.onclick = function(){ var s=document.getElementById(\'update-audit\'); if(s) s.scrollIntoView({behavior:\'smooth\',block:\'start\'}); };\n  }\n}\n' + h[j+len('\n  box.innerHTML=h;\n}\n'):]
            print('OK 核查函数已加徽章同步')
        else:
            print('MISS box.innerHTML 结尾')
    else:
        print('MISS 核查函数')
else:
    print('已存在徽章同步')

open(FP, 'w', encoding='utf-8').write(h)
