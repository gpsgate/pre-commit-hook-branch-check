from __future__ import annotations

import argparse
import sys
import subprocess
import re

# Default patterns are for conventional commits. See:
# https://conventional-branch.github.io/
DEFAULT_ALLOWED_PATTERNS = [
    '^(feature|bugfix|hotfix|release|chore)/[a-z0-9/.-]+$'
]
DEFAULT_DENIED_PATTERNS = [
    '^(main|master)$'
]


def main(argv: Sequence[str] | None = None) -> int:
    """
    Main function for the branch_check script. Parses the command-line
    arguments, then checks the name of the branch against the allowed/denied
    patterns.  A branch name must match at least one of the allowed patterns
    and must not match any of the denied patterns.

    Args:
      argv: A sequence of command-line arguments. If None, sys.argv[1:] will be
      used.

    Returns:
      An integer representing the exit code. 0 indicates success, while non-zero
      values indicate errors.
    """
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog='branch_check', description='Check branch name against allow/deny patterns')

    parser.add_argument(
        '-a', '--allow',
        dest='allow',
        action='append',
        help='Regular expression that branch name should match, can be repeated.'
    )

    parser.add_argument(
        '-d', '--deny',
        dest='deny',
        action='append',
        help='Regular expression that branch name should not match, can be repeated.'
    )

    args = parser.parse_args(argv)
    allow_patterns = args.allow or DEFAULT_ALLOWED_PATTERNS
    deny_patterns = args.deny or DEFAULT_DENIED_PATTERNS
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
    if not branch_name:
        print('No branch name found. Are you in a git repository?')
        return 1
    
    # Check if the branch name matches any of the allowed patterns
    if not any(re.match(pattern, branch_name) for pattern in allow_patterns):
        print(f'Branch name "{branch_name}" does not match any of the allowed patterns: {allow_patterns}')
        return 1
    # Check if the branch name matches any of the denied patterns
    if any(re.match(pattern, branch_name) for pattern in deny_patterns):
        print(f'Branch name "{branch_name}" matches a denied pattern: {deny_patterns}')
        return 1
    print(f'Branch name "{branch_name}" is valid.')
    return 0
    

if __name__ == '__main__':
    raise SystemExit(main())
