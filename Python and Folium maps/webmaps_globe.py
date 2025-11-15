from flask import Flask, send_from_directory, jsonify, render_template_string
import os
import json

# Simple Flask app to serve a static HTML globe and marker data
APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)


@app.route('/')
def index():
    # Serve the static HTML file
    return send_from_directory(STATIC_DIR, 'map_globe.html')


@app.route('/data')
def data():
    # Return the sample markers JSON
    path = os.path.join(STATIC_DIR, 'markers.json')
    if not os.path.exists(path):
        return jsonify([])
    with open(path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


if __name__ == '__main__':
    print('Starting Flask server. Open http://127.0.0.1:5000 in your browser')
    app.run(host='0.0.0.0', port=5000, debug=True)
