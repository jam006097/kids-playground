import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page


class FrontendJsModuleLoadTest(StaticLiveServerTestCase):
    """
    フロントエンドの JS モジュールが 404 にならないことを保証するテスト。
    """

    host = "127.0.0.1"
    port = 8081

    def setUp(self):
        super().setUp()

        # Playwright 起動
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page: Page = self.browser.new_page()

        # 404 をここに集約
        self.js_404_errors: list[str] = []

        # レスポンスイベントで 404 を検出
        self.page.on("response", self._record_js_404)

    def tearDown(self):
        # 終了処理
        self.page.close()
        self.browser.close()
        self.playwright.stop()
        super().tearDown()

    # ---- Helper ----

    def _record_js_404(self, response):
        """
        JS ファイルの 404 を検出して記録する。
        余計なフィルタリングはせず、「JS の 404」だけに責務を限定する。
        """
        if response.status == 404 and response.url.endswith(".js"):
            self.js_404_errors.append(response.url)

    # ---- Test ----

    def test_frontend_js_modules_should_not_404(self):
        """
        フロントエンド JS モジュールのロードに 404 が発生しないこと。
        """

        # When: ページを開く
        self.page.goto(self.live_server_url + "/")

        # ネットワークが落ち着くまで待つ（JS modules の読み込み待ち）
        self.page.wait_for_load_state("networkidle")

        # Then: JS の 404 が発生していないこと
        assert (
            not self.js_404_errors
        ), "JS モジュールのロードに 404 が発生しています:\n" + "\n".join(
            self.js_404_errors
        )
