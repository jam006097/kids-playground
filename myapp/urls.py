from django.urls import path
from myapp.views.playground_views import PlaygroundListView
from myapp.views.auth_views import UserLoginView, UserLogoutView, UserRegisterView
from myapp.views.favorite_views import (
    AddFavoriteView,
    RemoveFavoriteView,
    FavoriteListView,
)
from myapp.views.review_views import AddReviewView, ReviewListView

app_name = "myapp"

urlpatterns = [
    path("", PlaygroundListView.as_view(), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("favorites/", FavoriteListView.as_view(), name="favorites"),
    path("add_favorite/", AddFavoriteView.as_view(), name="add_favorite"),
    path("remove_favorite/", RemoveFavoriteView.as_view(), name="remove_favorite"),
    path(
        "playground/<int:playground_id>/add_review/",
        AddReviewView.as_view(),
        name="add_review",
    ),
    path(
        "playground/<int:playground_id>/reviews/",
        ReviewListView.as_view(),
        name="view_reviews",
    ),
]
