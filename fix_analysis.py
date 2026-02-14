# Fix script per analysis.py
with open('web_app/api/analysis.py', 'r') as f:
    content = f.read()

# Sostituisci il nome del blueprint
content = content.replace(
    "Blueprint('analysis  analysis.py:11' - fix_analysis.py:7",
    "Blueprint('analysis' - fix_analysis.py:8"
)

with open('web_app/api/analysis.py', 'w') as f:
    f.write(content)

print('Fix applicato! - fix_analysis.py:14')

