"""
build_world_cities.py

Small helper to download the GeoNames cities dump and convert to JSON in the format
[{"name":..., "lat":..., "lon":..., "desc":...}, ...]

Usage (PowerShell):
  python build_world_cities.py --out static/world_cities.json --source cities500

Notes:
- This script downloads the specified GeoNames cities file (e.g. cities500.zip or cities15000.zip)
  from download.geonames.org and converts it. The resulting JSON can be large.
"""

import argparse
import json
import os
import zipfile
from urllib.request import urlopen
from io import BytesIO, TextIOWrapper


GEONAMES_BASE = 'https://download.geonames.org/export/dump'


def download_and_extract(filename):
    url = GEONAMES_BASE + '/' + filename + '.zip'
    print('Downloading', url)
    resp = urlopen(url)
    z = zipfile.ZipFile(BytesIO(resp.read()))
    # expect a file named filename (without .zip)
    inner_name = filename
    if inner_name not in z.namelist():
        # pick the first txt file
        for n in z.namelist():
            if n.lower().endswith('.txt'):
                inner_name = n
                break
    print('Extracting', inner_name)
    return TextIOWrapper(z.open(inner_name), encoding='utf-8', errors='replace')


def convert_geonames_stream(f, out_path):
    # GeoNames columns (tab-separated):
    # geonameid name asciiname alternatenames latitude longitude feature class ... country code ... population ... timezone ...
    # We'll parse name (1), latitude (4), longitude (5), country code (8), population (14)
    out = open(out_path, 'w', encoding='utf-8')
    out.write('[')
    first = True
    for line in f:
        if not line.strip():
            continue
        parts = line.strip().split('\t')
        try:
            name = parts[1]
            lat = float(parts[4])
            lon = float(parts[5])
            country = parts[8] if len(parts) > 8 else ''
            population = parts[14] if len(parts) > 14 else ''
            desc = f'{country} population:{population}'
            obj = {"name": name, "lat": lat, "lon": lon, "desc": desc}
            if not first:
                out.write(',\n')
            out.write(json.dumps(obj, ensure_ascii=False))
            first = False
        except Exception:
            continue
    out.write(']\n')
    out.close()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source', default='cities500', help='GeoNames base filename (cities500, cities15000, etc)')
    p.add_argument('--out', default='static/world_cities.json', help='Output JSON path')
    args = p.parse_args()

    f = download_and_extract(args.source)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    convert_geonames_stream(f, args.out)
    print('Wrote', args.out)


if __name__ == '__main__':
    main()
