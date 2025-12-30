from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse,
    HttpRequest,
    HttpResponseRedirect,
    HttpResponse,  # HttpResponseを追加
)
from typing import Any, cast, Dict
from myapp.models import Playground, Review
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView  # CreateViewを追加
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import LoginRequiredJsonMixin
from users.models import CustomUser
from myapp.forms import ReviewForm  # ReviewFormをインポート
from django.urls import reverse_lazy  # reverse_lazyをインポート


class AddReviewView(LoginRequiredJsonMixin):
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
        review = Review.objects.create(
            playground=playground, user=user, content=content, rating=rating_int
        )

        review_data = {
            "content": review.content,
            "rating": review.rating,
            "user_account_name": review.user.account_name,
            "created_at": review.created_at.strftime("%Y年%m月%d日 %H:%M"),
        }

        return JsonResponse({"status": "success", "review": review_data})

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
    template_name = "reviews/review_list.html"
    context_object_name = "reviews"
    paginate_by = 10  # 1ページあたり10件

    def get_queryset(self):
        self.playground = get_object_or_404(Playground, id=self.kwargs["playground_id"])
        return (
            Review.objects.filter(playground=self.playground)
            .select_related("user")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["playground"] = self.playground
        return context


class ReviewCreateView(
    LoginRequiredMixin, CreateView
):  # TemplateViewからCreateViewに変更
    """
    レビュー投稿ページビュー。
    ログインしているユーザーのみがアクセス可能。
    """

    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def get_success_url(self) -> str:
        """
        レビュー投稿成功後にリダイレクトするURLを返す。
        公園の詳細ページにリダイレクトする。
        """
        return reverse_lazy("myapp:facility_detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(
        self, form: ReviewForm
    ) -> HttpResponse:  # HttpResponseRedirectからHttpResponseに変更
        """
        フォームが有効な場合の処理。
        PlaygroundとUserをReviewオブジェクトに設定する。
        """
        playground = get_object_or_404(Playground, pk=self.kwargs["pk"])
        form.instance.playground = playground
        form.instance.user = cast(CustomUser, self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        テンプレートに渡すコンテキストデータを追加する。
        """
        context = super().get_context_data(**kwargs)
        context["playground"] = get_object_or_404(Playground, pk=self.kwargs["pk"])
        if "form" not in context:  # フォームがすでにコンテキストにない場合のみ追加
            context["form"] = self.get_form()
        return context
