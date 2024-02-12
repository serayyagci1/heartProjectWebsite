import plotly.express as px
import json

# Load the GeoJSON data
with open('merged.geojson') as geojson_file:
    geojson_data = json.load(geojson_file)

# Convert 'HeartDiseasePercentage' values to floats
for feature in geojson_data['features']:
    percentage_str = feature['properties'].get('HeartDiseasePercentage', None)
    try:
        percentage_float = float(percentage_str)
        feature['properties']['HeartDiseasePercentage'] = percentage_float
    except (TypeError, ValueError):
        feature['properties']['HeartDiseasePercentage'] = None

# Extract information from each feature
locations = [feature['properties']['NAME'] for feature in geojson_data['features']]
hover_names = [feature['properties']['NAME'] for feature in geojson_data['features']]
color_values = [feature['properties']['HeartDiseasePercentage'] for feature in geojson_data['features']]

# Create a choropleth map
fig = px.choropleth(geojson_data, 
                    geojson=geojson_data,  # Provide the GeoJSON data explicitly
                    locations=locations,  # Extract state names
                    featureidkey="properties.NAME",  # Specify the key to match the GeoJSON features with the locations
                    color=color_values,  # Extract heart disease percentages
                    hover_name=hover_names,  # Extract state names for hover
                    color_continuous_scale="reds",  # Use a red color scale
                    title='Heart Disease Percentage by State')

# Show the map
fig.update_geos(fitbounds="locations", visible=False)
fig.show()
