from flask import Flask, send_from_directory, jsonify, request
import os
import json

# Simple Flask app to serve a static HTML globe and marker data + search
APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')

app = Flask(__name__, static_folder=STATIC_DIR)

# Try to load a world cities JSON (if present). This file may be large; if it's missing
# the app will fall back to `markers.json` for demo data.
WORLD_CITIES = None
WORLD_CITIES_PATH = os.path.join(STATIC_DIR, 'world_cities.json')
if os.path.exists(WORLD_CITIES_PATH):
    try:
        with open(WORLD_CITIES_PATH, 'r', encoding='utf-8') as f:
            WORLD_CITIES = json.load(f)
            # ensure lowercase indexing for fast search
            for c in WORLD_CITIES:
                c['_lc'] = (c.get('name','') + ' ' + c.get('desc','')).lower()
            print(f'Loaded {len(WORLD_CITIES)} world cities')
    except Exception as e:
        print('Failed to load world_cities.json:', e)


@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'map_globe.html')


@app.route('/data')
def data():
    # Return the full world cities if available, else the sample markers.json
    if WORLD_CITIES is not None:
        return jsonify(WORLD_CITIES)
    path = os.path.join(STATIC_DIR, 'markers.json')
    if not os.path.exists(path):
        return jsonify([])
    with open(path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))


@app.route('/search')
def search():
    # Server-side search for city names. Query param: q
    q = (request.args.get('q') or '').strip().lower()
    if not q:
        return jsonify([])

    # Prefer searching WORLD_CITIES if available
    source = WORLD_CITIES
    if source is None:
        # fallback to markers.json
        p = os.path.join(STATIC_DIR, 'markers.json')
        if not os.path.exists(p):
            return jsonify([])
        with open(p, 'r', encoding='utf-8') as f:
            source = json.load(f)
            for c in source:
                c['_lc'] = (c.get('name','') + ' ' + c.get('desc','')).lower()

    results = []
    # simple substring match on name/desc
    for item in source:
        if q in item.get('_lc',''):
            results.append({
                'name': item.get('name'),
                'lat': item.get('lat'),
                'lon': item.get('lon'),
                'desc': item.get('desc', '')
            })
        if len(results) >= 50:
            break

    return jsonify(results)


if __name__ == '__main__':
    print('Starting Flask server. Open http://127.0.0.1:5000 in your browser')
    # turn off the reloader by default to avoid restarts while testing; set debug True only if desired
    app.run(host='0.0.0.0', port=5000, debug=False)
