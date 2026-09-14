# -*- coding: utf-8 -*-
"""完整图片审计 v2：不依赖文件扩展名，抽取所有 <img src> 与 CSS url()
   （上一版因为正则要求扩展名，漏掉了 Unsplash 的免扩展名 URL）
"""
import io, sys, os, re, ssl, json, urllib.request, concurrent.futures
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

FILES = ['index.html', 'daily_data.js', 'detail_content.js']
found = {}   # url -> set(files)

RE_IMG_SRC = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.I)
RE_CSS_URL = re.compile(r'url\(["\']?(https?://[^)"\']+)["\']?\)', re.I)
RE_ANY_HTTP_IMG = re.compile(r'https?://[^\s"\'\\<>()]+', re.I)

for f in FILES:
    p = os.path.join(BASE, f)
    t = open(p, encoding='utf-8').read()
    for m in RE_IMG_SRC.finditer(t):
        u = m.group(1)
        if u.startswith('http'):
            found.setdefault(u, set()).add(f)
    for m in RE_CSS_URL.finditer(t):
        found.setdefault(m.group(1), set()).add(f)
    # 兜底：任何 http URL（含无扩展名），但排除明显非图片的站点链接
    for m in RE_ANY_HTTP_IMG.finditer(t):
        u = m.group(0).rstrip('.,);\'"')
        if re.search(r'\.(jpg|jpeg|png|webp|gif|avif)(\?|$)', u, re.I) or 'unsplash' in u or '/image/' in u or 'img' in u.lower():
            if not re.search(r'(taobao|bilibili|youtube|tmdb\.org/t/p/[^/]+$|dongchedi|boohee|myfitnesspal|xiachufang|github\.io|qq\.com|163\.com|sina|zhihu|weibo)', u):
                found.setdefault(u, set()).add(f)

print('=== 完整图片清单（按来源）===')
print('  总数：%d' % len(found))
from collections import Counter
dom = Counter(re.sub(r'^https?://([^/]+).*', r'\1', u) for u in found)
for d, n in dom.most_common():
    print('   %-30s %d' % (d, n))
print()


def check(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/*,*/*'})
        with urllib.request.urlopen(req, timeout=18, context=ctx) as r:
            data = r.read(600000)
            return u, r.status, r.headers.get('Content-Type', ''), len(data)
    except Exception as e:
        code = getattr(e, 'code', 0)
        return u, code, type(e).__name__, 0


res = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for u, st, ct, size in ex.map(check, list(found)):
        res.append((u, st, ct, size))

ok = [r for r in res if r[1] == 200 and r[2].startswith('image')]
bad = [r for r in res if not (r[1] == 200 and r[2].startswith('image'))]
print('=== HTTP 检查 ===')
print('  ✅ 正常 %d 张' % len(ok))
print('  ❌ 异常 %d 张' % len(bad))
for u, st, ct, size in bad:
    print('     [%s %s] %s' % (st or 'ERR', ct[:16], u[:92]))
print()
print('=== 正常图片（供视觉复核）===')
for u, st, ct, size in sorted(ok, key=lambda x: -x[3]):
    print('  %7.0fKB  %s' % (size / 1024, u[:96]))

json.dump([{'url': u, 'status': st, 'ctype': ct, 'bytes': size, 'files': sorted(found[u])}
           for u, st, ct, size in res],
          open(os.path.join(BASE, 'scripts', '_image_manifest.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('清单已更新：scripts/_image_manifest.json')
