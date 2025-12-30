from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from myapp.models import Playground, Review
from myapp.forms import ReviewForm  # ReviewFormをインポート

User = get_user_model()


class ReviewViewsTest(TestCase):
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


class ReviewCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser2@example.com",
            password="testpassword2",
            account_name="testuser2",
        )
        self.playground = Playground.objects.create(
            name="Create Review Park", address="Create Address", phone="098-765-4321"
        )
        self.review_create_url = reverse(
            "myapp:review_create", kwargs={"pk": self.playground.pk}
        )

    def test_unauthenticated_user_redirected_to_login(self):
        """未認証ユーザーはレビュー作成ページにアクセスするとログインページにリダイレクトされること。"""
        response = self.client.get(self.review_create_url)
        self.assertRedirects(
            response, f"/accounts/login/?next={self.review_create_url}"
        )

    def test_authenticated_user_accesses_review_create_page(self):
        """認証済みユーザーはレビュー作成ページにアクセスでき、正しいテンプレートとコンテキストがレンダリングされること。"""
        self.client.login(email="testuser2@example.com", password="testpassword2")
        response = self.client.get(self.review_create_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reviews/review_form.html")

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], ReviewForm)
        self.assertFalse(response.context["form"].is_bound)  # フォームは空であるべき

        self.assertIn("playground", response.context)
        self.assertEqual(response.context["playground"], self.playground)

    def test_authenticated_user_can_submit_review(self):
        """認証済みユーザーは有効なレビューを投稿でき、詳細ページにリダイレクトされること。"""
        self.client.login(email="testuser2@example.com", password="testpassword2")
        review_count_before = Review.objects.count()

        post_data = {
            "content": "This is a great playground!",
            "rating": 5,
        }
        response = self.client.post(self.review_create_url, post_data)

        self.assertEqual(Review.objects.count(), review_count_before + 1)
        new_review = Review.objects.latest("id")
        self.assertEqual(new_review.content, post_data["content"])
        self.assertEqual(new_review.rating, post_data["rating"])
        self.assertEqual(new_review.playground, self.playground)
        self.assertEqual(new_review.user, self.user)

        expected_redirect_url = reverse(
            "myapp:facility_detail", kwargs={"pk": self.playground.pk}
        )
        self.assertRedirects(response, expected_redirect_url)

    def test_authenticated_user_cannot_submit_invalid_review(self):
        """認証済みユーザーは無効なレビューを投稿できず、フォームエラーが表示されること。"""
        self.client.login(email="testuser2@example.com", password="testpassword2")
        review_count_before = Review.objects.count()

        # contentが欠けている無効なデータ
        post_data = {
            "content": "",  # 必須フィールドを空にする
            "rating": 3,
        }
        response = self.client.post(self.review_create_url, post_data)

        self.assertEqual(
            response.status_code, 200
        )  # フォームエラーで同じページが再表示されるため200
        self.assertTemplateUsed(response, "reviews/review_form.html")
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertTrue(form.errors)  # エラーがあることを確認
        self.assertIn(
            "content", form.errors
        )  # contentフィールドにエラーがあることを確認

        self.assertEqual(
            Review.objects.count(), review_count_before
        )  # レビューが作成されていないことを確認
