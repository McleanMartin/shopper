

# importing googlemaps module
import googlemaps
import re
 
# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDl91ZLUSOuh36T_Z3EXcrgnZVc8bBd-1Y')
 
# Requires cities name
my_dist = gmaps.distance_matrix('mutare CBD','greenside,mutare')['rows'][0]['elements'][0]
 
# Printing the result
print(my_dist['distance']['text'])
dist = re.findall("\d+\.\d+", my_dist['distance']['text'])
print( f' The distance is {float(dist[0])} KM')
