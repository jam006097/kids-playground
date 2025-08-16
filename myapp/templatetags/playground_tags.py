from django import template
from myapp.models import Favorite
import re

register = template.Library()


@register.simple_tag
def is_favorite(playground, user):
    """ユーザーが施設をお気に入り登録しているか判定する"""
    if not user.is_authenticated:
        return False
    return Favorite.objects.filter(playground=playground, user=user).exists()


@register.filter
def format_phone_number(value):
    """電話番号をハイフンで区切ってフォーマットする"""
    if not value:  # Noneや空文字列の場合
        return ""
    # 数字以外の文字をすべて削除
    digits_only = re.sub(r"[^0-9]", "", str(value))

    if len(digits_only) == 10:  # 例: 0901234567 -> 090-123-4567
        return f"{digits_only[:3]}-{digits_only[3:6]}-{digits_only[6:]}"
    elif len(digits_only) == 11:  # 例: 09012345678 -> 090-1234-5678
        return f"{digits_only[:3]}-{digits_only[3:7]}-{digits_only[7:]}"
    else:
        return value  # その他の桁数の場合はそのまま返す
