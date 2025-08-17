from django.db.models import Q
from django.db.models.query import QuerySet
from typing import Any, Dict
from myapp.models import Playground
from django.http import HttpRequest


class PlaygroundFilterMixin:
    """
    Playgroundモデルに対するフィルタリング機能を提供するMixin。
    GETリクエストのクエリパラメータに基づいて、QuerySetをフィルタリングし、
    フィルタリング条件をコンテキストに追加する。
    """

    request: HttpRequest

    def _get_filter_params(self) -> None:
        """
        GETリクエストからフィルタリングパラメータを取得し、インスタンス変数に格納します。
        """
        self.search_query = self.request.GET.get("q")
        self.selected_city = self.request.GET.get("city")
        self.nursing_room = self.request.GET.get("nursing_room") == "on"
        self.diaper_changing_station = (
            self.request.GET.get("diaper_changing_station") == "on"
        )
        self.stroller_accessible = self.request.GET.get("stroller_accessible") == "on"
        self.kids_space = self.request.GET.get("kids_space") == "on"
        self.lunch_allowed = self.request.GET.get("lunch_allowed") == "on"
        self.indoor_play_area = self.request.GET.get("indoor_play_area") == "on"
        self.kids_toilet = self.request.GET.get("kids_toilet") == "on"
        self.target_age_min = self.request.GET.get("target_age_min")
        self.target_age_max = self.request.GET.get("target_age_max")
        self.fee_min = self.request.GET.get("fee_min")
        self.fee_max = self.request.GET.get("fee_max")
        self.parking_info = self.request.GET.get("parking_info")

    def get_queryset(self) -> QuerySet[Playground]:
        """
        クエリセットを取得し、フィルタリングパラメータに基づいてフィルタリングします。
        """
        # 親クラスのget_querysetを呼び出す。ListViewを継承していることが前提。
        queryset = super().get_queryset()  # type: ignore
        self._get_filter_params()

        if self.search_query:
            queryset = queryset.filter(
                Q(name__icontains=self.search_query)
                | Q(address__icontains=self.search_query)
                | Q(description__icontains=self.search_query)
            )
        if self.selected_city:
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
        if self.kids_toilet:
            queryset = queryset.filter(kids_toilet_available=True)
        if self.target_age_min:
            queryset = queryset.filter(target_age_start__gte=self.target_age_min)
        if self.target_age_max:
            queryset = queryset.filter(target_age_end__lte=self.target_age_max)
        if self.fee_min:
            queryset = queryset.filter(fee_decimal__gte=self.fee_min)
        if self.fee_max:
            queryset = queryset.filter(fee_decimal__lte=self.fee_max)
        if self.parking_info and self.parking_info != "all":
            queryset = queryset.filter(parking_info=self.parking_info)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        テンプレートに渡すコンテキストデータを取得する。
        現在のフィルタリングパラメータもコンテキストに追加する。
        """
        context = super().get_context_data(**kwargs)  # type: ignore
        context.update(
            {
                "selected_city": self.selected_city,
                "search_query": self.search_query,
                "nursing_room": self.nursing_room,
                "diaper_changing_station": self.diaper_changing_station,
                "stroller_accessible": self.stroller_accessible,
                "kids_space": self.kids_space,
                "lunch_allowed": self.lunch_allowed,
                "indoor_play_area": self.indoor_play_area,
                "kids_toilet": self.kids_toilet,
                "target_age_min": self.target_age_min,
                "target_age_max": self.target_age_max,
                "fee_min": self.fee_min,
                "fee_max": self.fee_max,
                "parking_info": self.parking_info,
                "search_form_opened": bool(self.request.GET),
            }
        )
        return context
