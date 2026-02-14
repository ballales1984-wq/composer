# Leggi analysis_fixed.py
with open('web_app/api/analysis_fixed.py', 'r') as f:
    content_fixed = f.read()

# Leggi analysis.py
with open('web_app/api/analysis.py', 'r') as f:
    content_analysis = f.read()

# Mostra il contenuto di analysis_fixed.py
print("=== analysis_fixed.py === - read_files.py:10")
print(content_fixed)
print("\n\n=== analysis.py === - read_files.py:12")
print(content_analysis)

