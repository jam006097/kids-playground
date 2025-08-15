from django.views.generic import ListView
from myapp.models import Playground
from django.db.models.query import QuerySet


class RankingListView(ListView):
    model = Playground
    template_name = "ranking/list.html"
    context_object_name = "playgrounds"

    def get_queryset(self) -> QuerySet[Playground]:
        sort_by = self.request.GET.get("sort")
        if sort_by == "review_count":
            return Playground.objects.get_by_review_count_rank()
        else:
            return Playground.objects.get_by_rating_rank()
