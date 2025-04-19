from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search_place', views.search_place, name='search_place'),
    path('login/', views.user_login, name='login'),
    path('mypage/', views.mypage, name='mypage'),
    path('add_favorite/', views.add_favorite, name='add_favorite'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('playground/<int:playground_id>/add_review/', views.add_review, name='add_review'),
    path('playground/<int:playground_id>/reviews/', views.view_reviews, name='view_reviews'),
]
