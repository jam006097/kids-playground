# Issue: ポートフォリオ用スクリーンショットPDF生成コマンドの実装 (DONE)

## 1. 目的
ローカル開発環境での動作を証明するため、主要なWebページを自動巡回し、1つのPDFにまとめるDjangoコマンド `generate_portfolio_pdf` を実装する。

## 2. 完了条件
- [x] `pypdf` が依存関係に追加されていること。
- [x] `python manage.py generate_portfolio_pdf` を実行すると、`portfolio.pdf` が生成されること。
- [x] 生成されたPDFに、ログイン必須ページ（マイページ等）が含まれていること。
- [x] 全てのテストがパスし、`flake8`, `mypy` のチェックをクリアしていること。

## 3. 範囲
- `myapp/management/commands/generate_portfolio_pdf.py` の新規作成。
- ページ巡回、ログイン処理、PDF結合の各クラス実装。
- 上記を検証する TDD ベースのテストコード。

## 4. 方針
- `Playwright` の同期 API を使用。
- `pypdf` による PDF 結合。
- SOLID原則に基づき、コマンド、ブラウザ操作、PDF合成の責務を分離。

## 5. 振り返り (Check, Act)
- **Check:** Playwright を使用することで、JavaScriptによる動的なレンダリングも正確にキャプチャできた。TDDにより、依存関係のモック化も含めて堅牢なコードを構築できた。
- **Act:** ログイン情報はテンプレートに記載されていたテスト用アカウントを使用したが、セキュリティを考慮し環境変数から取得する構造にした。今後のポートフォリオ作成において、このコマンドは非常に強力なツールとなる。
