from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from myapp.models import Playground, Review

User = get_user_model()


class ReviewViewsTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            account_name="testuser",
        )
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_review_url = reverse(
            "myapp:add_review", kwargs={"playground_id": self.playground.id}
        )
        self.review_list_url = reverse(
            "myapp:view_reviews", kwargs={"playground_id": self.playground.id}
        )

    # レビュー追加ビューのテスト
    def test_add_review_view(self):
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Review.objects.filter(user=self.user, playground=self.playground).exists()
        )

    # レビューリストビューのテスト
    def test_review_list_view(self):
        Review.objects.create(
            user=self.user, playground=self.playground, content="Nice!", rating=4
        )
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/view_reviews.html")
        self.assertEqual(len(response.context["reviews"]), 1)

    def test_review_displays_account_name(self):
        """口コミにアカウント名が表示されることをテスト"""
        self.client.login(email="testuser@example.com", password="testpassword")
        Review.objects.create(
            user=self.user, playground=self.playground, content="Test review", rating=5
        )

        # 初期状態（名無し）の確認 - コンテキスト内のデータを確認
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["reviews"][0].user.account_name, "testuser")

        # アカウント名変更後の確認 - ユーザーモデルの更新とコンテキスト内のデータを確認
        new_name = "テストユーザー"
        self.client.post(reverse("accounts:name_change"), {"account_name": new_name})

        # ユーザーモデルが更新されたことを確認
        self.user.refresh_from_db()
        self.assertEqual(self.user.account_name, new_name)

        # レビューリストを再取得し、コンテキスト内のデータを確認
        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["reviews"][0].user.account_name, new_name)

    def test_add_review_view_invalid_rating(self):
        """不正なratingでレビュー追加を試みると400エラーが返ることをテスト"""
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": "abc"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid rating")

    def test_reviews_ordered_by_created_at_descending(self):
        """レビューが投稿日時の新しい順に表示されることをテスト"""
        # ユーザーと公園はsetUpで作成済み
        # 異なるタイミングでレビューを作成
        review1 = Review.objects.create(
            user=self.user, playground=self.playground, content="Old review", rating=3
        )
        # created_atがreview1より後になるように少し待つ（テストの確実性を高めるため）
        # ただし、DjangoのTestCaseはトランザクションを使うため、実際にはcreated_atはほぼ同じになる可能性もある
        # そのため、ID順でソートされていないことを確認する
        review2 = Review.objects.create(
            user=self.user, playground=self.playground, content="New review", rating=5
        )

        response = self.client.get(self.review_list_url)
        self.assertEqual(response.status_code, 200)
        reviews_in_context = response.context["reviews"]

        # 新しいレビューが最初に表示されることを確認
        self.assertEqual(reviews_in_context[0].id, review2.id)
        self.assertEqual(reviews_in_context[1].id, review1.id)
