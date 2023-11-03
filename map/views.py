from django.shortcuts import render
import googlemaps
from datetime import datetime

def show_map(request,pk):
    
    return render(request,'map/map.html')