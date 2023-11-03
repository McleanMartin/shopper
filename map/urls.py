from django.urls import path

from map import views

app_name = "map"

urlpatterns = [
	path('showmap/<int:pk>', views.show_map, name='showmap'),
]