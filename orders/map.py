# importing googlemaps module
import googlemaps
import re


class get_delivery_price():
    def __init__(self,des):
        self.destination = des

    def get(self):
        # Requires API key
        gmaps = googlemaps.Client(key='AIzaSyDl91ZLUSOuh36T_Z3EXcrgnZVc8bBd-1Y')
        
        # Requires cities name
        my_dist = gmaps.distance_matrix('mutare CBD',self.destination)['rows'][0]['elements'][0]
        
        # Distance price
        dist = re.findall("\d+\.\d+", my_dist['distance']['text'])
        km = float(dist[0])
        print( float(km * 0.50))


get_delivery_price('harare').get()