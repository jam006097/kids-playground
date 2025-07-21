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


class AddReviewView(LoginRequiredMixin, View):
    """
    レビュー追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(self, request, playground_id, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園にレビューを追加する。
        """
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        # 公園オブジェクトを取得
        playground = get_object_or_404(Playground, id=playground_id)

        # レビューを作成
        Review.objects.create(
            playground=playground, user=request.user, content=content, rating=rating
        )

        return JsonResponse(
            {"status": "success", "message": "口コミが投稿されました！"}
        )

    def get(self, request, *args, **kwargs):
        """
        GETリクエストは無効。
        """
        return JsonResponse(
            {"status": "error", "message": "無効なリクエストです。"}, status=400
        )


class ReviewListView(ListView):
    """
    レビュー一覧ビュー。
    指定された公園のレビュー一覧を表示する。
    """

    model = Review
    template_name = "reviews/view_reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        """
        クエリセットを取得する。
        URLから公園IDを取得し、その公園のレビューをフィルタリングして返す。
        """
        playground_id = self.kwargs["playground_id"]
        self.playground = get_object_or_404(Playground, id=playground_id)
        return Review.objects.filter(playground=self.playground).select_related("user")

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        現在の公園情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        context["playground"] = self.playground
        return context
