```markdown
***In this repository you will find some .py codes.***

```

**Web Map**
- **Purpose:** Generate an interactive HTML map using `folium` from Python.
- **Script:** `Python and Folium maps\\webmaps.py` — creates `map.html` by default.
- **Install:** Create a virtual environment and install dependencies:

```powershell
python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1; pip install -r "Python and Folium maps\\requirements.txt"
```
- **Run:** Examples (from repository root):

```powershell
# Generate sample map
python "Python and Folium maps\\webmaps.py"

# Generate map from JSON file (file must be a list of objects with lat/lon keys)
python "Python and Folium maps\\webmaps.py" --data "path\\to\\your\\markers.json" --output "my_map.html"
```

- **Notes:** The script accepts JSON files containing a list of objects with common latitude/longitude keys such as `lat`/`lon`, `latitude`/`longitude`, or a `coords` list/tuple.
***In this repository you will find some .py codes.***
