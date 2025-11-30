from django.urls import path
from myapp.views.playground_views import PlaygroundListView
from myapp.views.favorite_views import (
    AddFavoriteView,
    RemoveFavoriteView,
    FavoriteListView,
)
from myapp.views.review_views import AddReviewView, ReviewListView
from myapp.views.ranking_views import RankingListView
from myapp.views.detail_views import FacilityDetailView
from myapp.views.chat_views import ChatView
from myapp.views.about import about_view


app_name = "myapp"

urlpatterns = [
    path("", PlaygroundListView.as_view(), name="index"),
    path("facilities/<int:pk>/", FacilityDetailView.as_view(), name="facility_detail"),
    path("ranking/", RankingListView.as_view(), name="ranking"),
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
    path("about/", about_view, name="about"),
    path("chat/", ChatView.as_view(), name="chat"),
]
