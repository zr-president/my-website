#!/usr/bin/env python3
"""Apply #35 and #38a to index.html — encoding-safe approach"""
import sys, io, os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INDEX = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')

with open(INDEX, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = 0

# === #35: Hot tags after insight callout ===
# Find line containing: callout info + ins.trend + ins.tip
insight_idx = None
for i, line in enumerate(lines):
    if 'class=\\"callout info\\"' in line and 'ins.trend' in line and 'ins.tip' in line:
        insight_idx = i
        break

if insight_idx is not None:
    print(f'#35: Found insight callout at line {insight_idx+1}')
    # Insert hot tags code AFTER this line, BEFORE the "// Layered reasoning" line
    # The hot tags code to insert:
    hot_tags_lines = [
        '      // #35: Hot tags extracted from trend text (**keyword**)\n',
        "      var trendText = ins.trend || '';\n",
        '      var hotTagMatches = trendText.match(/\\*\\*(.+?)\\*\\*/g);\n',
        '      if(hotTagMatches && hotTagMatches.length > 0){\n',
        "        detailHtml += '<div style=\"margin-top:6px;font-size:10px;color:var(--text3)\">"
        + "\u{1f525} \u4eca\u65e5\u70ed\u641c: ';\n",
        '        var seenKw = {};\n',
        '        hotTagMatches.forEach(function(tm){\n',
        '          var kw = tm.replace(/\\*\\*/g, "");\n',
        '          if(!seenKw[kw]){\n',
        '            seenKw[kw] = true;\n',
        "            detailHtml += '<span style=\"display:inline-block;margin:2px 3px;padding:2px 8px;background:var(--bg2);border:1px solid var(--border);border-radius:10px;cursor:pointer;font-size:10px;color:var(--text2)\" onclick=\"event.stopPropagation();window.open(\\'https://www.bing.com/search?q='+encodeURIComponent(kw)+'\\',\\'_blank\\')\" title=\"\u641c\u7d22: '+kw+'\">\u{1f50d} '+kw+'</span>';\n",
        '          }\n',
        '        });\n',
        "        detailHtml += '</div>';\n",
        '      }\n',
    ]
    # Insert after insight_idx
    for j, hl in enumerate(hot_tags_lines):
        lines.insert(insight_idx + 1 + j, hl)
    changes += 1
    print('#35: Hot tags inserted')
else:
    print('#35: Anchor line not found')

# === #38a: Featured card after dailyBanner, before dailyBriefing ===
# Find the line that closes dailyBanner div and the dailyBriefing comment line
banner_end_idx = None
briefing_start_idx = None
for i, line in enumerate(lines):
    if banner_end_idx is None and line.strip() == '</div></div>' and i > 100 and i < 300:
        # Verify previous line has dailyBanner context
        if i > 0 and 'checkUpdateStatus' in lines[i-1]:
            banner_end_idx = i
    if briefing_start_idx is None and 'Daily Briefing' in line and 'safe: event delegation' in line:
        briefing_start_idx = i

print(f'#38a: banner_end={banner_end_idx}, briefing_start={briefing_start_idx}')

if banner_end_idx is not None and briefing_start_idx is not None:
    # Insert featured card HTML between banner_end and briefing_start
    # We'll insert after banner_end_idx + 1 (the blank line after </div></div>)
    insert_at = banner_end_idx + 2  # after the blank line
    featured_card_lines = [
        '\n',
        '\t<!-- #38: \u4eca\u65e5\u5fc5\u770b\u7f6e\u9876\u805a\u5408\u5361\u7247 -->\n',
        '\t<div id="featuredCard" style="background:linear-gradient(135deg,#fef3c7,#fef9c3);border:1px solid #f59e0b;border-radius:12px;padding:12px 16px;margin-bottom:16px;display:none;cursor:pointer;transition:transform .15s,box-shadow .15s" onmouseover="this.style.transform=\'translateY(-1px)\';this.style.boxShadow=\'0 4px 12px rgba(245,158,11,.25)\'" onmouseout="this.style.transform=\'\';this.style.boxShadow=\'\'" onclick="openFeaturedCard()">\n',
        '\t<div style="display:flex;align-items:center;gap:10px">\n',
        '\t<span style="font-size:22px;flex-shrink:0">\u{1f4cc}</span>\n',
        '\t<div style="flex:1;min-width:0">\n',
        '\t<div style="font-size:10px;color:#d97706;font-weight:700;text-transform:uppercase;letter-spacing:1px">\u4eca\u65e5\u5fc5\u770b \u00b7 TOP STORY</div>\n',
        '\t<div id="featuredHeadline" style="font-size:14px;font-weight:700;color:#1c1917;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></div>\n',
        '\t<div id="featuredSummary" style="font-size:11px;color:#78716c;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"></div>\n',
        '\t</div>\n',
        '\t<span style="font-size:16px;color:#d97706;flex-shrink:0">\u2192</span>\n',
        '\t</div>\n',
        '\t</div>\n',
        '\n',
    ]
    for j, fl in enumerate(featured_card_lines):
        lines.insert(insert_at + j, fl)
    changes += 1
    print('#38a: Featured card inserted')
else:
    print('#38a: Anchors not found')

# Save
with open(INDEX, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print(f'\nDone. {changes} changes applied.')
