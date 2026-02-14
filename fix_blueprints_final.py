#!/usr/bin/env python3
"""Fix Flask Blueprint names in API files."""

import re

files = [
    r'c:\Users\user\composer\web_app\api\scales.py',
    r'c:\Users\user\composer\web_app\api\chords.py',
    r'c:\Users\user\composer\web_app\api\progressions.py',
    r'c:\Users\user\composer\web_app\api\analysis.py'
]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix blueprint names like 'scales - scales.py:12' -> 'scales'
    new_content = re.sub(r"Blueprint\('[\w]+  [\w\.]+:\d+', - fix_blueprints_final.py:18", "Blueprint('scales',", content)
    new_content = re.sub(r"Blueprint\('[\w]+  [\w\.]+:\d+', - fix_blueprints_final.py:19", "Blueprint('chords',", new_content)
    new_content = re.sub(r"Blueprint\('[\w]+  [\w\.]+:\d+', - fix_blueprints_final.py:20", "Blueprint('progressions',", new_content)
    new_content = re.sub(r"Blueprint\('[\w]+  [\w\.]+:\d+', - fix_blueprints_final.py:21", "Blueprint('analysis',", new_content)
    
    with open', encoding='utf(path, 'w-8') as f:
        f.write(new_content)
    
    print(f'Fixed {path} - fix_blueprints_final.py:26')

print('All done! - fix_blueprints_final.py:28')

# Fix analysis.py
with open('web_app/api/analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Blueprint('analysis  analysis.py:15' - fix_blueprints_final.py:33", "Blueprint('analysis'")
with open('web_app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed analysis.py - fix_blueprints_final.py:36')

print('All done! - fix_blueprints_final.py:38')

