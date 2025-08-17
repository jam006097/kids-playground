# myapp/models.py - Djangoモデルの定義
from __future__ import annotations
from django.db import models
from django.conf import settings
from django.db.models import Avg, Count, QuerySet
from typing import Any
import datetime
from users.models import CustomUser
import re


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

    description: str | None = models.TextField(blank=True, null=True, default="")  # type: ignore
    website: str = models.URLField(max_length=200, default="")  # type: ignore

    nursing_room_available: bool = models.BooleanField(default=False)  # type: ignore
    diaper_changing_station_available: bool = models.BooleanField(default=False)  # type: ignore
    stroller_accessible: bool = models.BooleanField(default=False)  # type: ignore

    lunch_allowed: bool = models.BooleanField(default=False)  # type: ignore

    google_map_url: str | None = models.URLField(max_length=500, blank=True, null=True)  # type: ignore
    indoor_play_area: bool = models.BooleanField(default=False)  # type: ignore
    kids_toilet_available: bool = models.BooleanField(default=False)  # type: ignore

    # New fields
    opening_time: models.TimeField = models.TimeField(null=True, blank=True)  # type: ignore
    closing_time: models.TimeField = models.TimeField(null=True, blank=True)  # type: ignore
    target_age_start: models.IntegerField = models.IntegerField(null=True, blank=True)  # type: ignore
    target_age_end: models.IntegerField = models.IntegerField(null=True, blank=True)  # type: ignore
    fee_decimal: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # type: ignore

    PARKING_CHOICES = [
        ("NO", "なし"),
        ("FREE", "無料"),
        ("PAID", "有料"),
    ]
    parking_info: models.CharField = models.CharField(  # type: ignore
        max_length=10,
        choices=PARKING_CHOICES,
        default="NO",
        null=True,
        blank=True,
    )

    objects: "PlaygroundManager" = PlaygroundManager()

    def __str__(self) -> str:
        return self.name

    @property
    def formatted_opening_hours(self) -> str:
        if self.opening_time and self.closing_time:
            return f"{self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"
        elif self.opening_time:
            return f"{self.opening_time.strftime('%H:%M')}"
        return "情報なし"

    @property
    def formatted_target_age(self) -> str:
        if self.target_age_start is not None and self.target_age_end is not None:
            return f"{self.target_age_start}歳 - {self.target_age_end}歳"
        elif self.target_age_start is not None:
            return f"{self.target_age_start}歳から"
        return "情報なし"

    @property
    def formatted_fee(self) -> str:
        if self.fee_decimal is not None:
            if self.fee_decimal == 0:
                return "無料"
            return f"{int(self.fee_decimal)}円"
        return "情報なし"

    @property
    def formatted_parking(self) -> str:
        return self.get_parking_info_display()  # type: ignore

    @property
    def formatted_phone(self) -> str:
        """電話番号をハイフンで区切ってフォーマットするプロパティ"""
        if not self.phone:
            return ""
        # 数字以外の文字をすべて削除
        digits_only = re.sub(r"[^0-9]", "", str(self.phone))

        if len(digits_only) == 10:  # 例: 0901234567 -> 090-123-4567
            return f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
        elif len(digits_only) == 11:  # 例: 09012345678 -> 090-1234-5678
            return f"{digits_only[:3]}-{digits_only[3:7]}-{digits_only[7:]}"
        else:
            return self.phone  # その他の桁数の場合はそのまま返す


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
