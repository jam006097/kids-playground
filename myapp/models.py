# myapp/models.py - Djangoモデルの定義
from __future__ import annotations
from django.db import models
from django.conf import settings
from django.db.models import Avg, Count, QuerySet
from typing import Any
import datetime
from users.models import CustomUser


class PlaygroundManager(models.Manager["Playground"]):
    def get_by_rating_rank(self) -> QuerySet["Playground"]:
        """評価の平均点が高い順に施設を返す"""
        return (
            self.get_queryset()
            .annotate(avg_rating=Avg("reviews__rating"))
            .filter(avg_rating__isnull=False)
            .order_by("-avg_rating")
        )

    def get_by_review_count_rank(self) -> QuerySet["Playground"]:
        """口コミの件数が多い順に施設を返す"""
        return (
            self.get_queryset()
            .annotate(review_count=Count("reviews"))
            .filter(review_count__gt=0)
            .order_by("-review_count")
        )


class Playground(models.Model):
    """
    Playgroundモデルは、子育て支援施設の情報を格納するためのモデルです。
    フィールド:
        prefecture: 都道府県名
        name: 施設名
        address: 施設住所
        phone: 電話番号
        latitude: 緯度
        longitude: 経度
    """

    id: int = models.AutoField(primary_key=True)  # type: ignore
    prefecture: str = models.CharField(max_length=100)  # type: ignore
    name: str = models.CharField(max_length=200)  # type: ignore
    address: str = models.CharField(max_length=300)  # type: ignore
    phone: str | None = models.CharField(max_length=30, null=True)  # type: ignore
    latitude: float | None = models.FloatField(null=True)  # type: ignore
    longitude: float | None = models.FloatField(null=True)  # type: ignore

    description: str = models.TextField(default="")  # type: ignore
    opening_hours: str = models.CharField(max_length=200, default="")  # type: ignore
    website: str = models.URLField(max_length=200, default="")  # type: ignore

    nursing_room_available: bool = models.BooleanField(default=False)  # type: ignore
    diaper_changing_station_available: bool = models.BooleanField(default=False)  # type: ignore
    stroller_accessible: bool = models.BooleanField(default=False)  # type: ignore
    kids_space_available: bool = models.BooleanField(default=False)  # type: ignore
    notes_for_infants: str | None = models.TextField(blank=True, null=True)  # type: ignore
    lunch_allowed: bool = models.BooleanField(default=False)  # type: ignore

    google_map_url: str | None = models.URLField(max_length=500, blank=True, null=True)  # type: ignore
    parking_available: bool = models.BooleanField(default=False)  # type: ignore
    indoor_play_area: bool = models.BooleanField(default=False)  # type: ignore
    kids_toilet_available: bool = models.BooleanField(default=False)  # type: ignore
    target_age: str | None = models.CharField(max_length=100, blank=True, null=True)  # type: ignore
    fee: str | None = models.CharField(max_length=100, blank=True, null=True)  # type: ignore

    objects: "PlaygroundManager" = PlaygroundManager()

    def __str__(self) -> str:
        return self.name


class Favorite(models.Model):
    """
    Favoriteモデルは、ユーザーがお気に入り登録した施設を格納するためのモデルです。
    フィールド:
        user: ユーザー
        playground: お気に入りの施設
    """

    user: "CustomUser" = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # type: ignore
    playground: "Playground" = models.ForeignKey(Playground, on_delete=models.CASCADE)  # type: ignore

    class Meta:
        unique_together = ("user", "playground")


class Review(models.Model):
    """
    Reviewモデルは、施設に対する口コミを格納するためのモデルです。
    フィールド:
        playground: 口コミ対象の施設
        user: 口コミを投稿したユーザー
        content: 口コミ内容
        rating: 評価（1〜5の整数）
        created_at: 口コミ投稿日時
    """

    playground: "Playground" = models.ForeignKey(  # type: ignore
        Playground, on_delete=models.CASCADE, related_name="reviews"
    )
    user: "CustomUser" = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # type: ignore
    content: str = models.TextField()  # type: ignore
    rating: int = models.PositiveIntegerField()  # type: ignore
    created_at: datetime.datetime = models.DateTimeField(auto_now_add=True)  # type: ignore

    def __str__(self) -> str:
        return f"{self.user.email} - {self.playground.name} - {self.rating}"
