#!/usr/bin/env python3
"""Fix Flask Blueprint names in API files."""

# Fix scales.py
with open('web_app/api/scales.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Blueprint('scales  scales.py:14' - fix.py:7", "Blueprint('scales'")
with open('web_app/api/scales.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed scales.py - fix.py:10')

# Fix chords.py
with open('web_app/api/chords.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Blueprint('chords  chords.py:14' - fix.py:15", "Blueprint('chords'")
with open('web_app/api/chords.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed chords.py - fix.py:18')

# Fix progressions.py
with open('web_app/api/progressions.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Blueprint('progressions  progressions.py:14' - fix.py:23", "Blueprint('progressions'")
with open('web_app/api/progressions.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed progressions.py - fix.py:26')

# Fix analysis.py
with open('web_app/api/analysis.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("Blueprint('analysis  analysis.py:15' - fix.py:31", "Blueprint('analysis'")
with open('web_app/api/analysis.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed analysis.py - fix.py:34')

print('All done! - fix.py:36')
