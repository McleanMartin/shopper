from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone

from products.models import Order, OrderItem
from cart.utils.cart import Cart
import googlemaps

import json
import requests
import sys


@login_required
def create_order(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(
            order=order, product=item['product'],
            price=item['price'], quantity=item['quantity']
    )
    return redirect('pay_order', order_id=order.id)


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order}
    return render(request, 'checkout.html', context)


@login_required
def fake_payment(request, order_id):
    cart = Cart(request)
    cart.clear()
    order = get_object_or_404(Order, id=order_id)
    order.status = True
    order.save()

    # Requires API key
    gmaps = googlemaps.Client(key='AIzaSyDl91ZLUSOuh36T_Z3EXcrgnZVc8bBd-1Y')
    
    # Requires location name
    dist = gmaps.distance_matrix('fern valley,mutare','dangamvura,mutare')['rows'][0]['elements'][0]
    
    # Get distance
    distance = dist['distance']['text']
    return redirect('user_orders')


@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'order/user_orders.html', context)


