from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from myapp.models import Playground, Review
from users.models import CustomUser


class TestSummarizeReviewsView(TestCase):
    """
    AI要約ビュー `SummarizeReviewsView` のテスト
    """

    @classmethod
    def setUpTestData(cls):
        """テスト全体で使う基本的なデータを作成"""
        cls.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password"
        )
        cls.playground = Playground.objects.create(
            name="テストの公園", prefecture="東京都", address="テスト住所"
        )
        # 3件の口コミを作成 (合計300文字以上)
        long_content = "あ" * 100
        Review.objects.create(
            playground=cls.playground,
            user=cls.user,
            content=f"口コミ1 {long_content}",
            rating=5,
        )
        Review.objects.create(
            playground=cls.playground,
            user=cls.user,
            content=f"口コミ2 {long_content}",
            rating=3,
        )
        Review.objects.create(
            playground=cls.playground,
            user=cls.user,
            content=f"口コミ3 {long_content}",
            rating=5,
        )

    def test_存在しない施設IDの場合は404を返すこと(self):
        """
        状況: 存在しないplayground_idでURLにアクセスする。
        振る舞い: 404 Not Foundが返されること。
        """
        url = reverse("myapp:summarize_reviews", kwargs={"playground_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @patch("myapp.views.summary_views.call_summary_api")
    def test_API連携が成功し要約が返されること(self, mock_call_api):
        """
        状況: AI要約APIが正常に要約文を返す。
        振る舞い: ビューが200 OKを返し、JSONに要約が含まれていること。
        """
        mock_call_api.return_value = "AIによる要約結果です。"
        url = reverse(
            "myapp:summarize_reviews", kwargs={"playground_id": self.playground.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"summary": "AIによる要約結果です。"})
        mock_call_api.assert_called_once()

    def test_口コミが3件未満の場合は400エラーを返すこと(self):
        """
        状況: 対象施設の口コミが2件しかない。
        振る舞い: APIを呼び出さず、400 Bad Requestとエラーメッセージを返すこと。
        """
        # 口コミが2件の新しい施設を作成
        playground_less_reviews = Playground.objects.create(name="口コミ少ない公園")
        Review.objects.create(
            playground=playground_less_reviews,
            user=self.user,
            content="a" * 150,
            rating=5,
        )
        Review.objects.create(
            playground=playground_less_reviews,
            user=self.user,
            content="b" * 150,
            rating=5,
        )

        url = reverse(
            "myapp:summarize_reviews",
            kwargs={"playground_id": playground_less_reviews.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content, {"error": "口コミが3件未満のため、要約できません。"}
        )

    def test_口コミ合計が300文字未満の場合は400エラーを返すこと(self):
        """
        状況: 口コミは3件あるが、合計文字数が300文字未満。
        振る舞い: APIを呼び出さず、400 Bad Requestとエラーメッセージを返すこと。
        """
        # 文字数が少ない口コミを持つ新しい施設を作成
        playground_short_reviews = Playground.objects.create(name="文字少ない公園")
        Review.objects.create(
            playground=playground_short_reviews,
            user=self.user,
            content="短い口コミ1",
            rating=5,
        )
        Review.objects.create(
            playground=playground_short_reviews,
            user=self.user,
            content="短い口コミ2",
            rating=5,
        )
        Review.objects.create(
            playground=playground_short_reviews,
            user=self.user,
            content="短い口コミ3",
            rating=5,
        )

        url = reverse(
            "myapp:summarize_reviews",
            kwargs={"playground_id": playground_short_reviews.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "口コミの合計文字数が300文字未満のため、要約できません。"},
        )

    @patch(
        "myapp.views.summary_views.call_summary_api", side_effect=Exception("API Error")
    )
    def test_API呼び出しで例外が発生した場合500エラーを返すこと(self, mock_call_api):
        """
        状況: APIクライアントの呼び出しで予期せぬ例外が発生する。
        振る舞い: 500 Internal Server Errorと汎用的なエラーメッセージを返すこと。
        """
        url = reverse(
            "myapp:summarize_reviews", kwargs={"playground_id": self.playground.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(
            response.content, {"error": "サーバーでエラーが発生しました。"}
        )
