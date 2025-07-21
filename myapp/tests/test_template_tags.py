from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Playground, Favorite
from myapp.templatetags.playground_tags import is_favorite

class TemplateTagsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.playground = Playground.objects.create(name='Test Park')

    def test_is_favorite_tag(self):
        """is_favoriteタグが正しくお気に入り状態を判定できるかテスト"""
        # お気に入りではない状態
        self.assertFalse(is_favorite(self.playground, self.user))

        # お気に入りに追加
        Favorite.objects.create(user=self.user, playground=self.playground)
        
        # お気に入りである状態
        self.assertTrue(is_favorite(self.playground, self.user))

    def test_is_favorite_for_anonymous_user(self):
        """is_favoriteタグが未認証ユーザーに対してFalseを返すかテスト"""
        from django.contrib.auth.models import AnonymousUser
        anonymous_user = AnonymousUser()
        self.assertFalse(is_favorite(self.playground, anonymous_user))
