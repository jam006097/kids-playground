from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class SearchPlaceViewTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.url = reverse("search_place")

    # 場所検索ビューが成功するケースのテスト
    @patch("myapp.views.urllib.request.urlopen")
    def test_search_place_view_success(self, mock_urlopen):
        # Google Places APIからのレスポンスをモック
        class MockResponse:
            def read(self):
                return b'{"candidates": [{"formatted_address": "Test Address", "name": "Test Place"}]}'

            def __enter__(self, *args, **kwargs):
                return self

            def __exit__(self, *args, **kwargs):
                pass

        mock_urlopen.return_value = MockResponse()

        response = self.client.get(
            self.url,
            {"name": "Test Place", "address": "Test Address", "phone": "123-456-7890"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"url": "https://www.google.com/maps/search/?api=1&query=Test%20Place"},
        )

    # 場所検索ビューで候補が見つからないケースのテスト
    @patch("myapp.views.urllib.request.urlopen")
    def test_search_place_view_not_found(self, mock_urlopen):
        # Google Places APIからのレスポンスをモック（候補なし）
        class MockResponse:
            def read(self):
                return b'{"candidates": []}'

            def __enter__(self, *args, **kwargs):
                return self

            def __exit__(self, *args, **kwargs):
                pass

        mock_urlopen.return_value = MockResponse()

        response = self.client.get(
            self.url,
            {"name": "Test Place", "address": "Test Address", "phone": "123-456-7890"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content, {"error": "No matching candidates found"}
        )
