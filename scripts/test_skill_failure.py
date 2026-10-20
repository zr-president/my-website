# -*- coding: utf-8 -*-
"""验收测试 #4「失败可见」：
   故意把某个分区的 updated 改成昨天，确认 check_consistency 必须报错；
   然后恢复，确认重新变绿。
   —— 这是 Skill 6 组验收标准里最重要的一项（防止静默通过）
"""
import io, sys, re, os, shutil, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:\Users\ZR\Desktop\钟锐的个人网站'
FP = os.path.join(BASE, 'daily_data.js')
BAK = os.path.join(BASE, '_test_backup.js')

print('=== 步骤 1：备份 ===')
shutil.copy2(FP, BAK)
print('  已备份到 _test_backup.js')

print()
print('=== 步骤 2：注入错误（把 ai-track 的 updated 改成 2026-10-19）===')
d = open(FP, encoding='utf-8').read()
orig = d
# 只改 ai-track 段的 updated
m = re.search(r'("?ai-track"?\s*:\s*\{[\s\S]*?)("?updated"?\s*:\s*")(2026-10-20)(")', d)
if m:
    d = d[:m.start()] + m.group(1) + m.group(2) + '2026-10-19' + m.group(4) + d[m.end():]
    open(FP, 'w', encoding='utf-8').write(d)
    print('  已注入：ai-track.updated = 2026-10-19')
else:
    print('  ❌ 未找到 ai-track 的 updated 字段')

print()
print('=== 步骤 3：跑 check_consistency（期望：失败）===')
r = subprocess.run([sys.executable, 'scripts/check_consistency.py'], capture_output=True,
                   text=True, encoding='utf-8', errors='replace', cwd=BASE)
out = (r.stdout or '') + (r.stderr or '')
caught = (r.returncode != 0) or ('日期审计' in out and '❌' in out) or ('不一致' in out)
for line in out.splitlines():
    if any(k in line for k in ['日期审计', '❌', '错误', '通过（']):
        print('  ' + line.strip()[:110])
print()
print('  退出码: %d' % r.returncode)
print('  → 检查是否抓住了错误: %s' % ('✅ 抓住了' if caught else '❌ 没抓住（静默通过 = 不合格）'))

print()
print('=== 步骤 4：恢复 ===')
shutil.copy2(BAK, FP)
os.remove(BAK)
print('  已恢复')

print()
print('=== 步骤 5：确认恢复后变绿 ===')
r2 = subprocess.run([sys.executable, 'scripts/check_consistency.py'], capture_output=True,
                    text=True, encoding='utf-8', errors='replace', cwd=BASE)
out2 = (r2.stdout or '') + (r2.stderr or '')
ok = (r2.returncode == 0)
print('  退出码: %d → %s' % (r2.returncode, '✅ 已恢复绿' if ok else '⚠️ 仍未通过'))
for line in out2.splitlines()[-4:]:
    if line.strip():
        print('  ' + line.strip()[:110])

print()
print('=== 验收结论 ===')
print('  Skill 验收标准 #4「失败可见」: %s' % ('✅ 通过' if (caught and ok) else '❌ 未通过'))
