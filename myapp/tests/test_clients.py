from unittest.mock import patch
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
        mock_instance.predict.return_value = ["AIによる要約結果です。"]

        # 実行
        summary = call_summary_api("これはテストの口コミです。")

        # 検証
        self.assertEqual(summary, "AIによる要約結果です。")
        MockClient.assert_called_once_with("https://test-space.hf.space/", auth=None)
        mock_instance.predict.assert_called_once_with(
            "これはテストの口コミです。", api_name="/predict"
        )

    @patch("myapp.clients.ai_summary_client.Client")
    def test_API呼び出しで例外が発生する場合(self, MockClient):
        """
        状況: Gradio Clientのpredictメソッドが例外を発生させる。
        振る舞い: RuntimeErrorが送出され、メッセージが正しいこと。
        """
        # 準備: mockの設定
        mock_instance = MockClient.return_value
        mock_instance.predict.side_effect = Exception("Gradio API Error")

        # 実行 & 検証
        with self.assertRaisesMessage(
            RuntimeError, "AI要約の取得中にエラーが発生しました。"
        ):
            call_summary_api("エラーになるテキスト")

    @override_settings(AI_SUMMARY_API_KEY="test_api_key")
    @patch("myapp.clients.ai_summary_client.Client")
    def test_APIキーが設定されている場合にauthが渡されること(self, MockClient):
        """
        状況: settingsにAI_SUMMARY_API_KEYが設定されている。
        振る舞い: Clientの初期化時にauthタプルが渡されること。
        """
        # 準備: mockの設定
        mock_instance = MockClient.return_value
        mock_instance.predict.return_value = ["Success"]

        # 実行
        call_summary_api("テストテキスト")

        # 検証
        MockClient.assert_called_once_with(
            "https://test-space.hf.space/", auth=("gemini", "test_api_key")
        )
