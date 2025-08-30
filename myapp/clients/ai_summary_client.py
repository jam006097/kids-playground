import requests
from django.conf import settings


def call_summary_api(text: str) -> str:
    """
    AI要約APIを呼び出し、要約テキストを返す

    Args:
        text: 要約対象のテキスト

    Returns:
        要約されたテキスト

    Raises:
        requests.Timeout: APIがタイムアウトした場合
        requests.HTTPError: APIがエラーレスポンスを返した場合
    """
    response = requests.post(
        settings.AI_SUMMARY_API_URL,
        json={"data": [text]},
        timeout=settings.AI_SUMMARY_API_TIMEOUT,
    )
    response.raise_for_status()  # 200番台以外のステータスコードで例外を発生させる

    response_data = response.json()
    return response_data["data"][0]
