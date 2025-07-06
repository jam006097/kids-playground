# myapp/models.py - Djangoモデルの定義
from django.db import models
from django.contrib.auth.models import User


class Playground(models.Model):
    """
    Playgroundモデルは、子育て支援施設の情報を格納するためのモデルです。
    フィールド:
        prefecture: 都道府県名
        name: 施設名
        address: 施設住所
        phone: 電話番号
    """

    id = models.AutoField(primary_key=True)  # 明示的にidを追加
    prefecture = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """
    Favoriteモデルは、ユーザーがお気に入り登録した施設を格納するためのモデルです。
    フィールド:
        user: ユーザー
        playground: お気に入りの施設
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)

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

    playground = models.ForeignKey(
        Playground, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.playground.name} - {self.rating}"
