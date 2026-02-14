# Fix blueprint names
files = [
    'web_app/api/scales.py',
    'web_app/api/chords.py', 
    'web_app/api/progressions.py',
    'web_app/api/analysis.py'
]

for f in files:
    try:
        with open(f, 'r') as file:
            content = file.read()
        
        # Replace any blueprint name with dot
        import re
        content = re.sub(r"Blueprint\('[^']*  [^']*:\d+' - fix_bp_names.py:16", "Blueprint('fixed'", content)
        
        with open(f, 'w') as file:
            file.write(f"Fixed {f}")
    except Exception as e:
        print(f"Error in {f}: {e} - fix_bp_names.py:21")

