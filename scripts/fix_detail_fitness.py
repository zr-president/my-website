# -*- coding: utf-8 -*-
"""补写 DETAIL.fitness（它是赋值语句 DETAIL.fitness = '...'，单引号）"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'
GEN = BASE + r'\scripts\update_fitness_1018.py'

# 从生成器里取出 DETAIL 的 Python 字符串定义
src = open(GEN, encoding='utf-8').read()
s = src.find('DETAIL = (')
e = src.find("\n# 写入 detail_content.js")
ns = {}
exec(src[s:e], ns)
DETAIL = ns['DETAIL']
print('新 DETAIL 长度:', len(DETAIL))

c = open(CFP, 'r', encoding='utf-8').read()
pat = re.compile(r"(DETAIL\.fitness\s*=\s*)'(?:[^'\\]|\\.)*'")
m = pat.search(c)
if not m:
    print('❌ 仍未匹配')
    # 调试：打印赋值开头
    i = c.find('DETAIL.fitness =')
    print(repr(c[i:i+120]))
else:
    print('原长度:', len(m.group(0)))
    c = c[:m.end()] + '' if False else c[:m.start()] + m.group(1) + json.dumps(DETAIL, ensure_ascii=False) + c[m.end():]
    open(CFP, 'w', encoding='utf-8').write(c)
    print('✅ DETAIL.fitness 已替换')

r = subprocess.run(['node', '--check', CFP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])

# 验证
v = subprocess.run(['node', '-e', r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('detail_content.js','utf8'),c);
const f=c.DETAIL.fitness;
console.log('长度:', f.length);
for (const k of ['60.65kg','骨盆前倾','进阶阶梯','推拉','空心支撑','臀桥','单杠']) {
  console.log('  含 '+k+': '+f.includes(k));
}
"""], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(v.stdout or v.stderr[:400])
