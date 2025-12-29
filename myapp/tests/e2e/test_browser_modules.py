import pytest
from playwright.sync_api import Page


@pytest.mark.e2e
def test_frontend_js_modules_should_not_404(live_server, page: Page):
    """
    フロントエンド JS モジュールのロードに 404 が発生しないこと。
    """
    js_404_errors: list[str] = []

    def _record_js_404(response):
        if response.status == 404 and response.url.endswith(".js"):
            js_404_errors.append(response.url)

    page.on("response", _record_js_404)

    # When: ページを開く
    page.goto(live_server.url + "/")

    # ネットワークが落ち着くまで待つ（JS modules の読み込み待ち）
    page.wait_for_load_state("networkidle")

    # Then: JS の 404 が発生していないこと
    assert (
        not js_404_errors
    ), "JS モジュールのロードに 404 が発生しています:\n" + "\n".join(js_404_errors)
