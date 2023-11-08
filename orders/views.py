from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
from products.models import Order, OrderItem
from cart.utils.cart import Cart
from .map import get_delivery_price

import paynow
import time


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        dist =  get_delivery_price(str(request.POST.get('address'))).get()     
        price =  dist + cart.get_total_price
        try:
            payment = paynow.create_payment('ecocash','smasonfukuzeya123@gmail.com')
            payment.add('ecocash',price)
            response = paynow.send_mobile(payment,str(request.POST.get('number')),'ecocash')
            if response.success:
                poll_url = response.poll_url
                print(poll_url)
                status  = paynow.check_transaction_status(poll_url)
                time.sleep(15)
                if status.paid:
                    order = Order.objects.create(
                    user=request.user,
                    firstname = request.POST.get('firstname'),
                    lastname = request.POST.get('lastname'),
                    destination = request.POST.get('address'),
                    status = True,
                    )
                    for item in cart:
                        OrderItem.objects.create(
                                order=order, product=item['product'],
                                price=item['price'], quantity=item['quantity']

                        )
                print("Payment ",{'status':status})
            else:
                pass
        except:
            pass
    return HttpResponseRedirect('list')


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {'title':'Checkout' ,'order':order}
    return render(request, 'checkout.html', context)



@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'order/user_orders.html', context)



def calculate_weekly_sales():
    pass



