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

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # ログをファイルに保存
        logging.StreamHandler(),  # コンソールにもログを表示
    ],
)


class PlaygroundListView(ListView):
    """
    公園一覧を表示するビュー。
    都市によるフィルタリング機能と、ユーザーのお気に入り公園情報を表示する。
    """

    model = Playground
    template_name = "playgrounds/list.html"
    context_object_name = "playgrounds"

    def get_queryset(self):
        """
        クエリセットを取得する。
        リクエストに'city'パラメータがあれば、その都市でフィルタリングする。
        """
        queryset = super().get_queryset()
        self.selected_city = self.request.GET.get("city")
        if self.selected_city:
            # 都市名で部分一致検索
            queryset = queryset.filter(address__icontains=self.selected_city)
        return queryset

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        公園の総数、フィルタリングされた公園の数、お気に入り公園の情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        playgrounds = context["playgrounds"]

        # 公園の総数とフィルタリングされた公園の数を取得
        total_count = Playground.objects.count()
        filtered_count = playgrounds.count()

        # 公園データをJSON形式に変換
        playgrounds_json = json.dumps(
            list(
                playgrounds.values(
                    "id", "name", "address", "phone", "latitude", "longitude"
                )
            )
        )

        favorite_ids = []
        # ユーザーが認証済みの場合、お気に入り公園の情報を取得
        if self.request.user.is_authenticated:
            # お気に入り公園のIDリストを取得
            favorite_ids = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "playground_id", flat=True
                )
            )
            favorite_ids = [str(id) for id in favorite_ids]

        # コンテキストを更新
        context.update(
            {
                "selected_city": self.selected_city,
                "total_count": total_count,
                "filtered_count": filtered_count,
                "playgrounds_json": playgrounds_json,
                "favorite_ids": json.dumps(favorite_ids),
            }
        )
        return context
