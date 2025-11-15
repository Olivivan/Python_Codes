import folium
from folium.plugins import Search
import json

# Create a base map centered on a location (e.g., New York City)
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add different tile layers
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('Stamen Terrain', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('Stamen Toner', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('Stamen Watercolor', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('CartoDB positron').add_to(m)
folium.TileLayer('CartoDB dark_matter').add_to(m)

# Add a layer control
folium.LayerControl().add_to(m)

# Add some sample markers
folium.Marker([40.7128, -74.0060], popup='New York City').add_to(m)
folium.Marker([40.7589, -73.9851], popup='Times Square').add_to(m)
folium.Marker([40.7505, -73.9934], popup='Empire State Building').add_to(m)

# Create a GeoJSON feature collection for search
features = [
    {
        "type": "Feature",
        "properties": {"name": "New York City"},
        "geometry": {"type": "Point", "coordinates": [-74.0060, 40.7128]}
    },
    {
        "type": "Feature",
        "properties": {"name": "Times Square"},
        "geometry": {"type": "Point", "coordinates": [-73.9851, 40.7589]}
    },
    {
        "type": "Feature",
        "properties": {"name": "Empire State Building"},
        "geometry": {"type": "Point", "coordinates": [-73.9934, 40.7505]}
    }
]

geojson_data = {"type": "FeatureCollection", "features": features}

# Add search functionality
Search(
    layer=folium.GeoJson(geojson_data, name="Locations").add_to(m),
    geom_type='Point',
    placeholder="Search for a location",
    collapsed=False,
    search_label='name'
).add_to(m)

# Save the map
m.save('D:/Python_Codes/Python and Folium maps/map.html')
print("Map saved as map.html")
