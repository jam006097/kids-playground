from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from typing import Any, Dict, cast
from django.db.models.query import QuerySet
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from myapp.models import Playground, Favorite, Review
import urllib.request
import urllib.parse
import json
import os

from django.views.generic import ListView, View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


from users.models import CustomUser


class AddFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        POSTリクエストを処理し、指定された公園をお気に入りに追加する。
        """
        playground_id = request.POST.get("playground_id")
        if playground_id is None:
            return JsonResponse(
                {"status": "error", "message": "playground_id is required"}, status=400
            )
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを作成または取得
        user = cast(CustomUser, request.user)
        Favorite.objects.get_or_create(user=user, playground=playground)
        return JsonResponse({"status": "ok"})


class RemoveFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り削除ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        POSTリクエストを処理し、指定された公園をお気に入りから削除する。
        """
        playground_id = request.POST.get("playground_id")
        if playground_id is None:
            return JsonResponse(
                {"status": "error", "message": "playground_id is required"}, status=400
            )
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを削除
        user = cast(CustomUser, request.user)
        Favorite.objects.filter(user=user, playground=playground).delete()
        return JsonResponse({"status": "ok"})


class FavoriteListView(LoginRequiredMixin, ListView):
    """
    お気に入り一覧ページビュー。
    ログインしているユーザーのみがアクセス可能。
    ユーザーのお気に入り公園一覧を表示する。
    """

    model = Playground
    template_name = "favorites/list.html"
    context_object_name = "favorites"

    def get_queryset(self) -> QuerySet[Playground]:
        user = cast(CustomUser, self.request.user)
        queryset = cast(QuerySet[Playground], super().get_queryset())
        queryset = queryset.filter(favorite__user=user)
        self.selected_city = self.request.GET.get("city")
        if self.selected_city:
            queryset = queryset.filter(address__icontains=self.selected_city)

        # フィルタリング後の件数を取得
        self.filtered_count = queryset.count()
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        favorites = context["favorites"]
        favorite_ids = [str(p.id) for p in favorites]
        playgrounds_json = json.dumps(
            list(
                favorites.values(
                    "id", "name", "address", "phone", "latitude", "longitude"
                )
            )
        )

        context.update(
            {
                "selected_city": self.selected_city,
                "favorite_ids": json.dumps(favorite_ids),
                "playgrounds_json": playgrounds_json,
                "filtered_count": self.filtered_count,  # 追加
                "total_count": Favorite.objects.filter(
                    user=cast(CustomUser, self.request.user)
                ).count(),  # 追加
            }
        )
        return context
