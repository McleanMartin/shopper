# importing googlemaps module
import googlemaps
import re
from paynow import Paynow

paynow = Paynow(
    '14813',
    '3e688baf-5630-4145-a99c-d5deb32e5b2e',
    'https://google.com',
    'http://127.0.0.1:8000'
)
 
# Requires API key
gmaps = googlemaps.Client(key='AIzaSyDl91ZLUSOuh36T_Z3EXcrgnZVc8bBd-1Y')
 
point = 'dangamvura'
# Requires cities name
my_dist = gmaps.distance_matrix('mutare CBD',point)['rows'][0]['elements'][0]
 
# Printing the result
print(my_dist['distance'])
dist = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", my_dist['distance']['text'])
price = float(dist[0]) * 0.20
# print( f' The distance cost is ${float(dist[0]) * 0.10} ')

payment = paynow.create_payment('ecocash','smasonfukuzeya123@gmail.com')
payment.add('ecocash',price)
response = paynow.send_mobile(payment,'0786195584','ecocash')
