calewith open('web_app/api/chords.py', 'rb') as f:
    data = f.read()

# Only fix the first occurrence at the very beginning of the file
# The problem is: """"\r\n followed by space
# This only affects the first docstring
first_triple_quote = data.find(b'"""')
if first_triple_quote != -1:
    # Find the newline after the first """
    search_start = first_triple_quote + 3
    # Look for \r\n followed by space
    pattern = b'"""\r\n '
    replacement = b'"""\r\n'
    data = data.replace(pattern, replacement, 1)  # Only first occurrence

with open('web_app/api/chords.py', 'wb') as f:
    f.write(data)

print('Fixed!')

