from unittest.mock import patch, MagicMock
from django.test import SimpleTestCase, override_settings

from myapp.clients.ai_summary_client import call_summary_api


@override_settings(AI_SUMMARY_API_URL="https://test-space.hf.space/")
class TestCallSummaryApi(SimpleTestCase):
    """
    AI要約APIクライアント `call_summary_api` のテスト (gradio_client版)
    """

    @patch("myapp.clients.ai_summary_client.Client")
    def test_成功時に要約テキストを返すこと(self, MockClient):
        """
        状況: Gradio Clientが正常に要約結果を返す。
        振る舞い: predictメソッドが呼ばれ、その結果が正しく返されること。
        """
        # 準備: mockの設定
        mock_instance = MockClient.return_value
        mock_instance.predict.return_value = "AIによる要約結果です。"

        # 実行
        summary = call_summary_api("これはテストの口コミです。")

        # 検証
        self.assertEqual(summary, "AIによる要約結果です。")
        MockClient.assert_called_once_with("https://test-space.hf.space/")
        mock_instance.predict.assert_called_once_with(
            "これはテストの口コミです。", api_name="/predict"
        )

    @patch("myapp.clients.ai_summary_client.Client")
    def test_API呼び出しで例外が発生する場合(self, MockClient):
        """
        状況: Gradio Clientのpredictメソッドが例外を発生させる。
        振る舞い: その例外がそのまま呼び出し元に伝播すること。
        """
        # 準備: mockの設定
        mock_instance = MockClient.return_value
        mock_instance.predict.side_effect = Exception("Gradio API Error")

        # 実行 & 検証
        with self.assertRaisesMessage(Exception, "Gradio API Error"):
            call_summary_api("エラーになるテキスト")
