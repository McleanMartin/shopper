from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

from products.models import Product,Stock
from django.contrib.auth.models import User
from products.models import Order, OrderItem
from .forms import *


def is_manager(user):
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404




@login_required
def dashboard(request):
    products = Product.objects.all().count()
    orders = Order.objects.all().count()
    customers = User.objects.all().count()
    client_orders = Order.objects.all().order_by('-created')
    context = {
        'products':products,
        'orders':orders,
        'customers':customers,
        'client_orders':client_orders
    }
    return render(request,'dashboard/stat.html',context)

@login_required
def products(request):
    products = Product.objects.all()
    context = {'title':'Products' ,'products':products}
    return render(request, 'dashboard/products.html', context)



@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added Successfuly!')
            return redirect('dashboard:products')
    else:
        form = AddProductForm()
    context = {'title':'Add Product', 'form':form}
    return render(request, 'dashboard/add_product.html', context)



@login_required
def delete_product(request, id):
    product = Product.objects.filter(id=id).delete()
    messages.success(request, 'product has been deleted!', 'success')
    return redirect('dashboard:products')



@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated', 'success')
            return redirect('dashboard:products')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 'form':form}
    return render(request, 'dashboard/edit_product.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added Successfuly!')
            return redirect('dashboard:products')
    else:
        form = AddCategoryForm()
    context = {'title':'Add Category', 'form':form}
    return render(request, 'dashboard/add_category.html', context)



@login_required
def orders(request):
    orders = Order.objects.all()
    context = {'title':'Orders', 'orders':orders}
    return render(request, 'dashboard/orders.html', context)



@login_required
def order_detail(request, id):
    order = Order.objects.filter(id=id).first()
    items = OrderItem.objects.filter(order=order).all()
    context = {'title':'order detail', 'items':items, 'order':order}
    return render(request, 'dashboard/order_detail.html', context)


def add_stock(request):
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfuly')
            return redirect('dashboard:stock')
    else:
        form = AddStockForm()
    context = {'title':'Add Stock', 'form':form}
    return render(request,'dashboard/add_stock.html',context)


#stock control
def stock(request):
    items = Stock.objects.all()
    context = {'title':'Inventory','items':items}
    return render(request,'dashboard/stock.html',context)


def edit_stock(request):
    context = {'title':'Edit Stock',}
    return render(request,'dashboard/edit_stock.html',context)


def del_stock(request,pk):
    if request.method == 'POST':
        item = Stock.objects.get(pk=pk)
        item.delete()
        item.save()
        messages.success(request, 'Item deleted succefully.', 'info')
    return redirect('dashboard:stock')


def inventory_request(request):
    if request.method == 'POST':
        form = RequestStockForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            stock = Stock.objects.get(title=data.item)
            if stock.quantity < data.quantity or stock.threshold > stock.quantity:
                messages.warning(request, f'You have {stock.quantity} {stock.title} left in stock ,\
                                Please Re-Order stock! and place your request again.')
                return redirect('dashboard:request')
            else:
                data.req = request.user
                data.save()
                messages.success(request, 'Request Submitted Successfully')
                return redirect('dashboard:stock')
    else:
        form = RequestStockForm()
    context = {'title':'Add Stock', 'form':form}
    return render(request,'dashboard/request.html',context)
    
