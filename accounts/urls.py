from django.urls import path
from .views import MyPageView, AccountNameChangeView

app_name = "accounts"

urlpatterns = [
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("name/", AccountNameChangeView.as_view(), name="name_change"),
]
