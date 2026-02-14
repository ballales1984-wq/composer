# Script per copiare analysis_new.py su analysis.py
import shutil

# Copia analysis_new.py su analysis.py
shutil.copy('web_app/api/analysis_new.py', 'web_app/api/analysis.py')

print("File copiato con successo! - copy_file.py:7")

