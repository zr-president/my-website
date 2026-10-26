# -*- coding: utf-8 -*-
"""INSIGHTS 三字段替换助手（供 update_1026_* 复用）

踩过的坑（都在这里处理掉）：
1. daily_data.js 里既有 "anime": {...}（要闻卡字段）又有 anime: {...}（INSIGHTS 分区）
   → 只在 `var INSIGHTS` 之后搜索
2. 分区名有的带引号（"ai-track"）有的不带（stock）
   → 正则同时兼容
3. 字符串字面量单双引号混用
   → 用引号类型原样保留，只替换内部内容
4. 花括号扫描要跳过字符串里的 { }
   → 逐字符状态机
"""
import re

def make_patcher(path, today=None):
    src = open(path, encoding='utf-8').read()
    ins_start = src.index('var INSIGHTS')

    def find_string_literal(s, pos):
        i = pos
        while i < len(s) and s[i] in ' \t\r\n':
            i += 1
        if i >= len(s) or s[i] not in '"\'':
            return None
        q = s[i]
        j = i + 1
        while j < len(s):
            c = s[j]
            if c == '\\':
                j += 2; continue
            if c == q:
                return (i, j + 1, s[i:j+1])
            j += 1
        return None

    def esc_js(text, quote='"'):
        text = text.replace('\\', '\\\\').replace('\n', '\\n')
        if quote == '"':
            text = text.replace('"', '\\"')
        else:
            text = text.replace("'", "\\'")
        return text

    def section_span(s, key):
        pat = re.compile(r'(?:"' + re.escape(key) + r'"|' + re.escape(key) + r')\s*:\s*\{')
        m = pat.search(s, ins_start)
        if not m:
            return None
        start = m.end() - 1
        depth = 0
        i = start
        in_str = None
        while i < len(s):
            c = s[i]
            if in_str:
                if c == '\\':
                    i += 2; continue
                if c == in_str:
                    in_str = None
                i += 1; continue
            if c in '"\'':
                in_str = c; i += 1; continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return (start, i + 1)
            i += 1
        return None

    def set_field(s, key, field, value):
        span = section_span(s, key)
        if not span:
            raise SystemExit('❌ 找不到分区 %s' % key)
        bs, be = span
        block = s[bs:be]
        fm = re.compile(r'(["\']?' + field + r'["\']?\s*:\s*)').search(block)
        if not fm:
            raise SystemExit('❌ 分区 %s 找不到字段 %s' % (key, field))
        lit = find_string_literal(block, fm.end())
        if not lit:
            raise SystemExit('❌ 分区 %s 的 %s 不是字符串字面量' % (key, field))
        qs, qe, raw = lit
        q = raw[0]
        return s[:bs] + block[:qs] + q + esc_js(value, q) + q + block[qe:] + s[be:]

    def apply(content_map):
        """content_map: {key: {'summary':..., 'trend':..., 'tip':...}}  返回更新字段数"""
        n = 0
        cur = src
        for key, fields in content_map.items():
            for f in ['summary', 'trend', 'tip']:
                if f not in fields:
                    raise SystemExit('❌ %s 缺少字段 %s' % (key, f))
                before = cur
                cur = set_field(cur, key, f, fields[f])
                if cur != before:
                    n += 1
        open(path, 'w', encoding='utf-8').write(cur)
        return n

    return apply
