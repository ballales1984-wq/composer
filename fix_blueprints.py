import re
import os

api_dir = 'c:/Users/user/composer/web_app/api'

# Fix scales.py
with open(os.path.join(api_dir, 'scales.py'), 'r') as f:
    content = f.read()
content = content.replace("Blueprint('scales  scales.py:14', __name__ - fix_blueprints.py:9", "Blueprint('scales', __name__")
with open(os.path.join(api_dir, 'scales.py'), 'w') as f:
    f.write(content)
print('Fixed scales.py - fix_blueprints.py:12')

# Fix chords.py  
with open(os.path.join(api_dir, 'chords.py'), 'r') as f:
    content = f.read()
content = content.replace("Blueprint('chords  chords.py:14', __name__ - fix_blueprints.py:17", "Blueprint('chords', __name__")
with open(os.path.join(api_dir, 'chords.py'), 'w') as f:
    f.write(content)
print('Fixed chords.py - fix_blueprints.py:20')

# Fix progressions.py
with open(os.path.join(api_dir, 'progressions.py'), 'r') as f:
    content = f.read()
content = content.replace("Blueprint('progressions  progressions.py:14', __name__ - fix_blueprints.py:25", "Blueprint('progressions', __name__")
with open(os.path.join(api_dir, 'progressions.py'), 'w') as f:
    f.write(content)
print('Fixed progressions.py - fix_blueprints.py:28')

# Fix analysis.py
with open(os.path.join(api_dir, 'analysis.py'), 'r') as f:
    content = f.read()
content = content.replace("Blueprint('analysis  analysis.py:15', __name__ - fix_blueprints.py:33", "Blueprint('analysis', __name__")
with open(os.path.join(api_dir, 'analysis.py'), 'w') as f:
    f.write(content)
print('Fixed analysis.py - fix_blueprints.py:36')

print('All API files fixed! - fix_blueprints.py:38')

