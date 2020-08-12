import mytools
import json
lon = 114.42393
lat =  30.395188
dis = 501
fawei = 45
print(mytools.geojson_tools.destination_point2(lon,lat, fawei, dis))
# destination_point()
#{'type': 'Point', 'coordinates': [-122.26000070571902, 19.822758489812447]}