from django.test import TestCase, Client
from django.contrib.auth.models import User
from myapp.models import Playground, Review  

class ReviewTestCase(TestCase):
    def setUp(self):
        # テストクライアントの作成
        self.client = Client()

        # テスト用のユーザーと施設を作成
        self.user = User.objects.create_user(username='jam', password='1221')
        self.playground = Playground.objects.create(
            prefecture='東京都',
            name='テスト施設',
            address='東京都新宿区',
            phone='123-456-7890'
        )

    def test_review_creation(self):
        # ユーザーをログイン
        self.client.login(username='jam', password='1221')

        # 口コミ投稿
        response = self.client.post(f'/playground/{self.playground.id}/add_review/', {
            'content': '素晴らしい施設でした！',
            'rating': 5
        })

        # レスポンスの確認
        self.assertEqual(response.status_code, 200)

        # データベースに口コミが保存されているか確認
        reviews = Review.objects.filter(playground=self.playground, user=self.user)
        self.assertEqual(reviews.count(), 1)
        review = reviews.first()
        self.assertEqual(review.content, '素晴らしい施設でした！')
        self.assertEqual(review.rating, 5)