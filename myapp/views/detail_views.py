from django.views.generic import DetailView
from myapp.models import Playground, Review
from typing import Any, Dict


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
        """
        context = super().get_context_data(**kwargs)
        playground = self.get_object()
        reviews = (
            Review.objects.filter(playground=playground)
            .select_related("user")
            .order_by("-created_at")
        )
        context["reviews"] = reviews
        return context
