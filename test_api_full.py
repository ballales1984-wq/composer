"""
Test API per Music Theory Engine Web App
Esegue test completi su tutti gli endpoint API.
"""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app.app import app


class TestAPI:
    """Test suite for API endpoints."""
    
    def __init__(self):
        self.app = app
        self.client = app.test_client()
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def run_test(self, name, method, endpoint, expected_status=200, data=None, headers=None):
        """Run a single API test."""
        try:
            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint, json=data, headers=headers)
            elif method == 'PUT':
                response = self.client.put(endpoint, json=data)
            elif method == 'DELETE':
                response = self.client.delete(endpoint)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code == expected_status
            
            if success:
                self.passed += 1
                status_icon = "✅"
            else:
                self.failed += 1
                status_icon = "❌"
            
            self.results.append({
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status': response.status_code,
                'expected': expected_status,
                'success': success,
                'icon': status_icon
            })
            
            return success, response
            
        except Exception as e:
            self.failed += 1
            self.results.append({
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status': 'ERROR',
                'expected': expected_status,
                'success': False,
                'icon': "❌",
                'error': str(e)
            })
            return False, None
    
    def print_results(self):
        """Print test results."""
        print("\n" + "=" * 70)
        print("📡 RISULTATI TEST API")
        print("=" * 70)
        
        for result in self.results:
            icon = result['icon']
            method = result['method']
            endpoint = result['endpoint']
            status = result['status']
            expected = result['expected']
            name = result['name']
            
            print(f"{icon} {name}")
            print(f"   {method} {endpoint}")
            print(f"   Status: {status} (expected: {expected})")
            
            if 'error' in result:
                print(f"   Error: {result['error']}")
            print()
        
        print("-" * 70)
        print(f"✅ Passati: {self.passed}")
        print(f"❌ Falliti: {self.failed}")
        print(f"📊 Totale: {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 Tutti i test sono passati!")
        else:
            print(f"\n⚠️ {self.failed} test falliti!")
        
        return self.failed == 0


def test_scales_api(tester):
    """Test Scales API endpoints."""
    print("\n🎼 Test Scales API...")
    
    # GET all scales
    tester.run_test(
        "Get scales list",
        "GET",
        "/api/scales",
        expected_status=200
    )
    
    # GET scale by root and type
    tester.run_test(
        "Get C Major scale",
        "GET",
        "/api/scales?root=C&type=major",
        expected_status=200
    )
    
    # GET scale list
    tester.run_test(
        "Get scale types list",
        "GET",
        "/api/scales/list",
        expected_status=200
    )
    
    # GET scale chords
    tester.run_test(
        "Get C Major scale chords",
        "GET",
        "/api/scales/chords?root=C&type=major",
        expected_status=200
    )
    
    # GET scale transpose
    tester.run_test(
        "Transpose C Major +2",
        "POST",
        "/api/scales/transpose",
        data={'root': 'C', 'type': 'major', 'semitones': 2},
        expected_status=200
    )
    
    # Test different scale types
    for scale_type in ['minor_natural', 'dorian', 'pentatonic_major', 'blues_minor']:
        tester.run_test(
            f"Get {scale_type} scale",
            "GET",
            f"/api/scales?root=G&type={scale_type}",
            expected_status=200
        )


def test_chords_api(tester):
    """Test Chords API endpoints."""
    print("\n🎸 Test Chords API...")
    
    # GET chord info
    tester.run_test(
        "Get Cmaj7 chord",
        "GET",
        "/api/chords?root=C&quality=maj7",
        expected_status=200
    )
    
    # GET chord list
    tester.run_test(
        "Get chord types list",
        "GET",
        "/api/chords",
        expected_status=200
    )
    
    # GET chord inversions
    tester.run_test(
        "Get Cmaj7 inversions",
        "GET",
        "/api/chords/inversions?root=C&quality=maj7",
        expected_status=200
    )
    
    # GET chord voicings
    tester.run_test(
        "Get Cmaj7 voicings",
        "GET",
        "/api/chords/voicing?root=C&quality=maj7",
        expected_status=200
    )
    
    # Test different chord qualities
    for quality in ['min', 'dom7', 'dim', 'aug', 'sus4']:
        tester.run_test(
            f"Get C{quality} chord",
            "GET",
            f"/api/chords?root=C&quality={quality}",
            expected_status=200
        )


def test_progressions_api(tester):
    """Test Progressions API endpoints."""
    print("\n🎶 Test Progressions API...")
    
    # POST create progression
    tester.run_test(
        "Create progression (POST)",
        "POST",
        "/api/progressions",
        data={'chords': ['C', 'F', 'G', 'C']},
        expected_status=200
    )
    
    # GET progressions list
    tester.run_test(
        "Get progressions list",
        "GET",
        "/api/progressions/list",
        expected_status=200
    )


def test_analysis_api(tester):
    """Test Analysis API endpoints."""
    print("\n📊 Test Analysis API...")
    
    # GET libraries status
    tester.run_test(
        "Get libraries status",
        "GET",
        "/api/analysis/libraries",
        expected_status=200
    )
    
    # GET key detection (uses query params, not POST)
    tester.run_test(
        "Detect key from C-E-G",
        "GET",
        "/api/analysis/key?notes=C&notes=E&notes=G",
        expected_status=200
    )
    
    # GET chord compatibility (uses query params)
    tester.run_test(
        "Check Cmaj7 compatibility with C Major",
        "GET",
        "/api/analysis/compatibility?scale=C%20Major&chord=C%20Major",
        expected_status=200
    )
    
    # GET progressions in key
    tester.run_test(
        "Get progressions in C Major",
        "GET",
        "/api/analysis/progressions?key=C%20Major&type=common",
        expected_status=200
    )


def test_circle_api(tester):
    """Test Circle of Fifths API endpoints."""
    print("\n🔵 Test Circle API...")
    
    # GET circle key
    tester.run_test(
        "Get Circle of Fifths for C",
        "GET",
        "/api/circle/key/C",
        expected_status=200
    )
    
    # GET circle neighbors
    tester.run_test(
        "Get neighbors of C",
        "GET",
        "/api/circle/neighbors/C",
        expected_status=200
    )


def test_analyzer_api(tester):
    """Test Real-time Analyzer API endpoints."""
    print("\n⚡ Test Analyzer API...")
    
    # POST realtime analyze
    tester.run_test(
        "Analyze C4-E4-G4",
        "POST",
        "/api/analyzer/realtime/analyze",
        data={'notes': ['C4', 'E4', 'G4']},
        expected_status=200
    )
    
    # POST chord detection
    tester.run_test(
        "Detect chord from C-E-G-B",
        "POST",
        "/api/analyzer/realtime/chord-detect",
        data={'notes': ['C4', 'E4', 'G4', 'B4']},
        expected_status=200
    )
    
    # POST scale suggestion
    tester.run_test(
        "Suggest scale for C-E-G",
        "POST",
        "/api/analyzer/realtime/scale-suggest",
        data={'notes': ['C4', 'E4', 'G4']},
        expected_status=200
    )


def test_orchestrator_api(tester):
    """Test Orchestrator API endpoints."""
    print("\n🎛️ Test Orchestrator API...")
    
    # POST suggest
    tester.run_test(
        "Suggest from input",
        "POST",
        "/api/orchestrator/suggest",
        data={'input': 'Cmaj7', 'genre': 'jazz', 'key': 'C'},
        expected_status=200
    )
    
    # POST expand
    tester.run_test(
        "Expand progression",
        "POST",
        "/api/orchestrator/expand",
        data={'chords': ['C', 'F', 'G'], 'target_length': 8},
        expected_status=200
    )
    
    # GET next chords
    tester.run_test(
        "Get next chords",
        "GET",
        "/api/orchestrator/next-chords?chord=Cmaj7&genre=jazz",
        expected_status=200
    )
    
    # GET compatible scales
    tester.run_test(
        "Get compatible scales",
        "GET",
        "/api/orchestrator/compatible-scales?chord=Cmaj7&genre=jazz",
        expected_status=200
    )
    
    # GET genre progressions
    tester.run_test(
        "Get jazz progressions",
        "GET",
        "/api/orchestrator/genre/progressions?genre=jazz",
        expected_status=200
    )


def test_routes(tester):
    """Test page routes."""
    print("\n📄 Test Routes...")
    
    routes = [
        ('Home', 'GET', '/'),
        ('Scales', 'GET', '/scales'),
        ('Chords', 'GET', '/chords'),
        ('Progressions', 'GET', '/progressions'),
        ('Fretboard', 'GET', '/fretboard'),
        ('About', 'GET', '/about'),
        ('Analyzer', 'GET', '/analyzer'),
        ('Realtime', 'GET', '/realtime'),
    ]
    
    for name, method, endpoint in routes:
        tester.run_test(
            f"Route {name}",
            method,
            endpoint,
            expected_status=200
        )


def run_all_tests():
    """Run all API tests."""
    print("=" * 70)
    print("🧪 MUSIC THEORY ENGINE - TEST SUITE")
    print("=" * 70)
    
    tester = TestAPI()
    
    # Run all test suites
    test_routes(tester)
    test_scales_api(tester)
    test_chords_api(tester)
    test_progressions_api(tester)
    test_analysis_api(tester)
    test_circle_api(tester)
    test_analyzer_api(tester)
    test_orchestrator_api(tester)
    
    # Print results
    success = tester.print_results()
    
    return success


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

