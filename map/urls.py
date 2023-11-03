from django.urls import path

from map import views

app_name = "map"

urlpatterns = [
	path('map/<int:pk>', views.show_map, name='map'),
]