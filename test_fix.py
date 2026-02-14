import sys
sys.path.insert(0, '.')
from music_engine.models import Progression

# Test
p = Progression(['C', 'G', 'C'])
scales = p.get_compatible_scales()
print(f"Compatible scales: {len(scales)}")
for s in scales[:3]:
    print(f"  - {s}")

sugs = p.get_scale_suggestions(3)
print(f"Suggestions: {len(sugs)}")
for s in sugs:
    print(f"  - {s}")
