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
    prefecture = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=30, null=True)  # 電話番号用フィールドの長さを増やす

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
        unique_together = ('user', 'playground')
