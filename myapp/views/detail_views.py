from django.views.generic import DetailView
from myapp.models import Playground, Review
from typing import Any, Dict
from django.core.paginator import Paginator


class FacilityDetailView(DetailView):
    """
    施設詳細ビュー

    指定されたPlaygroundオブジェクトの詳細を表示します。
    """

    model = Playground
    template_name = "myapp/facility_detail.html"
    context_object_name = "playground"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        テンプレートに渡すコンテキストデータを拡張します。
        レビューをページ分割して追加します。
        """
        context = super().get_context_data(**kwargs)
        playground = self.get_object()

        # 直近10件のレビューを取得
        all_reviews = (
            Review.objects.filter(playground=playground)
            .select_related("user")
            .order_by("-created_at")
        )
        context["reviews"] = all_reviews[:10]
        context["has_more_reviews"] = all_reviews.count() > 10
        return context
