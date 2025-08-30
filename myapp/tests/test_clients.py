import pytest
import requests
from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase, override_settings

from myapp.clients.ai_summary_client import call_summary_api


@override_settings(
    AI_SUMMARY_API_URL="http://test-api.com/api/predict/", AI_SUMMARY_API_TIMEOUT=10
)
class TestCallSummaryApi(SimpleTestCase):
    """
    AI要約APIクライアント `call_summary_api` のテスト
    """

    @patch("myapp.clients.ai_summary_client.requests.post")
    def test_成功時に要約テキストを返すこと(self, mock_post):
        """
        状況: AI要約APIが正常に成功レスポンスを返却する。
        振る舞い: APIから返された要約テキストを正しく返すこと。
        """
        # 準備: mockの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": ["これが要約されたテキストです。"],
            "duration": 1.5,
        }
        mock_post.return_value = mock_response

        # 実行
        summary = call_summary_api("これはテストの口コミです。")

        # 検証
        self.assertEqual(summary, "これが要約されたテキストです。")
        mock_post.assert_called_once_with(
            "http://test-api.com/api/predict/",
            json={"data": ["これはテストの口コミです。"]},
            timeout=10,
        )

    @patch("myapp.clients.ai_summary_client.requests.post")
    def test_タイムアウト時に例外を送出すること(self, mock_post):
        """
        状況: APIへのリクエストがタイムアウトする。
        振る舞い: `requests.Timeout` 例外を適切に送出すること。
        """
        # 準備: mockの設定
        mock_post.side_effect = requests.Timeout

        # 実行 & 検証
        with self.assertRaises(requests.Timeout):
            call_summary_api("タイムアウトするテキスト")

    @patch("myapp.clients.ai_summary_client.requests.post")
    def test_サーバーエラー時に例外を送出すること(self, mock_post):
        """
        状況: APIが500エラーなど、サーバー側のエラーを返す。
        振る舞い: `requests.HTTPError` 例外を適切に送出すること。
        """
        # 準備: mockの設定
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.HTTPError
        mock_post.return_value = mock_response

        # 実行 & 検証
        with self.assertRaises(requests.HTTPError):
            call_summary_api("サーバーエラーになるテキスト")
