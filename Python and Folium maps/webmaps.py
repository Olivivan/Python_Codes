
import argparse
import json
import os
from statistics import mean

try:
	import folium
except Exception as e:
	raise SystemExit('Missing dependency: folium. Run `pip install folium`')


def load_data(path):
	path = os.path.abspath(path)
	if not os.path.exists(path):
		raise FileNotFoundError(path)

	if path.lower().endswith('.json'):
		with open(path, 'r', encoding='utf-8') as f:
			data = json.load(f)
			if isinstance(data, dict):
				# try to find a list inside the dict
				for v in data.values():
					if isinstance(v, list):
						data = v
						break
			if not isinstance(data, list):
				raise ValueError('JSON must contain a list of marker objects')
			return data

	# fallback: try to parse as newline-delimited simple JSON objects
	with open(path, 'r', encoding='utf-8') as f:
		lines = [line.strip() for line in f if line.strip()]
		try:
			return [json.loads(line) for line in lines]
		except Exception:
			raise ValueError('Unsupported data format for file: ' + path)


def get_lat_lon(item):
	# Try common keys for latitude/longitude
	for lat_key in ('lat', 'latitude', 'y'):
		for lon_key in ('lon', 'lng', 'longitude', 'x'):
			if lat_key in item and lon_key in item:
				try:
					return float(item[lat_key]), float(item[lon_key])
				except Exception:
					continue
	# try combined 'coords' or tuple
	if 'coords' in item and isinstance(item['coords'], (list, tuple)) and len(item['coords']) >= 2:
		return float(item['coords'][0]), float(item['coords'][1])
	raise KeyError('No lat/lon in item')


def make_map(markers, output='map.html', start_location=None, zoom_start=2, tiles='OpenStreetMap'):
	# Determine center
	if start_location is None:
		lats_lons = []
		for m in markers:
			try:
				lat, lon = get_lat_lon(m)
				lats_lons.append((lat, lon))
			except Exception:
				continue
		if lats_lons:
			center = (mean([p[0] for p in lats_lons]), mean([p[1] for p in lats_lons]))
		else:
			center = (0, 0)
	else:
		center = tuple(start_location)

	m = folium.Map(location=center, zoom_start=zoom_start, tiles=tiles)

	for item in markers:
		try:
			lat, lon = get_lat_lon(item)
		except Exception:
			continue
		name = item.get('name') or item.get('popup') or item.get('label') or item.get('title') or ''
		tooltip = item.get('tooltip') or name
		folium.CircleMarker(location=(lat, lon), radius=6, color='blue', fill=True, fill_opacity=0.7,
							popup=str(name), tooltip=str(tooltip)).add_to(m)

	m.save(output)
	return output


def sample_markers():
	return [
		{'name': 'New York, USA', 'lat': 40.7128, 'lon': -74.0060},
		{'name': 'London, UK', 'lat': 51.5074, 'lon': -0.1278},
		{'name': 'Tokyo, Japan', 'lat': 35.6895, 'lon': 139.6917},
	]


def main():
	parser = argparse.ArgumentParser(description='Generate an interactive web map (HTML) using Folium.')
	parser.add_argument('--data', '-d', help='Path to data file (JSON with list of objects having lat/lon).')
	parser.add_argument('--output', '-o', default='map.html', help='Output HTML file name')
	parser.add_argument('--tiles', default='OpenStreetMap', help='Tile set (default: OpenStreetMap)')
	parser.add_argument('--zoom', type=int, default=2, help='Initial zoom level')
	args = parser.parse_args()

	if args.data:
		markers = load_data(args.data)
	else:
		markers = sample_markers()

	out = make_map(markers, output=args.output, zoom_start=args.zoom, tiles=args.tiles)
	print('Map generated:', os.path.abspath(out))


if __name__ == '__main__':
	main()

