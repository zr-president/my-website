#!/usr/bin/env python3
"""Apply remaining optimizations #35, #38 to index.html"""
import sys, io, os, re, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = ROOT + r'\index.html'

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ═══════════════════════════════════════════════════
# #35: INSIGHTS section-detail — extract hot tags from trend text
# ═══════════════════════════════════════════════════
# Anchor: after the insight callout line with ins.trend, before "// Layered reasoning"
old_35 = """      detailHtml += '<div class=\"callout info\" style=\"margin-bottom:16px\"><strong>📊 今日分析（'+ins.updated+'更新）</strong><br>'+ins.summary+'<br><span style=\"font-size:12px;color:var(--text2)\">'+ins.trend+'</span><br><strong style=\"color:var(--accent)\">'+ins.tip+'</strong></div>';
      // Layered reasoning"""

new_35 = """      detailHtml += '<div class=\"callout info\" style=\"margin-bottom:16px\"><strong>📊 今日分析（'+ins.updated+'更新）</strong><br>'+ins.summary+'<br><span style=\"font-size:12px;color:var(--text2)\">'+ins.trend+'</span><br><strong style=\"color:var(--accent)\">'+ins.tip+'</strong></div>';
      // #35: Hot tags extracted from trend text (**keyword**)
      var trendText = ins.trend || '';
      var hotTagMatches = trendText.match(/\*\*(.+?)\*\*/g);
      if(hotTagMatches && hotTagMatches.length > 0){
        detailHtml += '<div style=\"margin-top:6px;font-size:10px;color:var(--text3)\">🔥 今日热搜: ';
        var seenKw = {};
        hotTagMatches.forEach(function(tm){
          var kw = tm.replace(/\*\*/g, '');
          if(!seenKw[kw]){
            seenKw[kw] = true;
            detailHtml += '<span style=\"display:inline-block;margin:2px 3px;padding:2px 8px;background:var(--bg2);border:1px solid var(--border);border-radius:10px;cursor:pointer;font-size:10px;color:var(--text2)\" onclick=\"event.stopPropagation();window.open(\'https://www.bing.com/search?q='+encodeURIComponent(kw)+'\',\'_blank\')\" title=\"搜索: '+kw+'\">🔍 '+kw+'</span>';
          }
        });
        detailHtml += '</div>';
      }
      // Layered reasoning"""

if old_35 in content:
    content = content.replace(old_35, new_35, 1)
    changes += 1
    print('✓ #35: Hot tags extraction added to INSIGHTS section-detail')
else:
    print('✗ #35: Anchor not found — checking...')
    # Debug: show surrounding context
    idx = content.find('ins.trend')
    if idx > 0:
        print('  Found ins.trend at pos', idx, ':')
        print('  ', repr(content[idx-20:idx+200]))
    else:
        print('  ins.trend not found in file at all')

# ═══════════════════════════════════════════════════
# #38: Dashboard 今日必看 featured card
# ═══════════════════════════════════════════════════
# 38a: Insert the card HTML after dailyBanner, before dailyBriefing
old_38a = """</div></div>

	<!-- Daily Briefing (safe: event delegation, no inline onclick) -->
	<div id="dailyBriefing" style="margin-bottom:16px;display:none">"""

new_38a = """</div></div>

	<!-- #38: 今日必看置顶聚合卡片 -->
	<div id="featuredCard" style="background:linear-gradient(135deg,#fef3c7,#fef9c3);border:1px solid #f59e0b;border-radius:12px;padding:12px 16px;margin-bottom:16px;display:none;cursor:pointer;transition:transform .15s,box-shadow .15s" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 4px 12px rgba(245,158,11,.25)'" onmouseout="this.style.transform='';this.style.boxShadow=''" onclick="openFeaturedCard()">
	<div style="display:flex;align-items:center;gap:10px">
	<span style="font-size:22px;flex-shrink:0">📌</span>
	<div style="flex:1;min-width:0">
	<div style="font-size:10px;color:#d97706;font-weight:700;text-transform:uppercase;letter-spacing:1px">今日必看 · TOP STORY</div>
	<div id="featuredHeadline" style="font-size:14px;font-weight:700;color:#1c1917;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></div>
	<div id="featuredSummary" style="font-size:11px;color:#78716c;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"></div>
	</div>
	<span style="font-size:16px;color:#d97706;flex-shrink:0">→</span>
	</div>
	</div>

	<!-- Daily Briefing (safe: event delegation, no inline onclick) -->
	<div id="dailyBriefing" style="margin-bottom:16px;display:none">"""

if old_38a in content:
    content = content.replace(old_38a, new_38a, 1)
    changes += 1
    print('✓ #38a: Featured card HTML inserted')
else:
    print('✗ #38a: Anchor not found')

# 38b: Add populateFeaturedCard() call in renderBriefing function
# And add the openFeaturedCard() and populateFeaturedCard() functions
old_38b = """  content.innerHTML = h;
  container.style.display = 'block';
}"""

new_38b = """  content.innerHTML = h;
  container.style.display = 'block';
  // #38: Populate featured card from top briefing
  populateFeaturedCard();
}

// #38: Populate the 今日必看 featured card
function populateFeaturedCard(){
  var card = document.getElementById('featuredCard');
  if(!card || typeof DAILY_BRIEFING==='undefined') return;
  var top = DAILY_BRIEFING.highlights.slice().sort(function(a,b){return a.priority-b.priority;})[0];
  if(!top) return;
  var hl = document.getElementById('featuredHeadline');
  var sm = document.getElementById('featuredSummary');
  if(hl) hl.textContent = top.icon + ' ' + top.headline;
  if(sm) sm.textContent = top.summary;
  card.setAttribute('data-link', top.link || '');
  card.setAttribute('data-deep', top.deepLink || '');
  card.style.display = 'block';
}

// #38: Navigate from featured card
function openFeaturedCard(){
  var card = document.getElementById('featuredCard');
  if(!card) return;
  var deepLink = card.getAttribute('data-deep');
  if(deepLink){
    window.open(deepLink, '_blank');
  } else {
    var link = card.getAttribute('data-link');
    if(link && typeof navigateTo === 'function') navigateTo('section-detail', link.replace('#',''));
  }
}"""

if old_38b in content:
    content = content.replace(old_38b, new_38b, 1)
    changes += 1
    print('✓ #38b: populateFeaturedCard + openFeaturedCard functions added')
else:
    print('✗ #38b: Anchor not found — searching...')
    idx = content.find("container.style.display = 'block';")
    if idx > 0:
        print('  Found at pos', idx, ':', repr(content[idx:idx+60]))
    else:
        print('  String not found')

# ═══════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════
if changes > 0:
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'\n✓ {changes} changes applied, file saved')
else:
    print('\n⚠ No changes applied')
