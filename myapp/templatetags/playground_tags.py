from django import template
from myapp.models import Favorite

register = template.Library()

@register.simple_tag
def is_favorite(playground, user):
    """ユーザーが施設をお気に入り登録しているか判定する"""
    if not user.is_authenticated:
        return False
    return Favorite.objects.filter(playground=playground, user=user).exists()
