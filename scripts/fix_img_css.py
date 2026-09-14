# -*- coding: utf-8 -*-
"""修正图片卡片样式：
   ① 删除覆盖新样式的旧重复规则（L195-198）
   ② 内联 minmax(240px) → min(240px,100%) 防窄屏溢出
   ③ .img-picks 用 min() 兜底，并加移动端媒体查询
"""
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
FP = r'C:\Users\ZR\Desktop\钟锐的个人网站\index.html'
h = open(FP, 'r', encoding='utf-8').read()

# ---------- ① 删除旧的重复规则块 ----------
old_block = ('.img-card .img-body{padding:9px 11px}\n'
             '.img-card .img-title{font-size:12px;font-weight:700;margin-bottom:3px;line-height:1.4}\n'
             '.img-card .img-desc{font-size:10px;color:var(--text2);line-height:1.6}\n'
             '.img-card .img-tag{display:inline-block;margin-top:5px;padding:1px 7px;border-radius:8px;font-size:9px;font-weight:700;background:var(--accent-light);')
i = h.find(old_block)
if i > 0:
    # 该块的 img-tag 行可能还没结束，找到该行末尾
    j = h.find('\n', i + len(old_block))
    removed = h[i:j]
    h = h[:i] + h[j + 1:]
    print('① 已删除旧重复规则（%d 字符）' % len(removed))
else:
    print('① 未找到旧重复规则块（可能已处理）')

# ---------- ② 内联 240px → min(240px,100%) ----------
n = h.count('minmax(240px,1fr)')
h = h.replace('minmax(240px,1fr)', 'minmax(min(240px,100%),1fr)')
print('② 内联网格 minmax(240px) → min() 兜底：%d 处' % n)

# ---------- ③ .img-picks 用 min() + 移动端媒体查询 ----------
h = h.replace('.img-picks{display:grid;grid-template-columns:repeat(auto-fill,minmax(196px,1fr));gap:11px}',
              '.img-picks{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(196px,100%),1fr));gap:11px}')

MOBILE_CSS = '''/* ===== 图片卡片：窄屏适配（防止网格溢出 / 卡片过窄）===== */
@media(max-width:620px){
  .img-picks{grid-template-columns:repeat(auto-fill,minmax(min(150px,100%),1fr))!important;gap:9px}
  .img-card{border-radius:11px}
  .img-card .img-title{font-size:12px}
  .img-card .img-desc{font-size:10px;line-height:1.6}
  .img-picks[style]{grid-template-columns:repeat(auto-fill,minmax(min(150px,100%),1fr))!important}
}
@media(max-width:400px){
  .img-picks,.img-picks[style]{grid-template-columns:1fr!important}
}
'''
if '窄屏适配' not in h:
    anchor = '/* 竖版海报：给顶部叠一层非常淡的暗角，让标题区更稳 */'
    h = h.replace(anchor, MOBILE_CSS + anchor, 1)
    print('③ 已加移动端媒体查询')
else:
    print('③ 移动端媒体查询已存在')

open(FP, 'w', encoding='utf-8').write(h)

r = subprocess.run(['node', '-e', "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\\s\\S]*?)<\\/script>/g)].map(x=>x[1]);let bad=0;for(const s of m){try{new Function(s)}catch(e){bad++;console.log(e.message)}};console.log('index inline FAIL='+bad)"],
                   capture_output=True, text=True, encoding='utf-8', cwd=r'C:\Users\ZR\Desktop\钟锐的个人网站')
print(r.stdout.strip())

print()
print('=== 复查：图片相关规则顺序 ===')
for ln, line in enumerate(open(FP, encoding='utf-8').read().split('\n'), 1):
    if re.search(r'\.img-picks\{|\.img-card \.img-(body|title|desc|tag)\{', line):
        print('  L%-5d %s' % (ln, line.strip()[:110]))
