from django.urls import path
from . import views

urlpatterns = [
    path("", views.PlaygroundListView.as_view(), name="index"),
    path("search_place", views.SearchPlaceView.as_view(), name="search_place"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("mypage/", views.MyPageView.as_view(), name="mypage"),
    path("add_favorite/", views.AddFavoriteView.as_view(), name="add_favorite"),
    path(
        "remove_favorite/", views.RemoveFavoriteView.as_view(), name="remove_favorite"
    ),
    path(
        "playground/<int:playground_id>/add_review/",
        views.AddReviewView.as_view(),
        name="add_review",
    ),
    path(
        "playground/<int:playground_id>/reviews/",
        views.ReviewListView.as_view(),
        name="view_reviews",
    ),
]
