# 親子で遊ぼうナビ - 子供が遊べる施設のまとめサイト

## 概要
子供が遊べる施設や子育て支援施設を検索・表示し、お気に入り登録や口コミ投稿ができるWebアプリケーションです。

- サイトURL: https://jam006097.pythonanywhere.com/



## 主な機能

- **施設情報**: 全国の公園、児童館、子育て支援センターなど、子供が遊べる施設情報を一覧・地図で表示
- **検索**: 住所や施設名での検索
- **口コミ**: 施設ごとの口コミ投稿・表示、Hugging Face Spacesを活用したAIによる口コミ要約機能
- **お気に入り**: 気になる施設をお気に入り登録
- **ランキング**: 口コミの評価/件数に基づいた施設ランキング
- **ユーザー認証**: 会員登録、ログイン・ログアウト

## 技術スタック
- 言語: Python, JavaScript, HTML, CSS
- フレームワーク: Django, Bootstrap
- データベース: PostgreSQL
- コンテナ化: Docker
- AI要約API: Hugging Face Spaces
- CI/CD: GitHub Actions
- コード品質: Pytest, Flake8, Black, Mypy, pre-commit
- ソース管理: Git, GitHub

## セットアップ手順
1. リポジトリをクローン
   ```bash
   git clone https://github.com/jam006097/kidsPlayGround.git
   cd kidsPlayGround
   ```
2. Docker Composeでサービスを起動 (推奨)
   ```bash
   docker-compose up -d --build
   ```
   - これにより、PostgreSQLデータベースとDjangoアプリケーションがDockerコンテナとして起動します。
   - 初回起動時はイメージのビルドに時間がかかります。
3. 仮想環境の作成・有効化 (Dockerを使用しない場合)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. 依存パッケージのインストール (Dockerを使用しない場合)
   ```bash
   pip install -r requirements.txt
   ```
5. DB設定（.envファイルに DATABASE_URL を設定。例: DATABASE_URL="postgres://user:password@host:port/dbname"）
   - Docker Composeを使用する場合は、`docker-compose.yml`内の`db`サービスが自動で設定を読み込みます。
6. マイグレーション実行
   ```bash
   python manage.py migrate
   ```
   - Docker Composeを使用する場合は、`docker-compose exec web python manage.py migrate` を実行します。
7. サーバー起動 (Dockerを使用しない場合)
   ```bash
   python manage.py runserver
   ```
8. pre-commitフックのセットアップ
   ```bash
   pre-commit install
   ```
   - 仮想環境を有効にした状態で実行してください。
   - Docker Composeを使用する場合は、`docker-compose exec web pre-commit install` を実行します。

## ディレクトリ構成
- `myapp/` ... アプリ本体
- `mysite/` ... プロジェクト設定
- `static/` ... 静的ファイル
- `templates/` ... テンプレート

## 開発・運用
- コード整形: `black`, `flake8` など推奨
- テスト: `python manage.py test`
- CI/CD: GitHub Actionsによる自動テストとデプロイ
- デプロイ: pythonanywhere など

## ライセンス
このプロジェクトはMITライセンスです。

## 作者
- jam006097
- お問い合わせ: GitHubのIssueまたはメールでご連絡ください。
