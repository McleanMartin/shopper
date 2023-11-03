from django.shortcuts import render,get_object_or_404
import googlemaps
from datetime import datetime
from products.models import Order

def show_map(request,pk):
    order = get_object_or_404(Order, pk=pk)
    destination = ""
    return render(request,'map/map.html',{'destination':destination})