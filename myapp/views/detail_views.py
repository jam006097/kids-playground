from django.views.generic import DetailView
from myapp.models import Playground


class FacilityDetailView(DetailView):
    """
    施設詳細ビュー

    指定されたPlaygroundオブジェクトの詳細を表示します。
    """

    model = Playground  # このビューで使用するモデルをPlaygroundに設定
    template_name = "myapp/facility_detail.html"  # 使用するテンプレートを指定
    context_object_name = "playground"  # テンプレート内でオブジェクトにアクセスするための変数名を'playground'に設定
