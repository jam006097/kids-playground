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

from ..filters import PlaygroundFilterMixin
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


class FavoriteListView(LoginRequiredMixin, PlaygroundFilterMixin, ListView):
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
        # PlaygroundFilterMixinのget_querysetを呼び出してフィルタリングを適用
        queryset = super().get_queryset()
        # さらにお気に入り登録されたもので絞り込み
        queryset = queryset.filter(favorite__user=user)

        # フィルタリング後の件数を取得
        self.filtered_count = queryset.count()
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        favorites = context["favorites"]
        favorite_ids = [str(p.id) for p in favorites]
        # 公園データをJSON形式に変換
        playgrounds_data = []
        for playground in favorites:
            playgrounds_data.append(
                {
                    "id": playground.id,
                    "name": playground.name,
                    "address": playground.address,
                    "phone": playground.phone,
                    "formatted_phone": playground.formatted_phone,
                    "latitude": playground.latitude,
                    "longitude": playground.longitude,
                    "opening_hours": playground.formatted_opening_hours,
                    "target_age": playground.formatted_target_age,
                    "fee": playground.formatted_fee,
                    "parking": playground.formatted_parking,
                }
            )
        playgrounds_json = json.dumps(playgrounds_data)

        context.update(
            {
                "favorite_ids": json.dumps(favorite_ids),
                "playgrounds_json": playgrounds_json,
                "filtered_count": self.filtered_count,
                "total_count": Favorite.objects.filter(
                    user=cast(CustomUser, self.request.user)
                ).count(),
            }
        )
        return context


class ReviewView(LoginRequiredMixin, View):
    """
    口コミ投稿ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        POSTリクエストを処理し、口コミを保存する。
        """
        playground_id = request.POST.get("playground_id")
        content = request.POST.get("content")
        rating_str = request.POST.get("rating")

        if not all([playground_id, content, rating_str]):
            return JsonResponse(
                {"status": "error", "message": "Missing required fields"}, status=400
            )

        content = cast(str, content)
        rating_str = cast(str, rating_str)

        playground = get_object_or_404(Playground, id=playground_id)
        user = cast(CustomUser, request.user)
        rating = int(rating_str)

        Review.objects.create(
            playground=playground, user=user, content=content, rating=rating
        )

        return JsonResponse({"status": "ok"})
