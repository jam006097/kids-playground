from django.views.generic import ListView
from myapp.models import Playground
from django.db.models.query import QuerySet


class RankingListView(ListView):
    """
    施設ランキング一覧ビュー

    Playgroundオブジェクトを評価順または口コミ数順で表示します。
    """

    model = Playground  # このビューで使用するモデルをPlaygroundに設定
    template_name = "ranking/list.html"  # 使用するテンプレートを指定
    context_object_name = "playgrounds"  # テンプレート内でリストにアクセスするための変数名を'playgrounds'に設定

    def get_queryset(self) -> QuerySet[Playground]:
        """
        表示するクエリセットを決定します。

        GETリクエストの'sort'パラメータに基づいて、評価順または口コミ数順で施設を並べ替えます。
        """
        sort_by = self.request.GET.get("sort")  # GETパラメータからソート順を取得
        if sort_by == "review_count":
            # 口コミ数が多い順に施設を取得
            return Playground.objects.get_by_review_count_rank()
        else:
            # 評価が高い順に施設を取得（デフォルト）
            return Playground.objects.get_by_rating_rank()
