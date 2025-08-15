# 児童支援施設ポートフォリオ

## 概要
児童支援施設の一覧表示・地図表示・会員登録・お気に入り登録などができるWebアプリケーションです。

- サイトURL: https://jam006097.pythonanywhere.com/

## 環境変数の設定
Google Mapsの地図表示機能を利用するため、Google Maps APIキーが必要です。

1. プロジェクトルートに`.env`ファイルを作成し、以下のように記載してください。
   ```env
    SECRET_KEY=Django_YOUR_SECRET_KEY
    GOOGLE_MAPS_API_KEY=your_google_maps_api_key
    DB_PASSWORD=your_db_password
   ```
2. APIキーはGoogle Cloud Platformで取得できます。
3. `.env`ファイルはセキュリティのため、必ず.gitignoreに追加してください。

## 主な機能

- **施設情報**こどもがあそべる施設情報を一覧・地図で表示
- **検索**: 住所や施設名での検索
- **口コミ**: 施設ごとの口コミ投稿・表示
- **お気に入り**: 気になる施設をお気に入り登録
- **ランキング**: 口コミの評価/件数に基づいた施設ランキング
- **ユーザー認証**: 会員登録、ログイン・ログアウト

## 技術スタック
- 言語: Python, JavaScript, HTML, CSS
- フレームワーク: Django, Bootstrap
- データベース: MySQL
- ソース管理: Git, GitHub

## セットアップ手順
1. リポジトリをクローン
   ```bash
   git clone https://github.com/jam006097/kidsPlayGround.git
   cd kidsPlayGround
   ```
2. 仮想環境の作成・有効化
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. 依存パッケージのインストール
   ```bash
   pip install -r requirements.txt
   ```
4. DB設定（`settings/base.py`などでMySQL接続情報を設定）
5. マイグレーション実行
   ```bash
   python manage.py migrate
   ```
6. サーバー起動
   ```bash
   python manage.py runserver
   ```

## ディレクトリ構成
- `myapp/` ... アプリ本体
- `mysite/` ... プロジェクト設定
- `static/` ... 静的ファイル
- `templates/` ... テンプレート

## 開発・運用
- コード整形: `black`, `flake8` など推奨
- テスト: `python manage.py test`
- デプロイ: pythonanywhere など

## ライセンス
このプロジェクトはMITライセンスです。

## 作者
- jam006097
- お問い合わせ: GitHubのIssueまたはメールでご連絡ください。
