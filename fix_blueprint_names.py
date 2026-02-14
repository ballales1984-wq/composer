import os
import re

api_dir = r"c:\Users\user\composer\web_app\api"

files = ['scales.py', 'chords.py', 'progressions.py', 'analysis.py']

for f in files:
    path = os.path.join(api_dir, f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace patterns like "scales - fix_api.py:21" with "scales"
        new_content = re.sub(r'scales - \w+:\d+', 'scales', content)
        new_content = re.sub(r'chords - \w+:\d+', 'chords', new_content)
        new_content = re.sub(r'progressions - \w+:\d+', 'progressions', new_content)
        new_content = re.sub(r'analysis - \w+:\d+', 'analysis', new_content)
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"Fixed {f} - fix_blueprint_names.py:23")

print("Done! - fix_blueprint_names.py:25")

