#!/usr/bin/env python3
"""安全编辑包装器 — 优化建议 #29
在编辑 daily_data.js 之前自动 git stash，编辑后自动 JS 语法校验，
失败则回滚，防止脚本替换错误导致文件全损。

用法:
  python scripts/safe_edit.py <target_file> <edit_script.py> [args...]

工作流:
  1. git stash push <target_file>  (备份当前状态)
  2. python <edit_script.py> [args]  (执行编辑)
  3. node -e "new Function(fs.readFileSync(...))"  (JS 语法校验)
  4. 成功 → git stash drop (丢弃备份)
  5. 失败 → git checkout -- <target_file> (回滚到备份前)
"""
import sys, io, os, subprocess, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def run(cmd, cwd=None):
    """Run a command and return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, timeout=30)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'
    except Exception as e:
        return -1, '', str(e)

def main():
    parser = argparse.ArgumentParser(description='Safe edit wrapper with git backup + JS validation')
    parser.add_argument('target', help='Target file to edit (relative to repo root)')
    parser.add_argument('script', help='Python edit script to run')
    parser.add_argument('script_args', nargs='*', help='Additional args for the edit script')
    parser.add_argument('--no-git', action='store_true', help='Skip git operations (no repo)')
    parser.add_argument('--no-validate', action='store_true', help='Skip JS syntax validation')
    parser.add_argument('--repo', default=None, help='Path to git repo (default: auto-detect from target)')
    args = parser.parse_args()

    target_abs = os.path.abspath(args.target)
    if not os.path.exists(target_abs):
        print(f'❌ Target file not found: {target_abs}')
        sys.exit(1)

    # Determine repo root
    if args.repo:
        repo_root = args.repo
    else:
        repo_root = os.path.dirname(target_abs)
        # Walk up to find .git
        while repo_root and not os.path.isdir(os.path.join(repo_root, '.git')):
            parent = os.path.dirname(repo_root)
            if parent == repo_root:
                repo_root = None
                break
            repo_root = parent

    target_rel = os.path.relpath(target_abs, repo_root) if repo_root else target_abs

    # Step 1: Backup
    if not args.no_git and repo_root:
        print(f'📦 git stash push {target_rel} ...')
        rc, out, err = run(f'git stash push -- "{target_rel}"', cwd=repo_root)
        if rc != 0:
            print(f'⚠️  git stash warning: {err}')
        else:
            print(f'   ✅ Backup saved')
    else:
        # Simple backup
        backup = target_abs + '.bak'
        with open(target_abs, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(backup, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f'📦 Backup saved to {backup}')

    # Step 2: Run edit script
    print(f'🔧 Running edit script: {args.script} ...')
    cmd = f'python "{args.script}"' + (' ' + ' '.join(f'"{a}"' for a in args.script_args) if args.script_args else '')
    rc, out, err = run(cmd, cwd=os.path.dirname(target_abs) if not repo_root else repo_root)
    if out:
        print(out)
    if rc != 0:
        print(f'❌ Edit script failed (exit {rc}): {err}')
        # Rollback
        _rollback(target_abs, repo_root, target_rel, args.no_git)
        sys.exit(1)
    print('   ✅ Edit script completed')

    # Step 3: Validate JS syntax (for .js files)
    if not args.no_validate and target_abs.endswith('.js'):
        print('🔍 Validating JavaScript syntax ...')
        validate_script = f"""
var fs = require('fs');
try {{
    var code = fs.readFileSync('{target_abs.replace(chr(92), chr(47))}', 'utf8');
    new Function(code);
    console.log('OK');
}} catch(e) {{
    console.log('ERROR: ' + e.message.split('\\n')[0]);
    process.exit(1);
}}
"""
        rc, out, err = run(f'node -e "{validate_script}"')
        if 'OK' in out:
            print('   ✅ JS syntax valid')
        else:
            print(f'   ❌ JS syntax error: {out}')
            _rollback(target_abs, repo_root, target_rel, args.no_git)
            sys.exit(1)
    else:
        print('⏭️  Skipping validation')

    # Step 4: Success — discard backup
    if not args.no_git and repo_root:
        rc, out, err = run('git stash drop', cwd=repo_root)
        if rc == 0:
            print('🗑️  Backup discarded (edit successful)')
    else:
        backup = target_abs + '.bak'
        if os.path.exists(backup):
            os.remove(backup)
            print('🗑️  Backup discarded (edit successful)')

    # Final summary
    print(f'\n✅ Safe edit complete! {target_rel} updated successfully.')

def _rollback(target_abs, repo_root, target_rel, no_git):
    """Rollback to backup."""
    print('\n🔄 Rolling back to backup...')
    if not no_git and repo_root:
        rc, out, err = run(f'git checkout -- "{target_rel}"', cwd=repo_root)
        if rc == 0:
            print('   ✅ Rollback successful (git checkout)')
        else:
            print(f'   ⚠️  git checkout failed: {err}')
        # Drop the stash
        run('git stash drop', cwd=repo_root)
    else:
        backup = target_abs + '.bak'
        if os.path.exists(backup):
            with open(backup, 'r', encoding='utf-8') as f:
                original = f.read()
            with open(target_abs, 'w', encoding='utf-8') as f:
                f.write(original)
            os.remove(backup)
            print('   ✅ Rollback successful (backup file)')
    print('⚠️  File restored to pre-edit state. Fix the edit script and retry.')

if __name__ == '__main__':
    main()
