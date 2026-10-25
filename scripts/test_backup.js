/* 备份/恢复逻辑 · 回归测试
   用法：node scripts/test_backup.js   （退出码 0 = 通过）
   只测纯逻辑（collect / validate / planImport / applyImport / groupStats），不碰 DOM。 */
const path = require('path');
const BackupKit = require(path.join(__dirname, '..', 'backup.js'));

let pass = 0, fail = 0;
function chk(name, actual, expected) {
  const ok = String(actual) === String(expected);
  console.log((ok ? '  \u2705 ' : '  \u274c ') + name + '  \u2192  \u5b9e\u9645 ' + actual + ' / \u671f\u671b ' + expected);
  if (ok) pass++; else fail++;
}
function t(name, cond) { chk(name, !!cond, true); }

/* 简易 storage 模拟 */
function mockStore(init) {
  const m = Object.assign({}, init || {});
  return {
    get length() { return Object.keys(m).length; },
    key(i) { return Object.keys(m)[i] || null; },
    getItem(k) { return k in m ? m[k] : null; },
    setItem(k, v) { m[k] = String(v); },
    _dump() { return m; }
  };
}

console.log('=== T1 \u5e94\u7528\u952e\u8bc6\u522b ===');
t('tp_note_xxx \u662f\u5e94\u7528\u952e', BackupKit.isAppKey('tp_note_workflow::w01_score_a'));
t('zhongrui_resume \u662f\u5e94\u7528\u952e', BackupKit.isAppKey('zhongrui_resume'));
t('theme \u662f\u5e94\u7528\u952e', BackupKit.isAppKey('theme'));
t('myprefix \u4e5f\u4f1a\u547d\u4e2d\uff08my \u524d\u7f00\uff09', BackupKit.isAppKey('myJudgments'));
t('\u7b2c\u4e09\u65b9\u952e\u4e0d\u7b97', !BackupKit.isAppKey('_ga'));
t('\u7a7a\u952e\u4e0d\u7b97', !BackupKit.isAppKey(''));

console.log('');
console.log('=== T2 collect\uff08\u53ea\u6536\u5e94\u7528\u952e\uff09===');
const st = mockStore({
  'zhongrui_resume': '{"a":1}',
  'tp_note_x': 'v',
  'theme': 'dark',
  '_ga': 'GA1.2',
  'someRandom': 'nope'
});
const col = BackupKit.collect(st);
chk('\u6536\u96c6\u5230\u7684\u952e\u6570', Object.keys(col.data).length, 3);
t('\u4e0d\u542b _ga', !('_ga' in col.data));
t('\u4e0d\u542b someRandom', !('someRandom' in col.data));
chk('meta.version', col.meta.version, 1);
t('meta.exportedAt \u6709\u503c', !!col.meta.exportedAt);
t('meta.bytes > 0', col.meta.bytes > 0);

console.log('');
console.log('=== T3 validate ===');
const good = BackupKit.collect(mockStore({ 'theme': 'dark', 'tp_note_a': 'x' }));
t('\u5408\u6cd5\u5907\u4efd\u901a\u8fc7', BackupKit.validate(good).ok);

t('\u975e\u5bf9\u8c61\u62d2\u7edd', !BackupKit.validate(null).ok);
t('\u6570\u7ec4\u62d2\u7edd', !BackupKit.validate([]).ok);
t('\u7f3a meta \u62d2\u7edd', !BackupKit.validate({ data: {} }).ok);

const wrongVer = { meta: { version: 99 }, data: { theme: 'dark' } };
const vWrong = BackupKit.validate(wrongVer);
t('\u7248\u672c\u4e0d\u5339\u914d\u62d2\u7edd', !vWrong.ok);
t('\u7248\u672c\u9519\u8bef\u63d0\u5230\u7248\u672c', /版本/.test(vWrong.error));

t('\u7f3a data \u62d2\u7edd', !BackupKit.validate({ meta: { version: 1 } }).ok);
t('\u7a7a data \u62d2\u7edd', !BackupKit.validate({ meta: { version: 1 }, data: {} }).ok);
t('data \u662f\u6570\u7ec4\u62d2\u7edd', !BackupKit.validate({ meta: { version: 1 }, data: [] }).ok);

const badVal = { meta: { version: 1 }, data: { theme: 'dark', tp_note_a: 123 } };
const vBad = BackupKit.validate(badVal);
t('\u975e\u5b57\u7b26\u4e32\u503c\u62d2\u7edd', !vBad.ok);
t('\u63d0\u5230\u54ea\u4e2a\u952e', /tp_note_a/.test(vBad.error));

const unknownKey = { meta: { version: 1 }, data: { theme: 'dark', weird_key: 'v' } };
const vUnk = BackupKit.validate(unknownKey);
t('\u672a\u77e5\u952e\u4ecd\u901a\u8fc7', vUnk.ok);
t('\u4f46\u7ed9\u51fa\u8b66\u544a', /不是本工具认识/.test(vUnk.warning));

console.log('');
console.log('=== T4 planImport\uff08\u8986\u76d6/\u65b0\u589e/\u4fdd\u7559\uff09===');
const plan = BackupKit.planImport(
  { theme: 'dark', 'tp_note_a': 'x', 'new_key_zh_': 'y' },
  ['theme', 'tp_note_a', 'zhongrui_resume']
);
chk('\u4f1a\u8986\u76d6\u7684', plan.overwrite.length, 2);
chk('\u4f1a\u65b0\u589e\u7684', plan.add.length, 1);
chk('\u4fdd\u7559\u4e0d\u52a8\u7684', plan.untouched.length, 1);
chk('\u4fdd\u7559\u7684\u662f\u54ea\u4e2a', plan.untouched[0], 'zhongrui_resume');
t('summary \u63d0\u5230\u4e09\u4e2a\u6570\u5b57', /覆盖 2/.test(plan.summary) && /新增 1/.test(plan.summary) && /保留当前 1/.test(plan.summary));

console.log('');
console.log('=== T5 applyImport\uff08\u771f\u5199\u5165\uff09===');
const target = mockStore({ 'zhongrui_resume': 'old', 'other': 'keep' });
const res = BackupKit.applyImport(target, { theme: 'light', 'zhongrui_resume': 'new' });
chk('\u5199\u5165\u6b21\u6570', res.written, 2);
chk('\u5931\u8d25\u6570', res.failed.length, 0);
chk('resume \u5df2\u88ab\u8986\u76d6', target.getItem('zhongrui_resume'), 'new');
chk('theme \u5df2\u65b0\u589e', target.getItem('theme'), 'light');
chk('\u5907\u4efd\u91cc\u6ca1\u6709\u7684\u952e\u4e0d\u52a8', target.getItem('other'), 'keep');

/* \u5199\u5165\u5931\u8d25\u7684\u60c5\u51b5 */
const failing = {
  length: 0, key() { return null; }, getItem() { return null; },
  setItem(k) { if (k === 'bad') throw new Error('quota'); }
};
const res2 = BackupKit.applyImport(failing, { ok: '1', bad: '2' });
chk('\u6210\u529f 1 \u9879', res2.written, 1);
chk('\u5931\u8d25 1 \u9879', res2.failed.length, 1);
chk('\u5931\u8d25\u7684\u662f bad', res2.failed[0], 'bad');

console.log('');
console.log('=== T6 groupStats\uff08\u5206\u7ec4\u7edf\u8ba1\uff09===');
const gs = BackupKit.groupStats({
  'tp_note_a': 'x', 'tp_note_b': 'y',
  'zhongrui_resume': 'r',
  'theme': 'dark'
});
const byKey = {};
gs.forEach(g => { byKey[g.key] = g; });
chk('\u8bad\u7ec3\u573a\u7ec4\u9879\u6570', byKey.train.count, 2);
chk('\u7b80\u5386\u7ec4\u9879\u6570', byKey.resume.count, 1);
chk('\u504f\u597d\u7ec4\u9879\u6570', byKey.pref.count, 1);
chk('\u603b\u9879\u6570\u52a0\u8d77\u6765', gs.reduce((a, g) => a + g.count, 0), 4);

console.log('');
console.log('=== T7 \u6587\u4ef6\u540d ===');
const fn = BackupKit.fileName();
t('\u4ee5 zhongrui-backup- \u5f00\u5934', fn.indexOf('zhongrui-backup-') === 0);
t('\u4ee5 .json \u7ed3\u5c3e', /\.json$/.test(fn));
t('\u542b 12 \u4f4d\u65f6\u95f4\u6233', /\d{12}/.test(fn));

console.log('');
console.log('=== \u7ed3\u679c\uff1a' + pass + ' \u901a\u8fc7 / ' + fail + ' \u5931\u8d25 ===');
process.exit(fail ? 1 : 0);
