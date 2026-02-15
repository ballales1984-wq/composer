"""Test Chord Builder API endpoints"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_app.app import app

def test_chord_api():
    """Test all chord API endpoints"""
    print("=" * 60)
    print("Testing Chord Builder API Endpoints")
    print("=" * 60)
    
    with app.test_client() as client:
        # Test 1: Get basic chord info
        print("\n1. GET /api/chords?root=C&quality=maj")
        r = client.get('/api/chords?root=C&quality=maj')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
            print(f"   ✓ Intervals: {data['chord']['intervals']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 2: Get chord inversions
        print("\n2. GET /api/chords/inversions?root=C&quality=maj")
        r = client.get('/api/chords/inversions?root=C&quality=maj')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Inversions found: {len(data['inversions'])}")
            for inv in data['inversions']:
                print(f"     - Position {inv['position']}: {inv['notes']} (bass: {inv['bass']})")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 3: Get chord voicing
        print("\n3. GET /api/chords/voicing?root=C&quality=maj")
        r = client.get('/api/chords/voicing?root=C&quality=maj')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Voicing notes:")
            for v in data['voicing']:
                print(f"     - {v['note']} (octave {v['octave']})")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 4: Get minor chord
        print("\n4. GET /api/chords?root=C&quality=min")
        r = client.get('/api/chords?root=C&quality=min')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
            print(f"   ✓ Semitones: {data['chord']['semitones']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 5: Get dominant 7th chord
        print("\n5. GET /api/chords?root=G&quality=dom7")
        r = client.get('/api/chords?root=G&quality=dom7')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 6: Get diminished chord
        print("\n6. GET /api/chords?root=B&quality=dim")
        r = client.get('/api/chords?root=B&quality=dim')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 7: Get augmented chord
        print("\n7. GET /api/chords?root=C&quality=aug")
        r = client.get('/api/chords?root=C&quality=aug')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 8: Get chord with sharp root
        print("\n8. GET /api/chords?root=F#&quality=maj7")
        r = client.get('/api/chords?root=F#&quality=maj7')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Notes: {data['chord']['notes']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 9: Get chord positions (fretboard)
        print("\n9. GET /api/chords/positions?root=C&quality=maj")
        r = client.get('/api/chords/positions?root=C&quality=maj')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Chord: {data['chord']['name']}")
            print(f"   ✓ Voicings: {len(data.get('voicings', []))}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
        
        # Test 10: List chord qualities
        print("\n10. GET /api/chords/list")
        r = client.get('/api/chords/list')
        print(f"   Status: {r.status_code}")
        data = r.get_json()
        if data.get('success'):
            print(f"   ✓ Qualities: {len(data['qualities'])}")
            for q in data['qualities']:
                print(f"     - {q['id']}: {q['name']}")
        else:
            print(f"   ✗ Error: {data.get('error')}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_chord_api()

