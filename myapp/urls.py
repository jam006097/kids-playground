from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_place', views.search_place, name='search_place'),
]
