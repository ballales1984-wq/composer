"""Test API endpoints"""
from web_app.app import app

with app.test_client() as client:
    # Test orchestrator suggest
    r = client.post('/api/orchestrator/suggest', json={'input': 'Cmaj', 'genre': 'jazz', 'key': 'C'})
    print(f'POST /api/orchestrator/suggest: {r.status_code}')
    print(f'Response: {r.get_json()}')
