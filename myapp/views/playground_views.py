from django.db.models import Q  # Qオブジェクトをインポート
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpRequest
from typing import Any, Dict, cast
from django.db.models.query import QuerySet
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from myapp.models import Playground, Favorite, Review
import urllib.request
import urllib.parse
import json
from django.views.generic import ListView, View, CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


class PlaygroundListView(ListView):
    """
    公園一覧を表示するビュー。
    様々な条件でのフィルタリング機能と、ユーザーのお気に入り公園情報を表示する。
    """

    model = Playground
    template_name = "playgrounds/list.html"
    context_object_name = "playgrounds"

    def get_queryset(self) -> QuerySet[Playground]:
        """
        クエリセットを取得する。
        リクエストのGETパラメータに基づいて、公園をフィルタリングする。
        """
        queryset = cast(QuerySet[Playground], super().get_queryset())

        # フィルタリングパラメータの取得
        self.search_query = self.request.GET.get("q")
        self.selected_city = self.request.GET.get("city")  # Keep existing city filter
        self.nursing_room = (
            self.request.GET.get("nursing_room") == "on"
        )  # New filter parameter
        self.diaper_changing_station = (
            self.request.GET.get("diaper_changing_station") == "on"
        )  # New filter parameter
        self.stroller_accessible = (
            self.request.GET.get("stroller_accessible") == "on"
        )  # New filter parameter
        self.kids_space = (
            self.request.GET.get("kids_space") == "on"
        )  # New filter parameter
        self.lunch_allowed = (
            self.request.GET.get("lunch_allowed") == "on"
        )  # New filter parameter
        self.indoor_play_area = (
            self.request.GET.get("indoor_play_area") == "on"
        )  # New filter parameter

        # フィルタリングロジック
        if self.search_query:
            queryset = queryset.filter(
                Q(name__icontains=self.search_query)
                | Q(address__icontains=self.search_query)
                | Q(description__icontains=self.search_query)
            )
        if self.selected_city:
            # 都市名で部分一致検索
            queryset = queryset.filter(address__icontains=self.selected_city)
        if self.nursing_room:
            queryset = queryset.filter(nursing_room_available=True)
        if self.diaper_changing_station:
            queryset = queryset.filter(diaper_changing_station_available=True)
        if self.stroller_accessible:
            queryset = queryset.filter(stroller_accessible=True)
        if self.kids_space:
            queryset = queryset.filter(kids_space_available=True)
        if self.lunch_allowed:
            queryset = queryset.filter(lunch_allowed=True)
        if self.indoor_play_area:
            queryset = queryset.filter(indoor_play_area=True)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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
        # formatted_phone プロパティを含めるために手動でデータを構築
        playgrounds_data = []
        for playground in playgrounds:
            playgrounds_data.append(
                {
                    "id": playground.id,
                    "name": playground.name,
                    "address": playground.address,
                    "phone": playground.phone,  # 元の電話番号も保持
                    "formatted_phone": playground.formatted_phone,  # フォーマット済み電話番号
                    "latitude": playground.latitude,
                    "longitude": playground.longitude,
                    "opening_hours": playground.formatted_opening_hours,
                    "target_age": playground.formatted_target_age,
                    "fee": playground.formatted_fee,
                    "parking": playground.formatted_parking,
                }
            )
        playgrounds_json = json.dumps(playgrounds_data)

        favorite_ids: list[str] = []
        # ユーザーが認証済みの場合、お気に入り公園の情報を取得
        if self.request.user.is_authenticated:
            # お気に入り公園のIDリストを取得
            favorite_ids_int = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "playground_id", flat=True
                )
            )
            favorite_ids = [str(id) for id in favorite_ids_int]

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
