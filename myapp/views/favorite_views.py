from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from myapp.models import Playground, Favorite, Review
import urllib.request
import urllib.parse
import json
import logging
import os
from dotenv import load_dotenv
from django.views.generic import ListView, View, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

# .envファイルから環境変数を読み込む
load_dotenv()

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # ログをファイルに保存
        logging.StreamHandler(),  # コンソールにもログを表示
    ],
)


class AddFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園をお気に入りに追加する。
        """
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを作成または取得
        Favorite.objects.get_or_create(user=request.user, playground=playground)
        return JsonResponse({"status": "ok"})


class RemoveFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り削除ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園をお気に入りから削除する。
        """
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを削除
        Favorite.objects.filter(user=request.user, playground=playground).delete()
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

    def get_queryset(self):
        queryset = super().get_queryset().filter(favorite__user=self.request.user)
        self.selected_city = self.request.GET.get("city")
        if self.selected_city:
            queryset = queryset.filter(address__icontains=self.selected_city)
        
        # フィルタリング後の件数を取得
        self.filtered_count = queryset.count()
        return queryset

    def get_context_data(self, **kwargs):
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
                "filtered_count": self.filtered_count, # 追加
                "total_count": Favorite.objects.filter(user=self.request.user).count(), # 追加
            }
        )
        return context
