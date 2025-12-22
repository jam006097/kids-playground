FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Pythonの依存関係をインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Playwrightのブラウザをシステムワイドな場所にインストール
RUN PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright playwright install --with-deps
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/playwright
ENV DJANGO_ALLOW_ASYNC_UNSAFE=1


# アプリケーションコードをコピー
COPY . /app/

# Node.jsの依存関係をインストールし、TypeScriptをビルド
RUN npm install
RUN npm run build

# スタートスクリプトをコピーして実行権限を付与
COPY scripts/start.sh /app/
RUN chmod +x /app/start.sh

# 静的ファイルを収集（ビルドされたJSファイルも含まれる）
RUN python manage.py collectstatic --noinput

# コンテナ起動時のコマンド
CMD ["/app/start.sh"]
