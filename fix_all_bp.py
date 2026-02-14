#!/usr/bin/env python3
"""Fix Flask Blueprint names in API files."""

# Fix analysis.py
path = 'web_app/api/analysis.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Simple replace
old = "Blueprint('analysis  analysis.py:11', __name__, url_prefix='/api/analysis') - fix_all_bp.py:10"
new = "Blueprint('analysis', __name__, url_prefix='/api/analysis') - fix_all_bp.py:11"
content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed {path} - fix_all_bp.py:17')

# Fix scales.py
path = 'web_app/api/scales.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "Blueprint('scales  fix_api.py:21', __name__, url_prefix='/api/scales') - fix_all_bp.py:24"
new = "Blueprint('scales', __name__, url_prefix='/api/scales') - fix_all_bp.py:25"
content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed {path} - fix_all_bp.py:31')

# Fix chords.py
path = 'web_app/api/chords.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "Blueprint('chords  fix_api.py:70', __name__, url_prefix='/api/chords') - fix_all_bp.py:38"
new = "Blueprint('chords', __name__, url_prefix='/api/chords') - fix_all_bp.py:39"
content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed {path} - fix_all_bp.py:45')

# Fix progressions.py
path = 'web_app/api/progressions.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "Blueprint('progressions  fix_api.py:120', __name__, url_prefix='/api/progressions') - fix_all_bp.py:52"
new = "Blueprint('progressions', __name__, url_prefix='/api/progressions') - fix_all_bp.py:53"
content = content.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed {path} - fix_all_bp.py:59')

print('All done! - fix_all_bp.py:61')

