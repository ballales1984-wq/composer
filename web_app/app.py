import os
import sys

# Add web_app directory to path for API imports
web_app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, web_app_dir)

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import music_engine
from music_engine.core import scales, chords, harmony
from music_engine.models import Scale, Chord, Progression

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')
CORS(app)

# Configure folders
app.config['MUSIC_ENGINE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['PRESETS_DIR'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'presets')

# Import blueprints
from api.scales import bp as scales_bp
from api.chords import bp as chords_bp
from api.progressions import bp as progressions_bp
from api.analysis import bp as analysis_bp
from api.circle import bp as circle_bp
from api.midi import bp as midi_bp
from api.orchestrator import bp as orchestrator_bp

# Register blueprints
app.register_blueprint(scales_bp, url_prefix='/api')
app.register_blueprint(chords_bp, url_prefix='/api')
app.register_blueprint(progressions_bp, url_prefix='/api')
app.register_blueprint(analysis_bp, url_prefix='/api')
app.register_blueprint(circle_bp, url_prefix='/api')
app.register_blueprint(midi_bp, url_prefix='/api')
app.register_blueprint(orchestrator_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fretboard')
def fretboard():
    return render_template('fretboard.html')

@app.route('/scales')
def scales_page():
    return render_template('scales.html')

@app.route('/chords')
def chords_page():
    return render_template('chords.html')

@app.route('/progressions')
def progressions_page():
    return render_template('progressions.html')

@app.route('/analyzer')
def analyzer():
    return render_template('analyzer.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=404, message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error=500, message="Internal server error"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

