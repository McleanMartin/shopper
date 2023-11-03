from django.urls import path

from products import views

app_name = "products"

urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('<int:pk>', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
	path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
]