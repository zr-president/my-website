#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""修复所有脚本的硬编码路径，改为相对路径（两台机器通用）"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OLD_USER = 'ZR'
OLD_DIR = 'C:\\Users\\ZR\\Desktop\\钟锐的个人网站'

# ============ 1. sync.bat：用 %~dp0 ============
bat = 'sync.bat'
if os.path.exists(bat):
    with open(bat, 'r', encoding='utf-8') as f:
        c = f.read()
    for u in ['ZR', '13172']:
        c = c.replace('cd /d "C:\\Users\\%s\\Desktop\\钟锐的个人网站"' % u, 'cd /d "%~dp0"')
    with open(bat, 'w', encoding='utf-8') as f:
        f.write(c)
    print('OK sync.bat -> %~dp0')

# ============ 2. 根目录脚本 ============
root_scripts = ['apply_32_33.py', 'fix_vocab.py', 'update_insights.py', 'update_optimization.py']
for fname in root_scripts:
    if not os.path.exists(fname):
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    old = "filepath = r'" + OLD_DIR + "\\daily_data.js'"
    new = "filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'daily_data.js')"
    if old in c:
        c = c.replace(old, new)
        if 'import os' not in c:
            c = c.replace('import sys, io', 'import sys, io, os', 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK %s -> 相对路径' % fname)
    else:
        print('SKIP %s (未匹配)' % fname)

# ============ 3. scripts/ 目录脚本 ============
sub_scripts = {
    'scripts/apply_opt2.py': "INDEX = r'" + OLD_DIR + "\\index.html'",
    'scripts/apply_optimizations.py': "ROOT = r'" + OLD_DIR + "'",
}
for fname, old in sub_scripts.items():
    if not os.path.exists(fname):
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    if old in c:
        if 'apply_opt2' in fname:
            new = "INDEX = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')"
        else:
            new = "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"
        c = c.replace(old, new)
        if 'import os' not in c:
            c = c.replace('import sys, io, re', 'import sys, io, re, os', 1)
            c = c.replace('import sys, io', 'import sys, io, os', 1)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(c)
        print('OK %s -> 相对路径' % fname)
    else:
        print('SKIP %s (未匹配)' % fname)

# ============ 4. CLAUDE.md ============
with open('CLAUDE.md', 'r', encoding='utf-8') as f:
    c = f.read()
new_desc = '- 工作目录：项目在桌面「钟锐的个人网站」文件夹，脚本均用相对路径定位（sync.bat 用 %~dp0，Python 用 __file__），两台机器通用'
c = c.replace('- 工作目录：`C:\\Users\\13172\\Desktop\\钟锐的个人网站\\`', new_desc)
c = c.replace('- 工作目录：`C:\\Users\\ZR\\Desktop\\钟锐的个人网站\\`', new_desc)
with open('CLAUDE.md', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK CLAUDE.md -> 机器无关说明')

print('\n=== 最终验证 ===')
import subprocess
result = subprocess.run(['grep', '-rn', 'Users', '--include=*.py', '--include=*.bat', '--include=*.md', '.'],
                        capture_output=True, text=True)
for line in result.stdout.split('\n'):
    if 'ZR' in line or '13172' in line:
        if 'node_modules' not in line:
            print('残留:', line)
print('验证完成')
