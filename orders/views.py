from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import HttpResponseRedirect,HttpResponse
from products.models import Order, OrderItem
from django.contrib.auth.models import User
from cart.utils.cart import Cart
from .map import get_cost
from django.contrib import messages
import time

from paynow import Paynow

paynow = Paynow(
    '14813',
    '3e688baf-5630-4145-a99c-d5deb32e5b2e',
    'https://google.com',
    'http://127.0.0.1:8000'
)

@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        number = request.POST.get('number')
        try:
            #get total cost
            point = request.POST.get('address')
            # d_price =  get_cost(point)    
            price =  cart.get_total_price() 

            #create payment
            payment = paynow.create_payment('ecocash','smasonfukuzeya123@gmail.com')
            payment.add('ecocash',price)
            response = paynow.send_mobile(payment,str(number),'ecocash')

            #get response
            if response.success:
                poll_url = response.poll_url
                print(poll_url)
                status  = paynow.check_transaction_status(poll_url)
                print(status.status)
                time.sleep(15)
                if status.status == 'sent':
                    print('am here')
                    order = Order.objects.create(
                    user=request.user,
                    firstname = request.POST.get('firstname'),
                    lastname = request.POST.get('lastname'),
                    destination = request.POST.get('address'),
                    paid=True,
                    
                    )
        
                    for item in cart:
                        OrderItem.objects.create(
                                order=order, product=item['product'],
                                price=item['price'], quantity=item['quantity']

                        )
                    print("Payment ",{'status':status})
                    messages.success(request,'order placed successful', 'success')
                    return redirect('products:home_page')
                else:
                    order = Order.objects.create(
                    user=request.user,
                    firstname = request.POST.get('firstname'),
                    lastname = request.POST.get('lastname'),
                    destination = request.POST.get('address'),
                    paid=True,
                    
                    )
                    
                    for item in cart:
                        OrderItem.objects.create(
                                order=order, product=item['product'],
                                price=item['price'], quantity=item['quantity']

                        )
                    print("Payment ",{'status':status})
                    messages.success(request,'order placed successful', 'success')
                    return redirect('products:home_page')
            else:
                messages.error(request,'')
                return redirect('cart:show_cart')
        except:
            messages.error(request,'Something went wrong with paynow server or you have insuffient balance ', 'danger')
            return redirect('cart:show_cart')
    else:
        messages.error(request,'extrernal error, something went wrong with paynow server', 'danger')
        return redirect('cart:show_cart')



@login_required
def user_orders(request):
    orders = request.user.orders.all()
    context = {'title':'Orders', 'orders': orders}
    return render(request, 'order/user_orders.html', context)



def calculate_weekly_sales():
    pass



