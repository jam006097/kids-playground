from django.urls import path
from myapp.views.playground_views import PlaygroundListView
from myapp.views.search_views import SearchPlaceView
from myapp.views.auth_views import UserLoginView, UserLogoutView, UserRegisterView
from myapp.views.favorite_views import AddFavoriteView, RemoveFavoriteView, MyPageView
from myapp.views.review_views import AddReviewView, ReviewListView

urlpatterns = [
    path("", PlaygroundListView.as_view(), name="index"),
    path("search_place", SearchPlaceView.as_view(), name="search_place"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
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
