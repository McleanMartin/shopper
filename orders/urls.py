from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    
    path('list/', views.user_orders, name='user_orders'),
]