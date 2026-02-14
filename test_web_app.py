"""
Test and Debug Script for Music Theory Engine Web App
Run this script to test the API endpoints and verify everything works.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app.app import app

def test_routes():
    """Test all routes and API endpoints."""
    print("=" * 60)
    print("🧪 TESTING MUSIC THEORY ENGINE WEB APP")
    print("=" * 60)
    
    client = app.test_client()
    
    # Test main routes
    routes = [
        ('/', 'Home'),
        ('/scales', 'Scales'),
        ('/chords', 'Chords'),
        ('/progressions', 'Progressions'),
        ('/fretboard', 'Fretboard'),
        ('/about', 'About'),
        ('/analyzer', 'Analyzer'),
        ('/realtime', 'Real-time'),
    ]
    
    print("\n📄 Testing Routes:")
    print("-" * 40)
    
    for route, name in routes:
        response = client.get(route)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"  {status} {name:15} -> {route} ({response.status_code})")
    
    # Test API endpoints (with correct query parameters)
    print("\n🔌 Testing API Endpoints:")
    print("-" * 40)
    
    api_tests = [
        ('/api/scales', 'GET', None),
        ('/api/scales?root=C&type=major', 'GET', None),
        ('/api/scales/list', 'GET', None),
        ('/api/scales/chords?root=C&type=major', 'GET', None),
        ('/api/chords', 'GET', None),
        ('/api/chords?root=C&quality=maj7', 'GET', None),
        ('/api/progressions', 'GET', None),
        ('/api/analysis/key', 'POST', {'notes': ['C', 'E', 'G']}),
        ('/api/analyzer/realtime/analyze', 'POST', {'notes': ['C4', 'E4', 'G4']}),
    ]
    
    for endpoint, method, data in api_tests:
        if method == 'GET':
            response = client.get(endpoint)
        else:
            response = client.post(endpoint, json=data)
        
        status = "✅" if response.status_code == 200 else "❌"
        print(f"  {status} {method:4} {endpoint} -> {response.status_code}")
        
        # Print error details for failed requests
        if response.status_code != 200:
            print(f"       Error: {response.data[:200]}")

def test_models():
    """Test the music engine models directly."""
    print("\n🎵 Testing Music Engine Models:")
    print("-" * 40)
    
    from music_engine.models import Note, Chord, Scale, Progression
    
    # Test Note
    try:
        note = Note("C4")
        print(f"  ✅ Note: {note.name} = {note.frequency}Hz (MIDI: {note.midi})")
    except Exception as e:
        print(f"  ❌ Note Error: {e}")
    
    # Test Chord (root, quality - separate arguments!)
    try:
        chord = Chord("C", "maj7")  # Fixed: use separate args
        print(f"  ✅ Chord: {chord.name} -> Notes: {chord.note_names}")
    except Exception as e:
        print(f"  ❌ Chord Error: {e}")
    
    # Test Chord - minor
    try:
        chord_min = Chord("A", "min7")  # Minor 7 chord
        print(f"  ✅ Chord: {chord_min.name} -> Notes: {chord_min.note_names}")
    except Exception as e:
        print(f"  ❌ Chord Error: {e}")
    
    # Test Scale
    try:
        scale = Scale("C", "major")
        print(f"  ✅ Scale: {scale.name} -> Notes: {[n.name for n in scale.notes]}")
    except Exception as e:
        print(f"  ❌ Scale Error: {e}")
    
    # Test Progression (fixed chord creation)
    try:
        prog = Progression([
            Chord("C", "maj"), 
            Chord("F", "maj"), 
            Chord("G", "dom7"), 
            Chord("C", "maj")
        ])
        print(f"  ✅ Progression: {prog.name} -> {[c.name for c in prog.chords]}")
    except Exception as e:
        print(f"  ❌ Progression Error: {e}")

def test_integrations():
    """Test integration libraries."""
    print("\n🔗 Testing Integrations:")
    print("-" * 40)
    
    from music_engine.integrations import is_library_available, get_available_libraries
    
    libraries = get_available_libraries()
    print(f"  📚 Available libraries: {libraries}")
    
    for lib in ['music21', 'mingus']:
        available = is_library_available(lib)
        status = "✅" if available else "❌"
        print(f"  {status} {lib}: {'Available' if available else 'Not installed'}")

def test_api_detailed():
    """Test API in detail."""
    print("\n📡 Testing API Detailed:")
    print("-" * 40)
    
    client = app.test_client()
    
    # Test scales API
    response = client.get('/api/scales?root=C&type=major')
    if response.status_code == 200:
        import json
        data = json.loads(response.data)
        if data.get('success'):
            scale_info = data.get('scale', {})
            print(f"  ✅ Scale: {scale_info.get('name')}")
            print(f"      Notes: {scale_info.get('notes')}")
        else:
            print(f"  ❌ API Error: {data.get('error')}")
    else:
        print(f"  ❌ HTTP Error: {response.status_code}")
    
    # Test chords API
    response = client.get('/api/chords?root=C&quality=maj7')
    if response.status_code == 200:
        import json
        data = json.loads(response.data)
        if data.get('success'):
            chord_info = data.get('chord', {})
            print(f"  ✅ Chord: {chord_info.get('name')}")
            print(f"      Notes: {chord_info.get('notes')}")
        else:
            print(f"  ❌ API Error: {data.get('error')}")
    else:
        print(f"  ❌ HTTP Error: {response.status_code}")

if __name__ == '__main__':
    test_routes()
    test_models()
    test_integrations()
    test_api_detailed()
    
    print("\n" + "=" * 60)
    print("✅ TESTING COMPLETE!")
    print("=" * 60)
    print("\nTo run the web app, execute:")
    print("  python web_app/app.py")
    print("\nThen open your browser at: http://127.0.0.1:5000")

