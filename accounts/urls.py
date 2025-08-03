from django.urls import path
from .views import MyPageView

app_name = 'accounts'

urlpatterns = [
    path('mypage/', MyPageView.as_view(), name='mypage'),
]
