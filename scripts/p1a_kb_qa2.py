# -*- coding: utf-8 -*-
"""补注入：用正则定位锚点（CSS .search-box / JS // Avatar）"""
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()

CSS = '''/* ===== 知识问答面板（S03 知识卡 + S04 可核对问答）===== */
#qaPanel{display:none;margin:6px 0 10px;max-height:52vh;overflow:auto;padding-right:2px}
#qaPanel::-webkit-scrollbar{width:5px}
#qaPanel::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
.qa-hd{font-size:12px;color:var(--text3);margin:0 0 6px;line-height:1.6}
.qa-hd span{display:block;font-size:11px;opacity:.85}
.qa-card{background:var(--bg2);border-left:3px solid var(--accent);border-radius:8px;padding:8px 10px;margin-bottom:6px}
.qa-kw{font-size:12px;font-weight:700;color:var(--text);margin-bottom:3px}
.qa-info{font-size:12px;color:var(--text2);line-height:1.7}
.qa-src{font-size:11px;color:var(--text3);margin-top:5px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.qa-src a{color:var(--accent);text-decoration:none;font-weight:600;white-space:nowrap}
.qa-src a:hover{text-decoration:underline}
.qa-empty{font-size:12px;color:var(--text2);line-height:1.7;background:var(--bg2);border-left:3px solid var(--orange);border-radius:8px;padding:9px 11px}
.qa-empty span{display:block;font-size:11px;color:var(--text3);margin-top:4px}
'''

JS = r'''
/* ===== 知识问答：S03 知识卡 + S04 可核对问答 =====
   只做检索、不生成内容；每条结果必须带来源与更新时间；
   相关度不足时明确说「没有找到可靠依据」——宁可承认不知道，也不硬凑。 */
var __qaTimer = null;
function kbAsk(v){
  if(__qaTimer) clearTimeout(__qaTimer);
  __qaTimer = setTimeout(function(){ try{ kbAskNow(v); }catch(e){} }, 260);
}
function kbTokenize(q){
  var s = String(q).toLowerCase().replace(/[\s，。！？、；：""''（）\[\]{}<>《》~!@#$%^&*()_+|\\/=\-\+.,:;"'?]+/g, ' ');
  var parts = s.split(' ').filter(function(t){ return t.length >= 2; });
  if(!parts.length && String(q).trim().length >= 2) parts = [String(q).trim().toLowerCase()];
  return parts;
}
function kbScore(entry, qLower, tokens){
  var kw = String(entry.keyword||'').toLowerCase();
  var info = String(entry.info||'').toLowerCase();
  var s = 0;
  if(kw === qLower) s = 100;
  else if(qLower.indexOf(kw) >= 0 || kw.indexOf(qLower) >= 0) s = 85;
  else if(info.indexOf(qLower) >= 0) s = 70;
  else {
    var hit = 0;
    for(var i=0;i<tokens.length;i++){
      var t = tokens[i];
      if(kw.indexOf(t) >= 0) hit += 2;
      else if(info.indexOf(t) >= 0) hit += 1;
    }
    if(hit > 0) s = Math.min(60, 20 + hit * 8);
  }
  return s;
}
function kbClose(){
  var p = document.getElementById('qaPanel');
  if(p){ p.style.display = 'none'; p.innerHTML = ''; }
  var inp = document.getElementById('searchInput');
  if(inp) inp.value = '';
  document.querySelectorAll('.section').forEach(function(s){ s.classList.remove('search-none'); });
}
function kbAskNow(q){
  var panel = document.getElementById('qaPanel');
  if(!panel) return;
  q = String(q||'').trim();
  if(q.length < 2){ panel.style.display = 'none'; panel.innerHTML = ''; return; }
  panel.style.display = 'block';

  if(typeof KNOWLEDGE_INDEX === 'undefined'){
    panel.innerHTML = '<div class="qa-empty">正在加载知识索引（1573 条）…</div>';
    if(typeof ensureKnowledgeIndex === 'function'){
      ensureKnowledgeIndex(function(){ try{ kbAskNow(q); }catch(e){} });
    }
    return;
  }

  var qLower = q.toLowerCase();
  var tokens = kbTokenize(q);
  var hits = [];
  for(var i=0;i<KNOWLEDGE_INDEX.length;i++){
    var s = kbScore(KNOWLEDGE_INDEX[i], qLower, tokens);
    if(s > 0) hits.push({ s: s, e: KNOWLEDGE_INDEX[i] });
  }
  hits.sort(function(a,b){ return b.s - a.s; });

  if(!hits.length || hits[0].s < 45){
    panel.innerHTML = '<div class="qa-empty">🔍 没有找到可靠依据' +
      '<span>这个知识库里没有对得上的条目。换个说法再试；如果换几种说法都找不到，就说明它确实没有 —— 这种情况我不会编一个答案给你。</span></div>';
    return;
  }

  var per = {}, out = [];
  for(var j=0;j<hits.length && out.length<8;j++){
    var sec = hits[j].e.section;
    per[sec] = (per[sec]||0) + 1;
    if(per[sec] <= 3) out.push(hits[j]);
  }

  var html = '<div class="qa-hd">找到 ' + hits.length + ' 条相关 · 显示前 ' + out.length + ' 条' +
             '<span>点「核对原文」跳到对应分区自己看一遍</span></div>';
  for(var k=0;k<out.length;k++){
    var e = out[k].e;
    var upd = (typeof INSIGHTS !== 'undefined' && INSIGHTS[e.section] && INSIGHTS[e.section].updated) || '—';
    html += '<div class="qa-card">' +
            '<div class="qa-kw">' + escHtml(e.keyword) + '</div>' +
            '<div class="qa-info">' + escHtml(e.info) + '</div>' +
            '<div class="qa-src"><span>📚 ' + escHtml(e.section) + ' · 更新 ' + escHtml(upd) + '</span>' +
            '<a href="#' + escHtml(e.section) + '" onclick="kbClose()">核对原文 →</a></div>' +
            '</div>';
  }
  panel.innerHTML = html;
}

'''

ok_css = ok_js = False

# --- CSS ---
if '#qaPanel{' in h:
    print('ℹ️  CSS 已存在')
else:
    m = re.search(r'\.search-box\{', h)
    if m:
        h = h[:m.start()] + CSS + h[m.start():]
        ok_css = True
        print('✅ CSS 已注入（.search-box 之前）')
    else:
        print('❌ CSS 锚点仍未找到')

# --- JS ---
if 'function kbAskNow' in h:
    print('ℹ️  JS 已存在')
else:
    m = re.search(r'(?m)^[ \t]*//[ \t]*Avatar[ \t]*$', h)
    if m:
        h = h[:m.start()] + JS + h[m.start():]
        ok_js = True
        print('✅ JS 已注入（// Avatar 之前）')
    else:
        print('❌ JS 锚点仍未找到')

open(FP, 'w', encoding='utf-8').write(h)

h2 = open(FP, encoding='utf-8').read()
print()
for k in ['function kbAskNow', 'function kbScore', 'function kbTokenize', 'id="qaPanel"',
          '.qa-card{', '没有找到可靠依据', '.qa-empty{']:
    print('  含 %-22s %s' % (k, k in h2))
print('  文件 %.1f KB' % (len(h2.encode('utf-8'))/1024))
