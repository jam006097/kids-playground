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
- **AIチャット**: 遊び場探しや子育てに関する相談ができるAIチャットボット機能
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

## ローカル開発環境セットアップ

このプロジェクトでは、コード編集はローカルのPython仮想環境（`venv`）で行い、アプリケーションの実行やテストはDockerコンテナで行うハイブリッドな開発スタイルを推奨しています。

### ステップ1: コード編集環境のセットアップ (`venv`)

まず、コードの補完や静的解析をエディタで有効にするため、ローカルにPythonの仮想環境を構築します。

1.  **リポジトリをクローン**
    ```bash
    git clone https://github.com/jam006097/kidsPlayGround.git
    cd kidsPlayGround
    ```

2.  **Python仮想環境の作成と有効化**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *Windowsの場合は `venv\Scripts\activate` を実行してください。*

3.  **依存パッケージのインストール**
    ```bash
    pip install -r requirements.txt
    ```

4.  **pre-commitフックのセットアップ**
    コミット前にコード品質チェックを自動実行するための設定です。
    ```bash
    pre-commit install
    ```

5.  **フロントエンド依存関係のインストール**
    コードフォーマッターなどに使用します。
    ```bash
    npm install
    ```

6.  **エディタの設定**
    お使いのエディタ（VSCodeなど）で、作成した`venv`内のPythonインタープリタ（例: `venv/bin/python`）を選択してください。これにより、コードの自動補完やエラーチェックが正しく機能します。


### ステップ2: テスト・実行環境のセットアップ (Docker)

次に、アプリケーションの実際の動作確認やテストを行うためのDocker環境をセットアップします。

1.  **環境変数の設定**
    リポジトリのルートにある `.env.example` ファイルをコピーして `.env` ファイルを作成します。
    ```bash
    cp .env.example .env
    ```
    `.env` ファイルには、開発用のデータベース接続情報やDjangoの`SECRET_KEY`などが含まれています。必要に応じて内容を編集してください。

2.  **Dockerコンテナの起動**
    Docker Composeを使って、DjangoアプリケーションとPostgreSQLデータベースのコンテナをビルドし、バックグラウンドで起動します。
    ```bash
    docker-compose up -d --build
    ```
    - 初回起動時は、Dockerイメージのビルドに時間がかかることがあります。
    - `db`、`ai-api`、`web` の3つのサービスが起動します。

3.  **データベースの初期化**
    コンテナ内でマイグレーションを実行し、データベースのテーブルを作成します。
    ```bash
    docker-compose exec -T web python manage.py migrate
    ```

4.  **管理者ユーザーの作成**
    アプリケーションにログインするための管理者（スーパーユーザー）を作成します。このコマンドは対話形式のため、ご自身のターミナルで実行してください。
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **アプリケーションへのアクセス**
    セットアップが完了したら、ブラウザで [http://localhost:8000](http://localhost:8000) にアクセスします。

### コンテナの停止
```bash
docker-compose down
```
- `-v` オプションを付けて `docker-compose down -v` を実行すると、データベースのボリュームも削除されます。

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
