from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('products', views.products, name='products'),
    path('products/delete/<int:id>', views.delete_product, name='delete_product'),
    path('products/edit/<int:id>', views.edit_product, name='edit_product'),
    path('orders', views.orders, name='orders'),
    path('orders/detail/<int:id>', views.order_detail, name='order_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-stock/', views.add_stock, name='add_stock'),
    path('stock/', views.stock, name='stock'),
    path('request/', views.inventory_request, name='request'),
    path('edit-stock/', views.edit_stock, name='edit_stock'),
    path('delete-stock/<int:pk>', views.del_stock, name='delete_stock'),
]
