from playwright.sync_api import sync_playwright
from pathlib import Path
from pypdf import PdfWriter


class BrowserOperator:
    """
    Playwright を使用してブラウザ操作を行うクラス。
    """

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        """ブラウザの起動"""
        if not self.playwright:
            self.playwright = sync_playwright().start()
        if not self.browser:
            self.browser = self.playwright.chromium.launch()
        if not self.context:
            self.context = self.browser.new_context()
        if not self.page:
            self.page = self.context.new_page()

    def stop(self):
        """ブラウザの終了"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.browser = None
        self.playwright = None
        self.context = None
        self.page = None

    def save_page_as_pdf(self, url: str, output_path: str):
        """指定したURLをPDFとして保存する"""
        if not self.page:
            self.start()
        self.page.goto(url)
        # ページのレンダリング待ち
        self.page.wait_for_timeout(1000)
        self.page.pdf(path=output_path, format="A4")

    def login(self, login_url: str, email: str, password: str):
        """指定したURLでログインする"""
        if not self.page:
            self.start()
        self.page.goto(login_url)
        self.page.fill('input[name="login"]', email)
        self.page.fill('input[name="password"]', password)
        self.page.click('button[type="submit"]')
        # ログイン後の遷移待ち
        self.page.wait_for_load_state("networkidle")


class PdfComposer:
    """
    複数のPDFファイルを結合するクラス。
    """

    def merge(self, input_paths: list, output_path: str):
        """複数のPDFを結合して出力する"""
        merger = PdfWriter()
        for pdf in input_paths:
            if Path(pdf).exists():
                merger.append(pdf)
        merger.write(output_path)
        merger.close()
