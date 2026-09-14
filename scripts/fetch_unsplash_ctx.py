# -*- coding: utf-8 -*-
"""下载全部 Unsplash 图 + 提取每张图的上下文（它出现在哪个板块/卡片），
   供多模态复核「这张图配得对不对」
"""
import io, sys, os, re, ssl, json, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
OUT = os.path.join(BASE, 'scripts', '_imgcheck')
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
from PIL import Image

files = {f: open(os.path.join(BASE, f), encoding='utf-8').read() for f in
         ['index.html', 'daily_data.js', 'detail_content.js']}

urls = set()
for t in files.values():
    for m in re.finditer(r'https://images\.unsplash\.com/[^\s"\'\\<>()]+', t):
        urls.add(m.group(0).rstrip('.,);\'"'))

print('=== Unsplash 图片上下文 ===')
ctxmap = {}
for u in sorted(urls):
    # 找它出现的位置及其前后文（用来判断"应该是什么图"）
    where = []
    for f, t in files.items():
        for m in re.finditer(re.escape(u), t):
            seg = t[max(0, m.start() - 320): m.start() + 160]
            # 抽取同段的 title/alt/desc 关键信息
            labels = re.findall(r'(?:title|alt|desc|word|name)[:=]"([^"]{2,40})"', seg)
            section = ''
            for key in ['fashion', 'beer', 'movie', 'travel', 'novel', 'anime', 'car', 'diet', 'gaming']:
                if key in seg.lower():
                    section = key; break
            where.append((f, section, labels[:3]))
    ctxmap[u] = where
    print('  %s' % u[:84])
    for f, sec, labels in where[:2]:
        print('     出现在 %s | 疑似板块=%s | 邻近文本=%s' % (f, sec or '?', labels))

print()
print('=== 下载并检查 ===')
rep = []
for u in sorted(urls):
    name = re.sub(r'[^0-9a-zA-Z]+', '_', u.split('photo-')[-1].split('?')[0])[:30] + '.jpg'
    p = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            d = r.read()
        open(p, 'wb').write(d)
        im = Image.open(p); im.load()
        rep.append({'url': u, 'file': p, 'kb': round(len(d) / 1024, 1), 'size': im.size,
                    'context': ctxmap[u]})
        print('  ✅ %-34s %sx%s %6.1fKB' % (name, im.size[0], im.size[1], len(d) / 1024))
    except Exception as e:
        print('  ❌ %-34s %s' % (name, str(e)[:60]))

json.dump(rep, open(os.path.join(BASE, 'scripts', '_imgcheck_manifest.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('已下载 %d 张到 scripts/_imgcheck/（临时目录，复核后删除）' % len(rep))
