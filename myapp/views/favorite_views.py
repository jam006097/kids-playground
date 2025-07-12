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
from django.views.generic import ListView, View, CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

# .envファイルから環境変数を読み込む
load_dotenv()

# APIのURLとGoogle Maps APIキーを環境変数から取得
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

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


class MyPageView(LoginRequiredMixin, TemplateView):
    """
    マイページビュー。
    ログインしているユーザーのみがアクセス可能。
    ユーザーのお気に入り公園一覧を表示する。
    """
    template_name = "mypage.html"

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        ユーザーのお気に入り公園情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        # ユーザーのお気に入り公園を取得
        favorites = Favorite.objects.filter(user=self.request.user).select_related(
            "playground"
        )
        favorite_playgrounds = [favorite.playground for favorite in favorites]
        favorite_ids = [str(p.id) for p in favorite_playgrounds]
        # お気に入り公園データをJSON形式に変換
        playgrounds_json = json.dumps(
            [
                {"name": p.name, "address": p.address, "phone": p.phone}
                for p in favorite_playgrounds
            ]
        )
        # コンテキストを更新
        context.update(
            {
                "favorites": favorite_playgrounds,
                "favorite_ids": favorite_ids,
                "playgrounds_json": playgrounds_json,
                "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
            }
        )
        return context
