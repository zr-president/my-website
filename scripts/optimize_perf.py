# -*- coding: utf-8 -*-
"""性能优化：
   ① knowledge_index.js 371.8KB → 懒加载（搜索时才载）
   ② 统一版本号（修 img_style 的 1.8.15，给 3 个脚本补 ?v=）
   ③ 补 og:image / canonical / twitter card
"""
import io, sys, re, os, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = os.path.join(BASE, 'index.html')
V = '1.8.27'
h = open(FP, encoding='utf-8').read()
orig_len = len(h)

# ---------- ① knowledge_index.js 懒加载 ----------
old_tag = '  <script defer src="knowledge_index.js"></script>\n'
if old_tag in h:
    h = h.replace(old_tag, '', 1)
    print('✅ 已移除 knowledge_index.js 的 eager 加载')
elif '<script defer src="knowledge_index.js"></script>' in h:
    h = h.replace('<script defer src="knowledge_index.js"></script>', '', 1)
    print('✅ 已移除 knowledge_index.js（无缩进版）')
else:
    print('❌ 未找到 knowledge_index.js 的 script 标签')

# 在 doSectionQuery 里注入懒加载钩子
hook_anchor = "  var resultBox = document.getElementById('queryResultBox');\n  if(!resultBox) return;\n"
loader_fn = '''  var resultBox = document.getElementById('queryResultBox');
  if(!resultBox) return;

  // 知识库索引按需加载（371.8KB，只在真正查询时才下载）
  if(typeof KNOWLEDGE_INDEX==='undefined'){
    ensureKnowledgeIndex(function(){ try{ doSectionQuery(); }catch(e){} });
  }
'''
if hook_anchor in h:
    h = h.replace(hook_anchor, loader_fn, 1)
    print('✅ 已在 doSectionQuery 注入懒加载钩子')
else:
    print('❌ 未找到 doSectionQuery 锚点（缩进可能不同）')

# 全局 loader 函数（插在主脚本块开头之后）
loader_def = '''
// ===== 知识库索引：按需加载（首屏省 371.8KB）=====
window.__kiLoading=false; window.__kiCbs=[];
function ensureKnowledgeIndex(cb){
  if(typeof KNOWLEDGE_INDEX!=='undefined'){ if(cb)try{cb()}catch(e){} return; }
  if(window.__kiCbs && window.__kiCbs.length>=0 && window.__kiLoading){ window.__kiCbs.push(cb); return; }
  window.__kiLoading=true;
  window.__kiCbs=[cb];
  var s=document.createElement('script');
  s.src='knowledge_index.js?v=' + 'VERSION';
  s.async=true;
  s.onload=function(){
    window.__kiLoading=false;
    var cbs=window.__kiCbs||[]; window.__kiCbs=[];
    cbs.forEach(function(f){ try{ f&&f(); }catch(e){} });
  };
  s.onerror=function(){
    window.__kiLoading=false;
    var cbs=window.__kiCbs||[]; window.__kiCbs=[];
    cbs.forEach(function(f){ try{ f&&f(); }catch(e){} });
  };
  document.head.appendChild(s);
}
'''.replace('VERSION', V)

# 找主脚本块起点插入
m_main = re.search(r'<script>\s*\n\s*// ===== Theme System =====', h)
if m_main:
    ins = m_main.start() + len('<script>')
    h = h[:ins] + '\n' + loader_def + h[ins:]
    print('✅ 已插入 ensureKnowledgeIndex 定义')
else:
    print('❌ 未找到主脚本块入口')

# ---------- ② 版本号统一 ----------
h = h.replace('img_style.js?v=1.8.15', 'img_style.js?v=' + V)
h = re.sub(r'daily_data\.js\?v=[\d.]+', 'daily_data.js?v=' + V, h)
h = re.sub(r'<script defer src="detail_content\.js"></script>',
           '<script defer src="detail_content.js?v=' + V + '"></script>', h)
h = re.sub(r'<script defer src="personal_config\.js"></script>',
           '<script defer src="personal_config.js?v=' + V + '"></script>', h)
print('✅ 版本号已统一为 ' + V)

# ---------- ③ SEO meta ----------
if 'og:image' not in h:
    og = ('  <meta property="og:image" content="https://zr-president.github.io/my-website/assets/img/'
          'a1pMK4456dF2j5B9xvkjMEGiOOw.webp">\n'
          '  <meta name="twitter:card" content="summary_large_image">\n'
          '  <meta name="twitter:title" content="钟锐|个人数字空间">\n'
          '  <meta name="twitter:description" content="17个板块每日更新的个人智能信息中枢">\n')
    anchor = '  <meta property="og:url" content="https://zr-president.github.io/my-website/">\n'
    if anchor in h:
        h = h.replace(anchor, anchor + og, 1)
        print('✅ 已补 og:image + twitter card')
    else:
        print('❌ 未找到 og:url 锚点')
else:
    print('ℹ️  og:image 已存在')

if 'rel="canonical"' not in h:
    anchor2 = '  <link rel="icon" type="image/svg+xml" href="favicon.svg">\n'
    if anchor2 in h:
        h = h.replace(anchor2, anchor2 + '  <link rel="canonical" href="https://zr-president.github.io/my-website/">\n', 1)
        print('✅ 已补 canonical')
    else:
        print('❌ 未找到 favicon 锚点')
else:
    print('ℹ️  canonical 已存在')

open(FP, 'w', encoding='utf-8').write(h)
print()
print('index.html: %.1f KB → %.1f KB' % (orig_len / 1024, len(h) / 1024))

# ---------- 语法校验 ----------
r = subprocess.run(['node', '-e', r"""
const fs=require('fs');
const h=fs.readFileSync('index.html','utf8');
const blocks=[...h.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
let bad=0;
blocks.forEach((m,i)=>{ try{ new Function(m[1]); }catch(e){ bad++; console.log('  块#'+i+' 语法错误: '+e.message); } });
console.log('  内联脚本块: '+blocks.length+' · 失败: '+bad);
console.log('  含 ensureKnowledgeIndex: '+h.includes('function ensureKnowledgeIndex'));
console.log('  仍在首屏加载 knowledge_index: '+/<script[^>]*src="knowledge_index/.test(h));
"""], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(r.stdout or r.stderr[:400])
