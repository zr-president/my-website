# -*- coding: utf-8 -*-
"""个人网站前端结构与性能审计（静态分析 + 数据可用性）"""
import io, sys, re, os, json
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'

h = open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()
size = len(h.encode('utf-8'))

print('=== A. index.html 体积构成 ===')
css = sum(len(m) for m in re.findall(r'<style[^>]*>([\s\S]*?)</style>', h))
js = sum(len(m) for m in re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>', h))
print('  文件: %.1f KB (UTF-8)' % (size / 1024))
print('  内联 <style>: %.1f KB (%.1f%%)  块数 %d' % (css / 1024, css / len(h) * 100, len(re.findall(r'<style', h))))
print('  内联 <script>: %.1f KB (%.1f%%)  块数 %d' % (js / 1024, js / len(h) * 100, len(re.findall(r'<script(?![^>]*src=)', h))))
print('  纯 HTML:       %.1f KB (%.1f%%)' % ((len(h) - css - js) / 1024, (len(h) - css - js) / len(h) * 100))

print()
print('=== B. 结构质量 ===')
ids = re.findall(r'''\bid=["']([^"']+)["']''', h)
dup = {k: v for k, v in Counter(ids).items() if v > 1}
print('  id 总数 %d（去重 %d）· 重复 %d %s' % (len(ids), len(set(ids)), len(dup), list(dup.items())[:4]))
print('  标题层级: h1×%d  h2×%d  h3×%d' % (
    len(re.findall(r'<h1[ >]', h)), len(re.findall(r'<h2[ >]', h)), len(re.findall(r'<h3[ >]', h))))
imgs = re.findall(r'<img[^>]*>', h)
print('  静态 <img>: %d · 缺 alt: %d · 有 loading: %d' % (
    len(imgs), len([m for m in imgs if 'alt=' not in m]), len([m for m in imgs if 'loading=' in m])))
print('  ARIA: aria-label×%d  role×%d' % (len(re.findall(r'aria-label', h)), len(re.findall(r'\brole=', h))))
print('  SEO: description=%s  og:title=%s  og:image=%s  canonical=%s  viewport=%s' % (
    'meta name="description"' in h or "name='description'" in h,
    'og:title' in h, 'og:image' in h, 'rel="canonical"' in h, 'name="viewport"' in h))

print()
print('=== C. 外部依赖 ===')
ext = set(re.findall(r'https?://([a-zA-Z0-9.\-]+)', h))
own = {'zr-president.github.io'}
print('  外部域名 %d 个:' % len([e for e in ext if e not in own]))
for e in sorted(ext):
    if e not in own:
        print('    - ' + e)
print('  umami 占位 ID 未替换: %s' % ('REPLACE_WITH_YOUR_UMAMI_SITE_ID' in h))

print()
print('=== D. 脚本体积与加载时机 ===')
files = ['daily_data.js', 'detail_content.js', 'knowledge_index.js', 'img_style.js', 'personal_config.js']
total = 0
for f in files:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        kb = os.path.getsize(p) / 1024
        total += kb
        # 是否 defer/async
        m = re.search(r'<script([^>]*)\ssrc="' + re.escape(f), h)
        mode = 'blocking'
        if m:
            if 'defer' in m.group(1): mode = 'defer'
            elif 'async' in m.group(1): mode = 'async'
        print('  %-20s %7.1f KB  %s' % (f, kb, mode))
print('  脚本合计: %.1f KB' % total)

print()
print('=== E. 数据文件的内容构成（哪些首屏用不到）===')
d = open(os.path.join(BASE, 'daily_data.js'), encoding='utf-8').read()
var_sizes = []
for m in re.finditer(r'var\s+([A-Z_][A-Z0-9_]*)\s*=', d):
    start = m.end()
    nxt = re.search(r'\nvar\s+[A-Z_][A-Z0-9_]*\s*=', d[start:])
    end = start + (nxt.start() if nxt else len(d) - start)
    var_sizes.append((m.group(1), end - start))
var_sizes.sort(key=lambda x: -x[1])
print('  daily_data.js 各顶层变量（前 12）:')
for name, sz in var_sizes[:12]:
    print('    %-26s %7.1f KB' % (name, sz / 1024))
print('  变量数: %d' % len(var_sizes))

k = open(os.path.join(BASE, 'knowledge_index.js'), encoding='utf-8').read()
print()
print('  knowledge_index.js: %.1f KB' % (len(k.encode('utf-8')) / 1024))
print('    是否只在搜索时使用（首屏是否必需）: 需人工确认')
km = re.search(r'var\s+([A-Z_][A-Z0-9_]*)', k)
print('    顶层变量: %s' % (km.group(1) if km else '?'))

print()
print('=== F. 图片 ===')
for dpath in ['assets/img', 'img']:
    p = os.path.join(BASE, dpath)
    if not os.path.isdir(p):
        continue
    files = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
    tot = sum(os.path.getsize(os.path.join(p, f)) for f in files)
    exts = Counter(os.path.splitext(f)[1].lower() for f in files)
    print('  %-12s %2d 个 · %6.1f KB · %s' % (dpath, len(files), tot / 1024, dict(exts)))

print()
print('=== G. 缓存与版本 ===')
vers = set(re.findall(r'\?v=([\d.]+)', h))
print('  带版本号的引用: %s' % sorted(vers))
nover = []
for m in re.finditer(r'<script([^>]*)\ssrc="([^"?]+)"', h):
    if '?v=' not in m.group(2) and m.group(2).startswith(('daily', 'detail', 'knowledge', 'img_style', 'personal')):
        nover.append(m.group(2))
print('  未带版本号的本地脚本: %s' % nover)
