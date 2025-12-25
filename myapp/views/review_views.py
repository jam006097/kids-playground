from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from typing import Any, Dict, cast
from django.db.models.query import QuerySet
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


from users.models import CustomUser


class AddReviewView(LoginRequiredMixin, View):
    """
    レビュー追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    def post(
        self, request: HttpRequest, playground_id: int, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """
        POSTリクエストを処理し、指定された公園にレビューを追加する。
        """
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        if content is None or rating is None:
            return JsonResponse(
                {"status": "error", "message": "content and rating are required"},
                status=400,
            )

        # 公園オブジェクトを取得
        playground = get_object_or_404(Playground, id=playground_id)

        try:
            rating_int = int(rating)
        except (ValueError, TypeError):
            return JsonResponse(
                {"status": "error", "message": "Invalid rating"}, status=400
            )

        # レビューを作成
        user = cast(CustomUser, request.user)
        Review.objects.create(
            playground=playground, user=user, content=content, rating=rating_int
        )

        return JsonResponse(
            {"status": "success", "message": "口コミが投稿されました！"}
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
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

    def get_queryset(self) -> QuerySet[Review]:
        """
        クエリセットを取得する。
        URLから公園IDを取得し、その公園のレビューをフィルタリングして返す。
        """
        playground_id = self.kwargs["playground_id"]
        self.playground = get_object_or_404(Playground, id=playground_id)
        return (
            Review.objects.filter(playground=self.playground)
            .select_related("user")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        テンプレートに渡すコンテキストデータを取得する。
        現在の公園情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        context["playground"] = self.playground
        return context
