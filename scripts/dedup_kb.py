#!/usr/bin/env python3
"""知识库自动去重脚本 — 优化建议 #10
扫描 knowledge_base/ 各分类目录，比对相邻日期的文件，
自动合并或标注重复的二级标题段落，避免跨日内容冗余。
"""
import sys, io, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge_base')
DRY_RUN = '--dry-run' in sys.argv or '-n' in sys.argv
VERBOSE = '--verbose' in sys.argv or '-v' in sys.argv

def extract_sections(text):
    """Extract ##-level sections from markdown text. Returns list of (title, content, start_line)."""
    sections = []
    lines = text.split('\n')
    current_title = '_preamble'
    current_lines = []
    start_line = 0

    for i, line in enumerate(lines):
        if line.startswith('## '):
            if current_lines:
                sections.append((current_title, '\n'.join(current_lines).strip(), start_line))
            current_title = line.strip()
            current_lines = []
            start_line = i
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, '\n'.join(current_lines).strip(), start_line))

    return sections

def section_similarity(title1, title2):
    """Check if two section titles are about the same topic."""
    # Normalize: remove emoji, extra spaces, compare keywords
    def normalize(t):
        t = re.sub(r'[^一-鿿\w\s]', '', t)
        t = re.sub(r'\s+', '', t).lower()
        return t

    n1, n2 = normalize(title1), normalize(title2)
    if n1 == n2:
        return 1.0

    # Check for shared keywords
    words1 = set(re.findall(r'[一-鿿]+|\w+', n1))
    words2 = set(re.findall(r'[一-鿿]+|\w+', n2))
    if not words1 or not words2:
        return 0.0

    overlap = words1 & words2
    return len(overlap) / min(len(words1), len(words2))

def dedup_file(filepath, prev_filepath):
    """Deduplicate file against previous day's file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    with open(prev_filepath, 'r', encoding='utf-8') as f:
        prev_text = f.read()

    sections = extract_sections(text)
    prev_sections = extract_sections(prev_text)
    prev_titles = {s[0] for s in prev_sections}

    new_sections = []
    merged_count = 0
    skipped_count = 0

    for title, content, _ in sections:
        if title == '_preamble':
            new_sections.append((title, content))
            continue

        # Check if this exact section title exists in previous file
        if title in prev_titles:
            # Find matching section in prev
            prev_content = ''
            for pt, pc, _ in prev_sections:
                if pt == title:
                    prev_content = pc
                    break

            # If content is very similar (>80% overlap), skip
            if content == prev_content or _content_similarity(content, prev_content) > 0.8:
                if VERBOSE:
                    print(f'  ⏭  跳过完全相同: {title}')
                skipped_count += 1
                continue
            else:
                # Content differs — merge: keep new content, add note
                merged = content + f'\n\n> 💡 上日同主题要点: {prev_content[:120]}...' if len(prev_content) > 120 else content + f'\n\n> 💡 上日同主题: {prev_content}'
                new_sections.append((title, merged))
                merged_count += 1
                if VERBOSE:
                    print(f'  🔀 合并更新: {title}')
        else:
            # Check for fuzzy matches
            matched = False
            for prev_title in prev_titles:
                sim = section_similarity(title, prev_title)
                if sim > 0.7:
                    prev_content = ''
                    for pt, pc, _ in prev_sections:
                        if pt == prev_title:
                            prev_content = pc
                            break
                    merged = content + f'\n\n> 💡 上日相关({prev_title}): {prev_content[:120]}...'
                    new_sections.append((title, merged))
                    merged_count += 1
                    matched = True
                    if VERBOSE:
                        print(f'  🔀 模糊合并: {title} ≈ {prev_title}')
                    break

            if not matched:
                new_sections.append((title, content))

    # Rebuild file
    preamble = ''
    for title, content in new_sections:
        if title == '_preamble':
            preamble = content
            break

    rebuilt_lines = preamble.split('\n') if preamble else []
    for title, content in new_sections:
        if title != '_preamble':
            rebuilt_lines.append('')
            rebuilt_lines.append(title)
            for line in content.split('\n'):
                rebuilt_lines.append(line)

    # Remove leading blank lines
    while rebuilt_lines and not rebuilt_lines[0].strip():
        rebuilt_lines.pop(0)

    new_text = '\n'.join(rebuilt_lines) + '\n'

    return new_text, skipped_count, merged_count

def _content_similarity(a, b):
    """Simple similarity ratio of two content strings."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    lines_a = set(a.strip().split('\n'))
    lines_b = set(b.strip().split('\n'))
    if not lines_a or not lines_b:
        return 0.0
    overlap = lines_a & lines_b
    return len(overlap) / min(len(lines_a), len(lines_b))

def main():
    categories = [d for d in os.listdir(KB_DIR) if os.path.isdir(os.path.join(KB_DIR, d)) and not d.startswith('.')]

    total_skipped = 0
    total_merged = 0

    for cat in sorted(categories):
        cat_dir = os.path.join(KB_DIR, cat)
        files = sorted(glob.glob(os.path.join(cat_dir, '*.md')))

        if len(files) < 2:
            continue

        # Compare latest file with previous
        latest = files[-1]
        prev = files[-2]

        print(f'\n📂 {cat}/  {os.path.basename(prev)} → {os.path.basename(latest)}')

        try:
            new_text, skipped, merged = dedup_file(latest, prev)
        except Exception as e:
            print(f'  ❌ Error: {e}')
            continue

        if skipped > 0 or merged > 0:
            print(f'  结果: 跳过{skipped}个重复段落, 合并{merged}个更新段落')
            if not DRY_RUN:
                with open(latest, 'w', encoding='utf-8') as f:
                    f.write(new_text)
                print(f'  ✅ 已保存去重版本')
            else:
                print(f'  🔍 [DRY RUN] 未实际修改文件')
        else:
            print(f'  ✅ 无需去重')

        total_skipped += skipped
        total_merged += merged

    print(f'\n{"="*50}')
    print(f'总计: 跳过 {total_skipped} 个重复段落, 合并 {total_merged} 个更新段落')
    if DRY_RUN:
        print('🔍 此为预览模式，追加 --no-dry-run 参数以实际修改文件')

if __name__ == '__main__':
    main()
