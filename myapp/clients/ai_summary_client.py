from gradio_client import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


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
    api_key = getattr(settings, "AI_SUMMARY_API_KEY", None)
    auth = ("gemini", api_key) if api_key else None

    try:
        logger.debug(f"Connecting to Gradio API at {settings.AI_SUMMARY_API_URL}")
        client = Client(
            settings.AI_SUMMARY_API_URL,
            auth=auth,
        )
        logger.debug("Calling predict API...")
        result = client.predict(text, api_name="/predict")
        logger.debug("Successfully received summary from API.")
        # Gradio Clientのバージョンによって返り値の型が異なる可能性があるため、
        # 想定されるデータ構造からテキストを抽出する
        if isinstance(result, (list, tuple)) and len(result) > 0:
            summary = result[0]
        elif isinstance(result, str):
            summary = result
        else:
            raise TypeError(f"Unexpected response type from AI API: {type(result)}")

        return summary

    except Exception as e:
        logger.exception(f"Error calling AI summary API: {e}")
        raise RuntimeError("AI要約の取得中にエラーが発生しました。")
