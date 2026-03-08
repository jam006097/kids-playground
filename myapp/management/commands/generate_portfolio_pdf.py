import os
from django.core.management.base import BaseCommand
from django.urls import reverse
from myapp.utils.portfolio_pdf_generator import BrowserOperator, PdfComposer
from myapp.models import Playground
from pathlib import Path


class Command(BaseCommand):
    help = "ローカル環境の各ページを巡回し、スクリーンショットをPDFにまとめます。"

    def add_arguments(self, parser):
        parser.add_argument(
            "--base-url",
            default="http://localhost:8000",
            help="撮影対象のベースURL（デフォルト: http://localhost:8000）",
        )
        parser.add_argument(
            "--output",
            default="portfolio.pdf",
            help="出力PDF名（デフォルト: portfolio.pdf）",
        )

    def handle(self, *args, **options):
        base_url = options["base_url"].rstrip("/")
        output_file = options["output"]

        # 1. 撮影対象URLの定義
        targets = [
            {"name": "index", "path": reverse("myapp:index")},
            {"name": "about", "path": reverse("myapp:about")},
            {"name": "ranking", "path": reverse("myapp:ranking")},
            {"name": "login", "path": "/accounts/login/"},
        ]

        # 存在する公園のIDを1つ取得して詳細ページを追加
        pg = Playground.objects.first()
        if pg:
            targets.append(
                {
                    "name": "facility_detail",
                    "path": reverse("myapp:facility_detail", args=[pg.pk]),
                }
            )
            targets.append(
                {
                    "name": "view_reviews",
                    "path": reverse("myapp:view_reviews", args=[pg.pk]),
                }
            )

        # ログインが必要なページ
        targets.append(
            {
                "name": "favorites",
                "path": reverse("myapp:favorites"),
                "require_login": True,
            }
        )
        targets.append(
            {"name": "mypage", "path": "/accounts/mypage/", "require_login": True}
        )

        # 2. 実行
        self.stdout.write(
            self.style.SUCCESS(f"Starting PDF generation from {base_url}...")
        )

        operator = BrowserOperator()
        composer = PdfComposer()
        temp_pdfs = []

        try:
            operator.start()

            # ログイン処理
            login_url = f"{base_url}/accounts/login/"
            # テスト用アカウント（必要に応じて環境変数化）
            test_email = os.getenv("TEST_USER_EMAIL", "test@test.com")
            test_password = os.getenv("TEST_USER_PASSWORD", "123")

            self.stdout.write(f"Logging in as {test_email}...")
            operator.login(login_url, test_email, test_password)

            # 各ページの撮影
            for target in targets:
                url = f"{base_url}{target['path']}"
                name = target["name"]
                temp_pdf = f"temp_{name}.pdf"

                self.stdout.write(f"Capturing {name}: {url}...")
                try:
                    operator.save_page_as_pdf(url, temp_pdf)
                    temp_pdfs.append(temp_pdf)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to capture {name}: {e}")
                    )

            # PDF結合
            self.stdout.write(
                self.style.SUCCESS(
                    f"Merging {len(temp_pdfs)} pages into {output_file}..."
                )
            )
            composer.merge(temp_pdfs, output_file)

        finally:
            operator.stop()
            # 一時ファイルの削除
            for f in temp_pdfs:
                if Path(f).exists():
                    os.remove(f)

        self.stdout.write(self.style.SUCCESS("Portfolio PDF generation complete!"))
