# -*- coding: utf-8 -*-
"""P1A-① S03 知识卡 + S04 可核对问答
   把侧栏搜索从「分区过滤」升级为「跨 1573 条知识索引的带引用问答」。

   设计原则（对应培训材料「问它问题，它敢不敢给出来源」）：
   - 只做检索，不生成 —— 不会编内容
   - 每条结果都带「分区 + 该分区最后更新日期 + 核对原文」链接
   - 相关度不够时明确说「没有找到可靠依据」，而不是硬凑

   顺带补齐 V01 遗漏的小数字号（9.5/10.5/11.5/12.5px）
"""
import io, sys, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, encoding='utf-8').read()
orig = len(h)

# ============ 1) 补齐 V01 遗漏字号 ============
n_fix = 0
for a, b in [('9.5px', '11px'), ('10.5px', '12px'), ('11.5px', '12px'), ('12.5px', '13px')]:
    pat = re.compile(r'(font-size:\s*)' + re.escape(a))
    cnt = len(pat.findall(h))
    if cnt:
        h = pat.sub(lambda m: m.group(1) + b, h)
        n_fix += cnt
        print('  ✅ 补 V01：%s → %s（%d 处）' % (a, b, cnt))
print('  字号补齐合计 %d 处' % n_fix)

# ============ 2) 注入 CSS ============
CSS = '''  /* ===== 知识问答面板（S03 知识卡 + S04 可核对问答）===== */
  #qaPanel{display:none;margin:6px 0 10px;max-height:52vh;overflow:auto;padding-right:2px}
  #qaPanel::-webkit-scrollbar{width:5px}
  #qaPanel::-webkit-scrollbar-thumb{background:var(--border2);border-radius:3px}
  .qa-hd{font-size:12px;color:var(--text3);margin:0 0 6px;line-height:1.6}
  .qa-hd span{display:block;font-size:11px;opacity:.85}
  .qa-card{background:var(--bg2);border-left:3px solid var(--accent);border-radius:var(--r-sm,8px);padding:8px 10px;margin-bottom:6px}
  .qa-kw{font-size:12px;font-weight:700;color:var(--text);margin-bottom:3px}
  .qa-info{font-size:12px;color:var(--text2);line-height:1.7}
  .qa-src{font-size:11px;color:var(--text3);margin-top:5px;display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
  .qa-src a{color:var(--accent);text-decoration:none;font-weight:600;white-space:nowrap}
  .qa-src a:hover{text-decoration:underline}
  .qa-empty{font-size:12px;color:var(--text2);line-height:1.7;background:var(--bg2);border-left:3px solid var(--orange);border-radius:var(--r-sm,8px);padding:9px 11px}
  .qa-empty span{display:block;font-size:11px;color:var(--text3);margin-top:4px}

'''
if '#qaPanel{' not in h:
    anchor = '  .search-box{'
    if anchor in h:
        h = h.replace(anchor, CSS + anchor, 1)
        print('✅ QA 面板 CSS 已注入')
    else:
        print('⚠️ CSS 锚点未找到（.search-box）')
else:
    print('ℹ️  QA CSS 已存在')

# ============ 3) 注入 JS ============
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

    /* 每个分区最多 3 条，总展示 8 条，避免一个分区刷屏 */
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
if 'function kbAskNow' not in h:
    anchor_js = '  // Avatar\n'
    if anchor_js in h:
        h = h.replace(anchor_js, JS + anchor_js, 1)
        print('✅ 知识问答 JS 已注入')
    else:
        print('⚠️ JS 锚点未找到（// Avatar）')
else:
    print('ℹ️  知识问答 JS 已存在')

# ============ 4) 改输入框事件 + 加面板容器 ============
OLD_INPUT = '<div class="search-box"><input type="text" id="searchInput" placeholder="搜索板块..." oninput="doSearch(this.value)"></div>'
NEW_INPUT = ('<div class="search-box"><input type="text" id="searchInput" placeholder="问点什么…（搜板块 + 查知识库）" '
             'oninput="doSearch(this.value);kbAsk(this.value)"></div>\n'
             '<div id="qaPanel"></div>')
if OLD_INPUT in h:
    h = h.replace(OLD_INPUT, NEW_INPUT, 1)
    print('✅ 搜索框已升级（doSearch + kbAsk），并加 #qaPanel 容器')
elif 'id="qaPanel"' in h:
    print('ℹ️  输入框/面板已存在')
else:
    print('⚠️ 搜索框锚点未匹配')

open(FP, 'w', encoding='utf-8').write(h)
print()
print('index.html: %d → %d 字节' % (orig, len(h)))

# ============ 5) 校验 ============
h2 = open(FP, encoding='utf-8').read()
for k in ['function kbAskNow', 'function kbScore', 'id="qaPanel"', '.qa-card{', '没有找到可靠依据']:
    print('  含 %-22s %s' % (k, k in h2))
