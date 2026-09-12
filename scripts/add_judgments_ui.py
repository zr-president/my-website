# -*- coding: utf-8 -*-
"""突破一 UI：判断台账（CSS + DOM + 渲染/添加/验证函数）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) CSS ----------
css_anchor = '/* ===== 周训练计划可视化（健身区）===== */'
css_new = """/* ===== 判断台账（突破一：把信息消费转为能力资产）===== */
.jd-stats{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,var(--accent-light),var(--card));border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin-bottom:10px}
.jd-ring{position:relative;width:66px;height:66px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.jd-ring-in{position:absolute;width:50px;height:50px;border-radius:50%;background:var(--card);display:flex;align-items:center;justify-content:center;flex-direction:column}
.jd-ring-in b{font-size:15px;color:var(--accent);line-height:1}
.jd-ring-in span{font-size:8px;color:var(--text3)}
.jd-nums{display:flex;gap:14px;flex-wrap:wrap;flex:1}
.jd-num b{font-size:17px;color:var(--text);display:block;line-height:1.2}
.jd-num span{font-size:9px;color:var(--text3)}
.jd-card{background:var(--card);border:1px solid var(--border);border-left:3px solid var(--text3);border-radius:9px;padding:10px 12px;margin-bottom:7px}
.jd-card.ok{border-left-color:var(--green)}
.jd-card.bad{border-left-color:var(--red)}
.jd-card.pending{border-left-color:var(--orange)}
.jd-head{display:flex;align-items:center;gap:7px;flex-wrap:wrap;margin-bottom:4px}
.jd-topic{font-size:12px;font-weight:700;color:var(--text)}
.jd-badge{font-size:9px;font-weight:700;padding:1px 7px;border-radius:8px;white-space:nowrap}
.jd-badge.ok{background:#ecfdf5;color:#059669}
.jd-badge.bad{background:#fef2f2;color:#dc2626}
.jd-badge.pending{background:#fff7ed;color:#ea580c}
.jd-date{font-size:9px;color:var(--text3);margin-left:auto}
.jd-body{font-size:11px;color:var(--text2);line-height:1.7}
.jd-ev{font-size:10px;color:var(--accent);line-height:1.6;margin-top:3px}
.jd-actions{display:flex;gap:5px;margin-top:6px}
.jd-actions button{font-size:9px;padding:3px 9px;border-radius:8px;cursor:pointer;font-family:inherit;border:1px solid var(--border);background:var(--bg);color:var(--text2)}
.jd-actions button.y{border-color:var(--green);color:var(--green)}
.jd-actions button.n{border-color:var(--red);color:var(--red)}
.jd-form{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}
.jd-form input{grid-column:span 1;padding:6px 9px;border:1px solid var(--border);border-radius:7px;font-size:11px;font-family:inherit;background:var(--bg);color:var(--text)}
.jd-form input.full{grid-column:span 2}

""" + css_anchor
h = h.replace(css_anchor, css_new, 1)

# ---------- 2) DOM（插在 AI 行业观察 details 之前）----------
dom_anchor = '<!-- #96: AI 行业观察档案'
dom_new = """<!-- 突破一：我的 AI 判断台账（把信息消费转为能力资产） -->
<div id="zhJudgments" class="card" style="padding:13px 15px;margin-top:8px">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap">
<h3 style="font-size:13px;margin:0">⚖️ 我的 AI 判断台账</h3>
<span style="font-size:10px;color:var(--text3)">记录判断 → 事后验证 → 积累准确率（能力资产）</span>
<button onclick="zh_toggleJdForm()" style="margin-left:auto;padding:3px 10px;border:1px solid var(--accent);border-radius:9px;background:var(--accent-light);color:var(--accent);cursor:pointer;font-size:10px;font-weight:600">＋ 记一条判断</button>
</div>
<div id="zhJdForm" style="display:none;margin-bottom:10px">
<div class="jd-form">
<input type="text" id="jdTopic" class="full" placeholder="主题（如：AI Agent岗位需求）">
<input type="text" id="jdJudgment" class="full" placeholder="我的判断（要可验证，如：6个月内Agent岗位需求翻倍）">
<input type="text" id="jdVerifyDate" placeholder="验证日期（如 2027-03-12）">
<input type="text" id="jdEvidence" placeholder="当前依据/线索（可选）">
</div>
<button onclick="zh_addJudgment()" style="margin-top:6px;padding:5px 14px;background:var(--accent);color:#fff;border:none;border-radius:9px;cursor:pointer;font-size:11px;font-weight:600">保存判断</button>
</div>
<div id="zhJdStats"></div>
<div id="zhJdList"></div>
</div>

""" + dom_anchor
if dom_anchor in h:
    h = h.replace(dom_anchor, dom_new, 1)
    print('OK DOM 已插入')
else:
    print('DOM ANCHOR MISS')

# ---------- 3) JS 函数（插在 zh_renderGrowthWorkbench 之后）----------
js_anchor = 'function showView(viewName, categoryKey){'
js_new = """// ===== 判断台账（突破一）=====
function zh_toggleJdForm(){
  var f=document.getElementById('zhJdForm');
  if(f) f.style.display = f.style.display==='none' ? 'block' : 'none';
}
function zh_jdAll(){
  var built=(typeof AI_JUDGMENTS!=='undefined'&&AI_JUDGMENTS.items)?AI_JUDGMENTS.items.slice():[];
  var mine=[]; try{ mine=JSON.parse(localStorage.getItem('myJudgments')||'[]'); }catch(e){}
  mine.forEach(function(m){ m._mine=true; });
  return built.concat(mine);
}
function zh_addJudgment(){
  var t=(document.getElementById('jdTopic')||{}).value||'';
  var j=(document.getElementById('jdJudgment')||{}).value||'';
  var v=(document.getElementById('jdVerifyDate')||{}).value||'';
  var e=(document.getElementById('jdEvidence')||{}).value||'';
  if(!t.trim()||!j.trim()){ alert('请填写主题和判断'); return; }
  var mine=[]; try{ mine=JSON.parse(localStorage.getItem('myJudgments')||'[]'); }catch(e2){}
  var d=new Date();
  mine.push({date:d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'),
    topic:t.trim(), judgment:j.trim(), verifyDate:v.trim(), evidence:e.trim(), status:'待验证', result:'', _mine:true});
  localStorage.setItem('myJudgments', JSON.stringify(mine));
  document.getElementById('jdTopic').value=''; document.getElementById('jdJudgment').value='';
  document.getElementById('jdVerifyDate').value=''; document.getElementById('jdEvidence').value='';
  zh_toggleJdForm();
  zh_renderJudgments();
}
function zh_verifyJudgment(i, result){
  var mine=[]; try{ mine=JSON.parse(localStorage.getItem('myJudgments')||'[]'); }catch(e){}
  if(mine[i]){ mine[i].status='已验证'; mine[i].result=result; localStorage.setItem('myJudgments', JSON.stringify(mine)); }
  zh_renderJudgments();
}
function zh_renderJudgments(){
  var box=document.getElementById('zhJdList'), st=document.getElementById('zhJdStats');
  if(!box) return;
  var all=zh_jdAll();
  var verified=all.filter(function(j){return j.status==='已验证';});
  var correct=verified.filter(function(j){return j.result==='正确';});
  var acc=verified.length?Math.round(correct.length/verified.length*100):0;
  var pending=all.filter(function(j){return j.status!=='已验证';});
  if(st){
    var col = acc>=70?'var(--green)':acc>=50?'var(--orange)':'var(--red)';
    st.innerHTML='<div class="jd-stats">'+
      '<div class="jd-ring" style="background:conic-gradient('+col+' '+(acc*3.6)+'deg, var(--bg2) 0deg)"><div class="jd-ring-in"><b>'+acc+'%</b><span>准确率</span></div></div>'+
      '<div class="jd-nums">'+
      '<div class="jd-num"><b>'+all.length+'</b><span>累计判断</span></div>'+
      '<div class="jd-num"><b style="color:var(--green)">'+correct.length+'</b><span>已验证正确</span></div>'+
      '<div class="jd-num"><b style="color:var(--orange)">'+pending.length+'</b><span>待验证</span></div>'+
      '</div></div>';
  }
  var h='';
  function card(j, mineIdx){
    var cls = j.status==='已验证' ? (j.result==='正确'?'ok':'bad') : 'pending';
    var badge = j.status==='已验证' ? (j.result==='正确'?'<span class="jd-badge ok">✓ 已验证·正确</span>':'<span class="jd-badge bad">✗ 已验证·错误</span>') : '<span class="jd-badge pending">⏳ 待验证</span>';
    h+='<div class="jd-card '+cls+'">';
    h+='<div class="jd-head"><span class="jd-topic">'+escHtml(j.topic)+'</span>'+badge+'<span class="jd-date">'+escHtml(j.date||'')+(j.verifyDate?' → '+escHtml(j.verifyDate):'')+'</span></div>';
    h+='<div class="jd-body">📌 '+escHtml(j.judgment||'')+'</div>';
    if(j.evidence) h+='<div class="jd-ev">🔍 '+escHtml(j.evidence)+'</div>';
    if(mineIdx!==null && j.status!=='已验证'){
      h+='<div class="jd-actions"><button class="y" onclick="zh_verifyJudgment('+mineIdx+',\\'正确\\')">✓ 验证：正确</button><button class="n" onclick="zh_verifyJudgment('+mineIdx+',\\'错误\\')">✗ 验证：错误</button></div>';
    }
    h+='</div>';
  }
  if(pending.length){ h+='<div style="font-size:10px;color:var(--text3);margin:8px 0 4px;font-weight:700">⏳ 待验证（'+pending.length+'）</div>'; 
    var mi=0; var mine=[]; try{ mine=JSON.parse(localStorage.getItem('myJudgments')||'[]'); }catch(e){}
    pending.forEach(function(j){ card(j, (j._mine && j.status!=='已验证') ? mine.indexOf(j) : null); }); }
  if(verified.length){ h+='<div style="font-size:10px;color:var(--text3);margin:10px 0 4px;font-weight:700">✓ 已验证（'+verified.length+'）</div>'; verified.forEach(function(j){ card(j, null); }); }
  box.innerHTML=h;
}

function showView(viewName, categoryKey){"""
if js_anchor in h:
    h = h.replace(js_anchor, js_new, 1)
    print('OK JS 已插入')
else:
    print('JS ANCHOR MISS')

# ---------- 4) onDataReady 注册 ----------
old_task = 'zh_renderGrowth, zh_renderGrowthWorkbench, checkUpdateStatus'
if 'zh_renderJudgments, checkUpdateStatus' not in h:
    h = h.replace(old_task, 'zh_renderGrowth, zh_renderGrowthWorkbench, zh_renderJudgments, checkUpdateStatus', 1)
    print('OK onDataReady 注册')

open(FP, 'w', encoding='utf-8').write(h)
print('done')
