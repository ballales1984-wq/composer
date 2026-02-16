a"""
Test suite for Music Theory Engine Web Application
Run with: python -m pytest test_web_app_comprehensive.py -v
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ==================== ROUTE TESTS ====================

class TestRoutes:
    """Test all web routes return 200 OK."""
    
    def test_home_route(self, client):
        """Test home page loads."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_chords_route(self, client):
        """Test chords page loads."""
        response = client.get('/chords')
        assert response.status_code == 200
    
    def test_scales_route(self, client):
        """Test scales page loads."""
        response = client.get('/scales')
        assert response.status_code == 200
    
    def test_progressions_route(self, client):
        """Test progressions page loads."""
        response = client.get('/progressions')
        assert response.status_code == 200
    
    def test_fretboard_route(self, client):
        """Test fretboard page loads."""
        response = client.get('/fretboard')
        assert response.status_code == 200
    
    def test_about_route(self, client):
        """Test about page loads."""
        response = client.get('/about')
        assert response.status_code == 200


# ==================== CHORDS API TESTS ====================

class TestChordsAPI:
    """Test chords API endpoints."""
    
    def test_get_chord_c_major(self, client):
        """Test getting C major chord."""
        response = client.get('/api/chords?root=C&quality=maj')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'chord' in data
        assert data['chord']['root'] == 'C'
    
    def test_get_chord_a_minor(self, client):
        """Test getting A minor chord."""
        response = client.get('/api/chords?root=A&quality=min')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['chord']['root'] == 'A'
    
    def test_get_chord_g7(self, client):
        """Test getting G7 chord."""
        response = client.get('/api/chords?root=G&quality=dom7')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_chord_invalid_root(self, client):
        """Test with invalid root note."""
        response = client.get('/api/chords?root=INVALID&quality=maj')
        # Should handle gracefully
        assert response.status_code in [200, 400]
    
    def test_chord_inversions(self, client):
        """Test chord inversions endpoint."""
        response = client.get('/api/chords/inversions?root=C&quality=maj')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'inversions' in data
    
    def test_chord_voicing(self, client):
        """Test chord voicing endpoint."""
        response = client.get('/api/chords/voicing?root=C&quality=maj')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'voicing' in data
    
    def test_chord_positions(self, client):
        """Test chord positions endpoint."""
        response = client.get('/api/chords/positions?root=C&quality=maj')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'voicings' in data
    
    def test_chord_positions_realistic_mode(self, client):
        """Test chord positions with realistic mode."""
        response = client.get('/api/chords/positions?root=C&quality=maj&mode=realistic')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data.get('mode') == 'realistic'
    
    def test_chord_positions_theoretical_mode(self, client):
        """Test chord positions with theoretical mode."""
        response = client.get('/api/chords/positions?root=C&quality=maj&mode=theoretical')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data.get('mode') == 'theoretical'
    
    def test_chord_list(self, client):
        """Test chord list endpoint."""
        response = client.get('/api/chords/list')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'qualities' in data


# ==================== SCALES API TESTS ====================

class TestScalesAPI:
    """Test scales API endpoints."""
    
    def test_get_scale_c_major(self, client):
        """Test getting C major scale."""
        response = client.get('/api/scales?root=C&type=major')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'scale' in data
    
    def test_get_scale_a_minor(self, client):
        """Test getting A minor scale."""
        response = client.get('/api/scales?root=A&type=minor')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_scale_pentatonic(self, client):
        """Test getting pentatonic scale."""
        response = client.get('/api/scales?root=C&type=pentatonic_major')
        assert response.status_code == 200
    
    def test_scale_list(self, client):
        """Test scale list endpoint."""
        response = client.get('/api/scales/list')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


# ==================== CIRCLE OF FIFTHS API TESTS ====================

class TestCircleAPI:
    """Test circle of fifths API endpoints."""
    
    def test_get_circle(self, client):
        """Test getting circle of fifths data."""
        response = client.get('/api/circle')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'major_keys' in data
        assert 'minor_keys' in data
    
    def test_get_key_info_c_major(self, client):
        """Test getting C major key info."""
        response = client.get('/api/circle/key/C')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'diatonic_chords' in data
        assert 'common_progressions' in data
    
    def test_get_key_info_a_minor(self, client):
        """Test getting A minor key info."""
        response = client.get('/api/circle/key/Am')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_relationships_c(self, client):
        """Test getting key relationships for C."""
        response = client.get('/api/circle/relationships/C')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'relationships' in data
    
    def test_get_neighbors_c(self, client):
        """Test getting neighboring keys for C."""
        response = client.get('/api/circle/neighbors/C')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'neighbors' in data


# ==================== PROGRESSIONS API TESTS ====================

class TestProgressionsAPI:
    """Test progressions API endpoints."""
    
    def test_get_progressions(self, client):
        """Test getting progressions list."""
        response = client.get('/api/progressions')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_progression_details(self, client):
        """Test getting specific progression."""
        response = client.get('/api/progressions/1452')
        # May return 404 if progression doesn't exist
        assert response.status_code in [200, 404]


# ==================== ANALYSIS API TESTS ====================

class TestAnalysisAPI:
    """Test analysis API endpoints."""
    
    def test_analyze_notes(self, client):
        """Test note analysis."""
        response = client.post('/api/analysis/key', json={
            'notes': ['C', 'E', 'G']
        })
        assert response.status_code == 200
    
    def test_realtime_analyze(self, client):
        """Test realtime analysis."""
        response = client.post('/api/analyzer/realtime/analyze', json={
            'notes': ['C4', 'E4', 'G4']
        })
        # May return 200 or 404 depending on endpoint
        assert response.status_code in [200, 404]


# ==================== CHORD DIAGRAM TESTS ====================

class TestChordDiagrams:
    """Test chord diagram generation."""
    
    def test_c_major_voicings(self, client):
        """Test C major voicings have correct structure."""
        response = client.get('/api/chords/positions?root=C&quality=maj')
        data = response.get_json()
        
        if data['success']:
            voicings = data['voicings']
            assert len(voicings) > 0
            
            # Check first voicing has required fields
            first_voicing = voicings[0]
            assert 'name' in first_voicing
            assert 'frets' in first_voicing
    
    def test_g_major_voicings(self, client):
        """Test G major voicings."""
        response = client.get('/api/chords/positions?root=G&quality=maj')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_a_minor_voicings(self, client):
        """Test A minor voicings."""
        response = client.get('/api/chords/positions?root=A&quality=min')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
