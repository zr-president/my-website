# -*- coding: utf-8 -*-
"""在个人网站侧边栏顶部加「能力训练平台」直达入口（含动态进度）"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- 1) 侧边栏入口（插在「首页模式」区块之后） ----------
anchor = """	</div>
</div>
<div class="sidebar-footer">"""
entry = """	</div>
</div>
<!-- 能力训练平台 · 直达入口（外链） -->
<a href="https://zr-president.github.io/training/" target="_blank" rel="noopener" id="zhTrainEntry"
   style="display:flex;align-items:center;gap:9px;margin:8px 12px 6px;padding:10px 12px;border-radius:11px;text-decoration:none;background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;box-shadow:0 4px 14px rgba(79,70,229,.28);transition:.2s">
	<span style="font-size:16px">🎓</span>
	<span style="flex:1;line-height:1.35;min-width:0">
		<span style="display:block;font-size:12.5px;font-weight:700">能力训练平台</span>
		<span style="display:block;font-size:9.5px;opacity:.88" id="zhTrainSideMeta">SQL · 数据分析 · AI 产品</span>
	</span>
	<span style="font-size:13px;opacity:.9">→</span>
</a>
<div class="sidebar-footer">"""
if anchor in h:
    h = h.replace(anchor, entry, 1)
    print('OK 侧边栏入口已插入')
else:
    print('MISS 侧边栏锚点')

# ---------- 2) 让渲染函数同步更新侧边栏进度文案 ----------
old_fn_tail = """    '<div style="font-size:9.5px;color:var(--text3);margin-top:8px">数据来自训练平台（同源 localStorage，只存本机）'+(s.updated?' · 最近 '+s.updated:'')+'</div>'+
    '</div>';
}"""
new_fn_tail = """    '<div style="font-size:9.5px;color:var(--text3);margin-top:8px">数据来自训练平台（同源 localStorage，只存本机）'+(s.updated?' · 最近 '+s.updated:'')+'</div>'+
    '</div>';
}
// 同步侧边栏入口的进度文案
function zh_updateTrainEntry(){
  var el=document.getElementById('zhTrainSideMeta');
  if(!el) return;
  var s=null;
  try{ var raw=localStorage.getItem('tp_summary_v1'); if(raw) s=JSON.parse(raw); }catch(e){}
  if(s && s.total){ el.textContent='已练 '+s.done+'/'+s.total+'（'+s.pct+'%）· 点击进入'; }
  else { el.textContent='SQL · 数据分析 · AI 产品 · 点击进入'; }
}"""
if old_fn_tail in h:
    h = h.replace(old_fn_tail, new_fn_tail, 1)
    print('OK 已加 zh_updateTrainEntry')
else:
    print('MISS 渲染函数尾部')

# ---------- 3) 注册到 onDataReady ----------
if 'zh_updateTrainEntry, checkUpdateStatus' not in h:
    h = h.replace('zh_renderTraining, checkUpdateStatus',
                  'zh_renderTraining, zh_updateTrainEntry, checkUpdateStatus', 1)
    print('OK 已注册到 onDataReady')
else:
    print('已注册')

# ---------- 4) 若训练卡渲染时也调用一次 ----------
h = h.replace("""function zh_renderTraining(){
  var box=document.getElementById('zhTrainingBox');
  if(!box) return;""",
"""function zh_renderTraining(){
  var box=document.getElementById('zhTrainingBox');
  if(!box) return;
  try{ if(typeof zh_updateTrainEntry==='function') zh_updateTrainEntry(); }catch(e){}""", 1)

open(FP, 'w', encoding='utf-8').write(h)
print('done')
