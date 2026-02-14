"""
Music Theory Engine - Web Application

Flask web app for exploring music theory concepts interactively.
"""

import os
import sys

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask, render_template, jsonify, request
from music_engine.models import Note, Chord, Scale, Progression
from music_engine.integrations import IntegrationFactory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'music-theory-secret-key-2024'

# Import API routes
from web_app.api import scales, chords, progressions, analysis, analyzer, orchestrator, circle

# Register blueprints
app.register_blueprint(scales.bp)
app.register_blueprint(chords.bp)
app.register_blueprint(progressions.bp)
app.register_blueprint(analysis.bp)
app.register_blueprint(analyzer.bp)
app.register_blueprint(orchestrator.bp)
app.register_blueprint(circle.bp)


@app.route('/')
def index():
    """Home page - dashboard."""
    return render_template('index.html')


@app.route('/scales')
def scales_page():
    """Scale explorer page."""
    return render_template('scales.html')


@app.route('/chords')
def chords_page():
    """Chord builder page."""
    return render_template('chords.html')


@app.route('/progressions')
def progressions_page():
    """Progression analyzer page."""
    return render_template('progressions.html')


@app.route('/fretboard')
def fretboard_page():
    """Fretboard visualization page."""
    return render_template('fretboard.html')


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/analyzer')
def analyzer_page():
    """Harmony analyzer page."""
    return render_template('analyzer.html')


@app.route('/realtime')
def realtime_page():
    """Real-time analysis page with virtual keyboard."""
    return render_template('realtime.html')


@app.route('/learn')
def learn_page():
    """Learn music theory page."""
    return render_template('learn.html')


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html', error="Server error"), 500


if __name__ == '__main__':
    print("🎵 Starting Music Theory Engine Web App... - app.py:80")
    print("Open your browser at: http://127.0.0.1:5000 - app.py:81")
    app.run(debug=True, host='127.0.0.1', port=5000)
