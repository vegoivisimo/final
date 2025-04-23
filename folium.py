import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians

# Load the dataset
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
spacex_df = pd.read_csv(url)


spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]


nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)


for index, site in launch_sites_df.iterrows():
    coordinate = [site['Lat'], site['Long']]
    # Add a circle
    folium.Circle(
        coordinate,
        radius=1000,
        color='#d35400',
        fill=True
    ).add_child(folium.Popup(site['Launch Site'])).add_to(site_map)
    # Add a marker with label
    folium.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site['Launch Site']
        )
    ).add_to(site_map)



spacex_df['marker_color'] = spacex_df['class'].apply(lambda x: 'green' if x == 1 else 'red')

marker_cluster = MarkerCluster().add_to(site_map)


for index, record in spacex_df.iterrows():
    coordinate = [record['Lat'], record['Long']]
    marker = folium.Marker(
        coordinate,
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter
)
site_map.add_child(mouse_position)


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0  # Earth's radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


launch_site = launch_sites_df[launch_sites_df['Launch Site'] == 'CCAFS SLC-40'].iloc[0]
launch_site_lat = launch_site['Lat']
launch_site_lon = launch_site['Long']
coastline_lat = 28.56367  
coastline_lon = -80.57163
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

coastline_coordinate = [coastline_lat, coastline_lon]
distance_marker = folium.Marker(
    coastline_coordinate,
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline)
    )
)
site_map.add_child(distance_marker)


lines = folium.PolyLine(locations=[(launch_site_lat, launch_site_lon), (coastline_lat, coastline_lon)], weight=1)
site_map.add_child(lines)


site_map.save('spacex_launch_map.html')
print("Map saved as 'spacex_launch_map.html'. Open it in a web browser to view.")