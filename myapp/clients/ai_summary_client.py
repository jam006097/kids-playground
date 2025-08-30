from gradio_client import Client
from django.conf import settings


def call_summary_api(text: str) -> str:
    """
    AI要約APIを呼び出し、要約テキストを返す

    Args:
        text: 要約対象のテキスト

    Returns:
        要約されたテキスト

    Raises:
        Exception: API呼び出しでエラーが発生した場合
    """
    try:
        client = Client(settings.AI_SUMMARY_API_URL)
        # predictのapi_nameはHugging Face SpaceのGradioアプリで定義されたものに依存します。
        # 一般的には`/predict`ですが、確認が必要です。ここでは仮に`/predict`とします。
        result = client.predict(text, api_name="/predict")
        return result
    except Exception as e:
        # エラーロギングなどをここに追加することが望ましい
        raise e
