# importing googlemaps module
import googlemaps
import re

def get_cost(point):
    # Requires API key
    try:
        gmaps = googlemaps.Client(key='AIzaSyDl91ZLUSOuh36T_Z3EXcrgnZVc8bBd-1Y')
            
        # Requires cities name
        my_dist = gmaps.distance_matrix('mutare CBD',point)['rows'][0]['elements'][0]
            
        # Distance price
        dist = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", my_dist['distance']['text'])
        km = float(dist[0])
        return km * 0.50
    except:
        pass