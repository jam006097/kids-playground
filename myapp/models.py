# myapp/models.py - Djangoモデルの定義
from django.db import models

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
