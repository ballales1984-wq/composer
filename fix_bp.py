#!/usr/bin/env python3
"""Fix Flask Blueprint names in API files."""

files = [
    ('c:\\Users\\user\\composer\\web_app\\api\\scales.py', 'scales'),
    ('c:\\Users\\user\\composer\\web_app\\api\\chords.py', 'chords'),
    ('c:\\Users\\user\\composer\\web_app\\api\\progressions.py', 'progressions'),
    ('c:\\Users\\user\\composer\\web_app\\api\\analysis.py', 'analysis'),
]

for path, name in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the blueprint line
    import re
    pattern = r"Blueprint\('.*?'"
    replacement = f"Blueprint('{name}' - fix_bp.py:18"
    new_content = re.sub(pattern, replacement, content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'Fixed {path} - fix_bp.py:24')

print('All done! - fix_bp.py:26')

