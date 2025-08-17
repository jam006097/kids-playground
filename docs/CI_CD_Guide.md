# Docker, Render, GitHub Actions を用いた CI/CD ガイド

このドキュメントは、DjangoアプリケーションをDocker化し、GitHub ActionsでCI/CDパイプラインを構築し、Renderにデプロイするまでの手順と、特に注意すべき点やハマりどころをまとめたものです。

## 1. 全体像と技術スタック

*   **アプリケーション**: Django (Python)
*   **コンテナ化**: Docker
*   **CI/CD**: GitHub Actions
*   **デプロイ先**: Render (PaaS)
*   **データベース**: PostgreSQL (Render Managed Service)
*   **コンテナレジストリ**: GitHub Container Registry (GHCR)

## 2. 事前準備

### 2.1 GitHubリポジトリの作成

*   リポジトリ名は**すべて小文字**で作成することを強く推奨します（例: `kids-playground`）。大文字が含まれると、Dockerイメージのタグ付けなどで問題が発生する可能性があります。

### 2.2 Renderアカウントの作成とPostgreSQLデータベースのプロビジョニング

*   Renderでアカウントを作成し、新しいPostgreSQLデータベースサービスをプロビジョニングします。
*   データベースの「Internal Connection String」を控えておきます。これは後で`DATABASE_URL`として使用します。

### 2.3 GitHub Secretsの設定

以下のシークレットをGitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」に登録します。

*   `DJANGO_SECRET_KEY`: Djangoの`SECRET_KEY`。
*   `RENDER_API_KEY`: RenderのAPIキー。
*   `GHCR_PAT`: GitHub Container Registryへのプッシュ権限を持つPersonal Access Token (PAT)。
    *   PAT作成時、`write:packages`と`read:packages`スコープにチェックを入れてください。`repo`スコープも広範ですが確実です。

## 3. プロジェクトのDocker化

### 3.1 `Dockerfile`の作成

プロジェクトのルートに`Dockerfile`を作成します。

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 起動スクリプトをコピーし、実行権限を与える
COPY start.sh /app/
RUN chmod +x /app/start.sh

RUN python manage.py collectstatic --noinput

# アプリケーションの起動はstart.shに任せる
CMD ["/app/start.sh"]
```

### 3.2 `start.sh`の作成

プロジェクトのルートに`start.sh`を作成します。このスクリプトは、デプロイ時にデータベースマイグレーションを実行し、その後Gunicornを起動します。

```bash
#!/bin/bash

# データベースのマイグレーションを実行
# Renderの無料枠ではPre-Deploy Commandが使えないため、起動時に実行する
# /usr/local/bin/python はコンテナ内のPython実行ファイルのフルパス
/usr/local/bin/python manage.py migrate

# Gunicornを起動
/usr/local/bin/python -m gunicorn --bind 0.0.0.0:$PORT mysite.wsgi:application
```

**💡ハマりどころと工夫点:**
*   **`gunicorn: command not found`**: `gunicorn`が`PATH`にない場合、`python -m gunicorn`のようにPythonモジュールとして実行すると解決します。
*   **`python: No such file or directory`**: `python`のフルパスが`/usr/local/bin/python`であることを確認してください。`python:3.11-slim`イメージではこのパスです。
*   **`manage.py migrate`の実行タイミング**: Renderの無料枠では`Pre-Deploy Command`が使えないため、`Dockerfile`の`RUN`ステップでマイグレーションを実行しようとすると、ビルド時にデータベース接続が必要になったり、`manage.py`がコピーされる前でエラーになったりします。最終的に、**アプリケーションの起動スクリプト（`start.sh`）にマイグレーションを含める**ことで解決しました。これにより、アプリケーションが起動するたびにマイグレーションが実行されます（本番環境では注意が必要な点ですが、無料枠の制約下でのワークアラウンドです）。

### 3.3 `.dockerignore`の作成

Dockerイメージに含める必要のないファイルやディレクトリを指定します。

```
.git/
.venv/
venv/
__pycache__/
*.pyc
*.log
.env
node_modules/
```

## 4. Django設定の更新

### 4.1 `mysite/settings/base.py`

`DATABASE_URL`と`SECRET_KEY`を環境変数から読み込むように設定します。

```python
# mysite/settings/base.py

import os
from dotenv import load_dotenv
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env")) # ローカル開発用

SECRET_KEY = os.getenv("SECRET_KEY")

# ...

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# WhiteNoiseの設定を追加 (静的ファイル配信のため)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # この行を追加
    "django.contrib.sessions.middleware.SessionMiddleware",
    # ...
]

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # この行を追加
```

### 4.2 `mysite/settings/dev.py`

MySQLのハードコードされた設定を削除し、`base.py`から継承するようにします。

```python
# mysite/settings/dev.py

from .base import *
import os
import sys

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# DATABASESブロックはbase.pyから継承するため削除

# ...
```

### 4.3 `mysite/settings/prod.py`

Renderのドメインを`ALLOWED_HOSTS`に追加し、`dj_database_url`を明示的にインポートします。

```python
# mysite/settings/prod.py

from .base import *
import os
import dj_database_url # この行を追加

DEBUG = False
ALLOWED_HOSTS = ["kidsplayground.onrender.com"] # Renderのドメインに置き換える

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}

# ...
```

## 5. 依存関係の更新

### 5.1 `requirements.txt`

以下のライブラリを追加・更新します。

*   `psycopg2-binary`: PostgreSQL接続用
*   `dj-database-url`: `DATABASE_URL`環境変数解析用
*   `gunicorn`: Webサーバー
*   `whitenoise`: 静的ファイル配信
*   `pytest-dotenv`: ローカルテストで`.env`を自動読み込み

```
# requirements.txt

# ... 既存のライブラリ ...

psycopg2-binary==2.9.9
dj-database-url==2.1.0
gunicorn==22.0.0
whitenoise==6.7.0
pytest-dotenv==0.5.2
```

### 5.2 ローカルでのインストール

仮想環境をアクティベートし、`pip install -r requirements.txt`を実行します。

## 6. GitHub Actions ワークフロー (`.github/workflows/main.yml`)

CI/CDパイプラインを定義します。

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main # mainブランチへのプッシュでトリガー

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment: production # 環境名を指定 (GitHub Secretsと連携)

    permissions:
      contents: write # リポジトリへの書き込み権限 (GHCRプッシュに必要)
      packages: write # GHCRへの書き込み権限

    services: # テスト用PostgreSQLサービス
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: kina
          POSTGRES_PASSWORD: Kaim2308!
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval=10s --health-timeout=5s --health-retries=10

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install Python dependencies
      run: |
        pip cache purge
        pip install -r requirements.txt

    - name: Run Python tests
      env: # テスト用の環境変数を設定
        DATABASE_URL: "postgres://kina:Kaim2308!@127.0.0.1:5432/test_db"
        SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}
      run: |
        pytest --ds=mysite.settings.dev

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'

    - name: Install Node.js dependencies
      run: npm install

    - name: Run JavaScript tests
      run: |
        npm run format
        npm run lint
        npm run format -- --check # --check で変更せずにチェックのみ行う

    - name: Lint and Format Check (Python)
      run: |
        black . --check
        flake8 .

    - name: Lint and Format Check (JavaScript)
      run: |
        npm run format
        npm run lint
        npm run format -- --check # --check で変更せずにチェックのみ行う

    - name: Set lowercase repository name # リポジトリ名を小文字に変換
      id: repo_name_lower
      run: |
        LOWER_REPO_NAME=$(echo "${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
        echo "REPO_NAME_LOWER=$LOWER_REPO_NAME" >> $GITHUB_ENV

    - name: Log in to GitHub Container Registry # GHCRへのログイン
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }} # またはあなたのGitHubユーザー名
        password: ${{ secrets.GHCR_PAT }} # PATを使用

    - name: Build and push Docker image # Dockerイメージのビルドとプッシュ
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ghcr.io/${{ env.REPO_NAME_LOWER }}:latest

    - name: Deploy to Render # Renderへのデプロイ
      env:
        RENDER_SERVICE_ID: srv-d2b9l895pdvs73ci8550 # RenderのサービスID
      run: |
        curl -X POST -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" \
             -H "Content-Type: application/json" \
             "https://api.render.com/deploy/srv-${{ env.RENDER_SERVICE_ID }}?image=ghcr.io/${{ env.REPO_NAME_LOWER }}:latest"
```

**💡ハマりどころと工夫点:**
*   **`SECRET_KEY`が空エラー**: `pytest`は`.env`を自動で読み込まないため、`Run Python tests`ステップで`SECRET_KEY`を明示的に環境変数として設定する必要があります。`pytest-dotenv`を導入することで、ローカルでは`export`不要になりますが、CIでは`env:`ブロックで設定が必要です。
*   **`invalid tag: repository name must be lowercase`**: GitHubリポジトリ名に大文字が含まれると、Dockerイメージのタグ付けでエラーになります。`github.repository | lower`フィルターは`tags:`オプションでは使えないため、`Set lowercase repository name`ステップで環境変数`REPO_NAME_LOWER`を作成し、それを`tags:`で参照するようにしました。
*   **`unauthorized: unauthenticated: User cannot be authenticated with the token provided.`**: GHCRへのプッシュ権限エラーです。
    *   **`permissions: packages: write`** をワークフローの`jobs`レベルで設定することが必須です。
    *   デフォルトの`GITHUB_TOKEN`の権限が不足している場合があるため、**`docker/login-action`でPAT (`secrets.GHCR_PAT`) を使用する**ことで解決しました。PATのスコープ（`write:packages`, `read:packages`, `repo`）が重要です。
    *   `docker/build-push-action`の`with:`ブロックに`username`や`password`を直接渡すと警告/エラーになるため、`docker/login-action`でログインを完結させます。

## 7. Render Webサービスの設定

RenderのダッシュボードでWebサービスの設定を確認・更新します。

*   **Repository**: `https://github.com/jam006097/kids-playground` (新しいリポジトリ名)
*   **Branch**: `main`
*   **Build Command**: 空欄 (DockerイメージはGitHub Actionsでビルドするため)
*   **Start Command**: 空欄 (Dockerイメージの`CMD`を使用するため)
*   **Docker Command**: 空欄 (Dockerイメージの`CMD`を使用するため)
    *   **💡ハマりどころと工夫点**: Renderの「Docker Command」フィールドで複雑なコマンド（`bash -c "..."`）を直接入力すると、UIの解釈の問題でエラーが頻発しました。`start.sh`スクリプトを導入し、`Dockerfile`の`CMD`でそのスクリプトを実行するようにすることで、この問題を回避しました。
*   **Environment Variables**:
    *   `DATABASE_URL`: RenderのPostgreSQLデータベースの「Internal Connection String」を正確に設定。
    *   `SECRET_KEY`: GitHub Secretsと同じ値を設定。
    *   `PORT`: Renderが自動で設定するため、通常は不要。
    *   `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`など、`settings.py`で`os.getenv()`で読み込んでいる他の環境変数もすべて設定。

## 8. デプロイと動作確認

1.  **ローカルでの最終確認**:
    *   `git add .`
    *   `git commit -m "feat: CI/CD setup complete"`
    *   `git push origin main`
2.  **GitHub Actionsの確認**:
    *   ワークフローがすべてグリーンになることを確認。
3.  **Renderでの確認**:
    *   デプロイが成功し、アプリケーションが正常に動作することを確認。
    *   `Bad Request (400)`エラーが出た場合、`ALLOWED_HOSTS`にRenderのドメインが追加されているか確認。
    *   `Server Error (500)`や`relation "..." does not exist`エラーが出た場合、データベースのマイグレーションが正しく実行されていない可能性があります。`start.sh`が正しく機能しているか、Renderのログで確認します。
    *   静的ファイルが読み込まれない場合、`whitenoise`の設定が正しいか確認します。

## 9. データベースのマイグレーション（初回デプロイ時）

Renderの無料枠では`Pre-Deploy Command`が使えないため、`start.sh`にマイグレーションコマンドを含めることで対応しました。これにより、アプリケーションが起動するたびにマイグレーションが実行されます。
