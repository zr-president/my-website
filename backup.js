/* 数据备份/恢复 · 纯逻辑（可单测，不依赖 DOM）
   背景：两个站同源（zr-president.github.io），localStorage 共享。
   所以一个备份页可以同时备份个人站与训练场的全部数据。

   设计要点：
   - 导出：收集 localStorage 里的应用键，打成 {meta, data} 的 JSON
   - 校验：结构、版本、值类型逐项检查，任何一项不符就整体拒绝（不做「部分导入」）
   - 导入计划：明确区分「会覆盖」/「会新增」/「保持不动」，让用户看清楚再决定
   - 默认不动备份里没有的键（防止「导入旧备份」把后来新增的数据清掉） */
var BackupKit = (function () {
  var VERSION = 1;

  /* 应用数据键的识别规则（前缀 + 精确名） */
  var PREFIXES = [
    'zhongrui_',   // 简历、待办、跟踪、面试
    'zh_',         // 投递状态、备注、成长、日历
    'dsh_',        // 日历事件
    'tp_',         // 训练场：进度、笔记、自评、时间戳、摘要、雷达
    'my',          // myJudgments / myObservations
    'skill',       // skillRadar / skillPractice
    'vocab',       // vocabFlashcards
    'subject',     // subjectPathProgress
    'mock'         // mockInterviewLog
  ];
  var EXACT = ['theme', 'themeColor', 'lastRefresh'];

  function isAppKey(k) {
    if (!k) return false;
    for (var i = 0; i < EXACT.length; i++) if (k === EXACT[i]) return true;
    for (var j = 0; j < PREFIXES.length; j++) {
      if (k.indexOf(PREFIXES[j]) === 0) return true;
    }
    return false;
  }

  /* 粗略分组，用于展示「这份备份里都有什么」 */
  var GROUPS = [
    { key: 'train',  label: '训练场（进度/笔记/自评）', test: function (k) { return k.indexOf('tp_') === 0; } },
    { key: 'resume', label: '简历与求职（简历/投递/面试）', test: function (k) { return k.indexOf('zhongrui_') === 0 || k.indexOf('zh_apply') === 0; } },
    { key: 'cal',    label: '日历与日程', test: function (k) { return k.indexOf('dsh_') === 0; } },
    { key: 'learn',  label: '学习记录（词汇/判断/雷达）', test: function (k) {
        return k.indexOf('vocab') === 0 || k.indexOf('my') === 0 || k.indexOf('skill') === 0 ||
               k.indexOf('subject') === 0 || k.indexOf('mock') === 0 || k.indexOf('zh_growth') === 0; } },
    { key: 'pref',   label: '偏好设置（主题等）', test: function (k) {
        return k === 'theme' || k === 'themeColor' || k === 'lastRefresh'; } }
  ];

  function bytesOf(s) {
    /* 用 UTF-8 估算字节数（无 TextEncoder 环境退化用长度×2） */
    try {
      if (typeof TextEncoder !== 'undefined') return new TextEncoder().encode(s).length;
    } catch (e) {}
    var n = 0;
    for (var i = 0; i < s.length; i++) n += s.charCodeAt(i) > 127 ? 2 : 1;
    return n;
  }

  /* 从某个 storage（默认 localStorage）收集数据 */
  function collect(store) {
    store = store || (typeof localStorage !== 'undefined' ? localStorage : null);
    if (!store) return { meta: { version: VERSION, exportedAt: null, keyCount: 0, bytes: 0 }, data: {} };
    var data = {}, count = 0, bytes = 0;
    for (var i = 0; i < store.length; i++) {
      var k = store.key ? store.key(i) : null;
      if (!k) continue;
      if (!isAppKey(k)) continue;
      var v = null;
      try { v = store.getItem(k); } catch (e) { continue; }
      if (v === null || v === undefined) continue;
      data[k] = String(v);
      count++;
      bytes += bytesOf(k) + bytesOf(String(v));
    }
    return {
      meta: {
        version: VERSION,
        exportedAt: nowIso(),
        origin: (typeof location !== 'undefined' ? location.origin : ''),
        keyCount: count,
        bytes: bytes
      },
      data: data
    };
  }

  function nowIso() {
    var d = new Date();
    function p(n) { return String(n).padStart(2, '0'); }
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) +
           'T' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
  }

  /* 按分组统计 */
  function groupStats(data) {
    var out = [];
    var seen = {};
    GROUPS.forEach(function (g) {
      var n = 0, b = 0;
      for (var k in data) {
        if (seen[k]) continue;
        if (g.test(k)) { n++; b += bytesOf(k) + bytesOf(data[k]); seen[k] = 1; }
      }
      out.push({ key: g.key, label: g.label, count: n, bytes: b });
    });
    var restN = 0, restB = 0;
    for (var k2 in data) {
      if (!seen[k2]) { restN++; restB += bytesOf(k2) + bytesOf(data[k2]); }
    }
    if (restN) out.push({ key: 'other', label: '其他', count: restN, bytes: restB });
    return out;
  }

  /* 校验一份备份对象。任何一项不合格都整体拒绝，不做部分导入。 */
  function validate(obj) {
    if (!obj || typeof obj !== 'object') return { ok: false, error: '不是有效的 JSON 对象' };
    if (!obj.meta || typeof obj.meta !== 'object') return { ok: false, error: '缺少 meta 段（不像是本工具导出的备份）' };
    if (obj.meta.version !== VERSION) {
      return { ok: false, error: '备份版本不匹配（文件 v' + obj.meta.version + '，当前 v' + VERSION + '）' };
    }
    if (!obj.data || typeof obj.data !== 'object' || Array.isArray(obj.data)) {
      return { ok: false, error: '缺少 data 段，或 data 不是对象' };
    }
    var keys = Object.keys(obj.data);
    if (!keys.length) return { ok: false, error: '备份里没有任何数据键' };

    var notString = [], notApp = [];
    keys.forEach(function (k) {
      if (typeof obj.data[k] !== 'string') notString.push(k);
      if (!isAppKey(k)) notApp.push(k);
    });
    if (notString.length) {
      return { ok: false, error: '有 ' + notString.length + ' 个键的值不是字符串：' + notString.slice(0, 3).join(', ') };
    }
    return {
      ok: true,
      meta: obj.meta,
      data: obj.data,
      warning: notApp.length
        ? ('注意：有 ' + notApp.length + ' 个键不是本工具认识的键（' + notApp.slice(0, 3).join(', ') + '），仍会一并恢复')
        : ''
    };
  }

  /* 导入计划：会覆盖 / 会新增 / 保持不动 */
  function planImport(backupData, currentKeys) {
    currentKeys = currentKeys || [];
    var cur = {};
    currentKeys.forEach(function (k) { cur[k] = 1; });
    var overwrite = [], add = [], same = [];
    Object.keys(backupData).forEach(function (k) {
      if (cur[k]) overwrite.push(k); else add.push(k);
    });
    var untouched = currentKeys.filter(function (k) { return !(k in backupData); });
    return {
      overwrite: overwrite, add: add, untouched: untouched,
      summary: '将覆盖 ' + overwrite.length + ' 项 · 新增 ' + add.length + ' 项 · 保留当前 ' + untouched.length + ' 项（备份里没有的不动）'
    };
  }

  /* 执行导入（store 可注入以便测试） */
  function applyImport(store, backupData) {
    store = store || (typeof localStorage !== 'undefined' ? localStorage : null);
    var n = 0, failed = [];
    for (var k in backupData) {
      try { store.setItem(k, String(backupData[k])); n++; }
      catch (e) { failed.push(k); }
    }
    return { written: n, failed: failed };
  }

  /* 时间戳片段，用于文件名（YYYYMMDDHHMM） */
  function timeStampName() {
    return nowIso().replace(/[-:T]/g, '').slice(0, 12);
  }

  /* 生成下载用的文件名 */
  function fileName() {
    return 'zhongrui-backup-' + timeStampName() + '.json';
  }

  function stringify(payload) {
    return JSON.stringify(payload, null, 2);
  }

  return {
    VERSION: VERSION,
    isAppKey: isAppKey,
    collect: collect,
    validate: validate,
    planImport: planImport,
    applyImport: applyImport,
    groupStats: groupStats,
    bytesOf: bytesOf,
    fileName: fileName,
    timeStampName: timeStampName,
    stringify: stringify,
    nowIso: nowIso
  };
})();

if (typeof module !== 'undefined' && module.exports) module.exports = BackupKit;
