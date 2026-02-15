Port binding
Every Render web service must bind to a port on host 0.0.0.0 to serve HTTP requests. Render forwards inbound requests to your web service at this port (it is not directly reachable via the public internet).

We recommend binding your HTTP server to the port defined by the PORT environment variable. Here's a basic Express example:

Copy to clipboard
const express = require('express')
const app = express()
const port = process.env.PORT || 4000 

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
Adapted ever-so-slightly from here

The default value of PORT is 10000 for all Render web services. You can override this value by setting the environment variable for your service in the Render Dashboard.

If you bind your HTTP server to a different port, Render is usually able to detect and use it.

If Render fails to detect a bound port, your web service's deploy fails and displays an error in your logs.

The following ports are reserved by Render and cannot be used:

18012
18013
19099
Binding to multiple ports
Render forwards inbound traffic to only one HTTP port per web service. However, your web service can bind to additional ports to receive traffic over your private network.

If your service does bind to multiple ports, always bind your public HTTP server to the value of the PORT environment variable.

Connect to your web service
Connecting from the public internet
Your web service is reachable via the public internet at its onrender.com subdomain (along with any custom domains you add).

If you don't want your service to be reachable via the public internet, create a private service instead of a web service.

Render's load balancer terminates SSL for inbound HTTPS requests, then forwards those requests to your web service over HTTP. If an inbound request uses HTTP, Render first redirects it to HTTPS and then terminates SSL for it.

Connecting from other Render services
See Private Network.

Additional features
Render web services also support the following capabilities:

Zero-downtime deploys
Free, fully-managed TLS certificates
Custom domains (including wildcards)
Manual or automatic scaling
Persistent disks
Edge caching for static assets
WebSocket connections
Service previews
Instant rollbacks
Maintenance mode
HTTP/2
DDoS protection
Brotli compression
Support for Blueprints, Render's Infrastructure-as-Code modelimport os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import music_engine
from music_engine.core import scales, chords, harmony
from music_engine.models import Scale, Chord, Progression
from music_engine.integrations.music21_adapter import Music21Adapter
from music_engine.integrations.mingus_adapter import MingusAdapter

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')
CORS(app)

# Configure folders
app.config['MUSIC_ENGINE_DIR'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['PRESETS_DIR'] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'presets')

# Import blueprints
from api.scales import scales_bp
from api.chords import chords_bp
from api.progressions import progressions_bp
from api.analysis import analysis_bp
from api.circle import circle_bp
from api.midi import midi_bp
from api.orchestrator import orchestrator_bp

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

