# -*- coding: utf-8 -*-
"""把旧版 DETAIL.fitness 的优质尾部内容（12周后判断/认知/资源卡片）接到新版后面"""
import io, sys, re, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
CFP = BASE + r'\detail_content.js'

# 1) 从备份取旧版的优质尾部
c = open(BASE + r'\detail_content.js.bak', 'r', encoding='utf-8').read()
m = re.search(r"(DETAIL\.fitness\s*=\s*)'((?:[^'\\]|\\.)*)'", c)
old = m.group(2)
# JS 单引号字符串里的转义 → 还原
old = old.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
k = old.find('<h3>🔀 12 周后怎么判断下一步</h3>')
if k < 0:
    k = old.find('12 周后怎么判断下一步')
tail = old[k:] if k >= 0 else ''
print('取回旧尾部:', len(tail), '字')

# 2) 读当前新版
cur = open(CFP, 'r', encoding='utf-8').read()
m2 = re.search(r"(DETAIL\.fitness\s*=\s*)(\"(?:[^\"\\]|\\.)*\")", cur)
if not m2:
    print('❌ 未找到新版'); raise SystemExit(1)
newv = json.loads(m2.group(2))
print('当前新版:', len(newv), '字')

# 3) 去掉新版里重复的安全提醒（尾部会有），再拼接
newv2 = newv.replace(
    '<div class="callout warn">⚠️ 安全提醒：热身 5 分钟 ｜ 关节疼立刻停 ｜ 每周休息 ≥2 天 ｜ 增肌期睡眠 ≥7 小时（睡不够等于白练）｜ 单杠务必确认安装牢固</div>',
    '')
merged = newv2 + '<h3>🔀 12 周后怎么判断下一步</h3>' + tail.split('<h3>🔀 12 周后怎么判断下一步</h3>', 1)[1]
# 安全提醒补回（含单杠提醒）
merged = merged.replace('检查拉力绳固定', '检查拉力绳/单杠固定')
print('合并后:', len(merged), '字')

cur = cur[:m2.start(2)] + json.dumps(merged, ensure_ascii=False) + cur[m2.end(2):]
open(CFP, 'w', encoding='utf-8').write(cur)

r = subprocess.run(['node', '--check', CFP], capture_output=True, text=True)
print('语法：', 'OK' if r.returncode == 0 else 'FAIL ' + r.stderr[:300])

v = subprocess.run(['node', '-e', r"""
const fs=require('fs'),vm=require('vm');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('detail_content.js','utf8'),c);
const f=c.DETAIL.fitness;
console.log('最终长度:', f.length);
for (const k of ['60.65kg','骨盆前倾','进阶阶梯','空心支撑','门框单杠','12 周后怎么判断','博主推荐','Jeremy Ethier','安全提醒']) {
  console.log('  含 '+k+': '+f.includes(k));
}
"""], capture_output=True, text=True, encoding='utf-8', cwd=BASE)
print(v.stdout or v.stderr[:400])
