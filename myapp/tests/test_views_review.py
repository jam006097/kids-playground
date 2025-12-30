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
        )  # type: ignore
        self.playground = Playground.objects.create(
            name="Test Park", address="Test Address", phone="123-456-7890"
        )
        self.add_review_url = reverse(
            "myapp:add_review", kwargs={"playground_id": self.playground.id}
        )

    def test_add_review_returns_created_review_json(self):
        """
        レビューを正常に投稿すると、作成されたレビューのJSONが返されることをテストする。
        """
        self.client.login(email="testuser@example.com", password="testpassword")
        post_data = {"content": "Great park!", "rating": 5}
        response = self.client.post(self.add_review_url, post_data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        response_data = response.json()
        self.assertEqual(response_data["status"], "success")

        self.assertIn("review", response_data)
        review_data = response_data["review"]

        self.assertEqual(review_data["content"], post_data["content"])
        self.assertEqual(review_data["rating"], post_data["rating"])
        self.assertEqual(review_data["user_account_name"], self.user.account_name)

        # Check if review exists in DB as a sanity check
        self.assertTrue(
            Review.objects.filter(
                user=self.user,
                playground=self.playground,
                content=post_data["content"],
            ).exists()
        )

    def test_add_review_view_invalid_rating(self):
        """不正なratingでレビュー追加を試みると400エラーが返ることをテスト"""
        self.client.login(email="testuser@example.com", password="testpassword")
        response = self.client.post(
            self.add_review_url, {"content": "Great park!", "rating": "abc"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid rating")


class ReviewListPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="password",
            account_name="テストユーザー",
        )  # type: ignore
        self.playground = Playground.objects.create(name="Review List Park")
        # Create 15 reviews for pagination testing (10 on page 1, 5 on page 2)
        for i in range(15):
            Review.objects.create(
                playground=self.playground,
                user=self.user,
                content=f"List Review {i + 1}",
                rating=3,
            )
        self.review_list_url = reverse(
            "myapp:view_reviews", kwargs={"playground_id": self.playground.id}
        )

    def test_review_list_page_displays_first_page(self):
        """レビュー一覧ページが最初のページを正しく表示し、次のページへのリンクがあることをテストする。"""
        response = self.client.get(self.review_list_url, {"page": 1})
        view_reviews_url = reverse(
            "myapp:view_reviews", kwargs={"playground_id": self.playground.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "List Review 15")  # Newest first
        self.assertContains(response, "List Review 6")
        self.assertNotContains(response, "List Review 5")  # Should be on next page

        # Check for pagination links
        self.assertContains(
            response,
            f'<a class="page-link" href="{view_reviews_url}'
            f'?page=2" aria-label="次へ">',
        )
        self.assertNotContains(
            response,
            (
                f'<a class="page-link" href="{view_reviews_url}'
                f'?page=0" aria-label="前へ">'
            ),
        )  # Ensure no active previous link
        self.assertNotContains(
            response,
            (
                '<li class="page-item disabled"><span class="page-link" aria-hidden="true">'
                "&laquo;</span>"
            ),
            html=True,
        )

    def test_review_list_page_displays_second_page(self):
        """レビュー一覧ページが2ページ目を正しく表示し、前後のページへのリンクがあることをテストする。"""
        response = self.client.get(self.review_list_url, {"page": 2})
        view_reviews_url = reverse(
            "myapp:view_reviews", kwargs={"playground_id": self.playground.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "List Review 5")
        self.assertContains(response, "List Review 1")
        self.assertNotContains(response, "List Review 6")  # Should be on previous page

        # Check for pagination links
        self.assertContains(
            response,
            f'<a class="page-link" href="{view_reviews_url}'
            f'?page=1" aria-label="前へ">',
        )
        self.assertNotContains(
            response,
            (
                f'<a class="page-link" href="{view_reviews_url}'
                f'?page=3" aria-label="次へ">'
            ),
        )  # Ensure no active next link
        self.assertNotContains(
            response,
            (
                '<li class="page-item disabled"><span class="page-link" aria-hidden="true">'
                "&raquo;</span>"
            ),
            html=True,
        )

    def test_review_list_page_invalid_page_returns_404(self):
        """レビュー一覧ページで無効なページ番号が指定された場合に404が返されることをテストする。"""
        response = self.client.get(self.review_list_url, {"page": 99})
        self.assertEqual(response.status_code, 404)
