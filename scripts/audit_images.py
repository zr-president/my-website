# -*- coding: utf-8 -*-
"""全站图片体检：抽取所有外部图片 URL → 逐个 HTTP 检查 → 汇总可修复清单
   （这是多模态工作流的第一步：先知道"有哪些图"，才谈得上"图对不对"）
"""
import io, sys, os, re, json, urllib.request, urllib.error, ssl, concurrent.futures
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

FILES = ['index.html', 'daily_data.js', 'detail_content.js']
IMG_RE = re.compile(r'https?://[^\s"\'\\<>()]+?\.(?:jpg|jpeg|png|webp|gif|avif)', re.I)

urls = {}
for f in FILES:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        continue
    t = open(p, encoding='utf-8').read()
    for m in IMG_RE.finditer(t):
        u = m.group(0).rstrip('.,);')
        urls.setdefault(u, set()).add(f)

print('=== 全站外部图片 URL ===')
print('  总数：%d' % len(urls))
from collections import Counter
dom = Counter(re.sub(r'^https?://([^/]+).*', r'\1', u) for u in urls)
for d, n in dom.most_common():
    print('   %-34s %d' % (d, n))
print()


def check(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = r.read(400000)
            return u, r.status, r.headers.get('Content-Type', ''), len(data)
    except urllib.error.HTTPError as e:
        return u, e.code, 'HTTPError', 0
    except Exception as e:
        return u, 0, type(e).__name__, 0


print('=== 逐个 HTTP 检查（并发）===')
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    for u, st, ct, size in ex.map(check, list(urls)):
        results.append((u, st, ct, size))

ok = [r for r in results if r[1] == 200 and r[2].startswith('image')]
bad = [r for r in results if not (r[1] == 200 and r[2].startswith('image'))]

print('  ✅ 正常：%d' % len(ok))
print('  ❌ 异常：%d' % len(bad))
print()
if bad:
    print('=== 异常清单（需修复）===')
    for u, st, ct, size in sorted(bad, key=lambda x: x[1]):
        src = ','.join(sorted(urls[u]))
        print('  [%s %s] %s' % (st or 'ERR', ct[:18], u[:96]))
        print('        出现在：%s' % src)

print()
print('=== 正常图片明细（供多模态复核"图对不对"）===')
for u, st, ct, size in sorted(ok, key=lambda x: -x[3])[:40]:
    print('  %6.0fKB  %s' % (size / 1024, u[:100]))

# 导出清单供后续多模态复核
out = os.path.join(BASE, 'scripts', '_image_manifest.json')
json.dump([{'url': u, 'status': st, 'ctype': ct, 'bytes': size,
            'files': sorted(urls[u])} for u, st, ct, size in results],
          open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print()
print('清单已导出：scripts/_image_manifest.json')
