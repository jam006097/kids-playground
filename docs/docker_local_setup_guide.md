# Docker ローカル開発環境構築ガイド：競合解消とDocker Composeによる効率化

## はじめに

こんにちは！ 今回は、ローカル環境でDockerを使った開発でよく遭遇する問題、特に「Docker Desktopと既存のローカルDocker環境の競合」について解説し、その解決策として「Docker Compose」を使った効率的な開発環境の構築方法を紹介します。

この記事は、皆さんがよりスムーズに開発を進められるようになることを目的としています。

---

## 背景

私は、Djangoアプリケーション `kidsPlayGround` の開発を進めていました。このプロジェクトではデータベースとしてPostgreSQLを使用し、当初はローカルのDockerコンテナとしてPostgreSQLを単独で起動・管理していました。

しかし、開発を進める中で、Docker環境を統合的に管理できる「Docker Desktop」を導入することになり、問題が発生しました。Docker Desktopを起動すると、既存のローカルDocker環境と競合し、データベースコンテナが正しく動作しない、あるいは起動できない状況になったのです。

---

## 問題の核心

この問題の核心は、**複数のDockerデーモンが同じリソース（特にポート）を奪い合おうとする**ことにあります。

- **既存のローカルDocker環境:** Linux環境では、DockerをインストールするとシステムサービスとしてDockerデーモンがバックグラウンドで動作します。このデーモンがコンテナを管理します。
- **Docker Desktop:** Docker Desktopは独自のDockerデーモンを持ち、GUIやKubernetesとの連携機能を提供します。Linux版では既存のDockerデーモンと競合する可能性があります。

つまり、2つの異なるDockerデーモンが同じポート（例えばPostgreSQLの `5432`）を使おうとしたり、コンテナ管理権を巡って衝突するわけです。

---

## 解決策：Docker Composeによる統合管理

この問題を解決し、開発環境を効率化する最善策が「Docker Compose」です。

### Docker Composeとは？

Docker Composeは、複数のコンテナで構成されるアプリケーションを定義し、実行するためのツールです。`docker-compose.yml` というYAMLファイルに、アプリケーションを構成するすべてのサービス（データベース、Webアプリ、キャッシュなど）を記述します。

これにより、単一のコマンド (`docker-compose up`) で関連するすべてのコンテナをまとめて起動・停止・管理できます。

### Docker Composeが競合を解決する仕組み

Docker Compose自体はDockerデーモンではなく、**現在アクティブなDockerデーモン**に指示を出すクライアントツールです。

1.  **Docker Desktopのデーモンをアクティブにする:** Docker Desktopを起動すると、その内部デーモンがアクティブになります。既存のスタンドアロンのDockerデーモンとの競合を避けるため、通常はスタンドアロンデーモンを停止するか、Docker Desktopが管理します。
2.  **`docker-compose.yml` で一元管理:** `docker-compose.yml` ファイルにすべてのサービスを定義すると、Docker ComposeはDocker Desktopのデーモンに指示を出してコンテナを起動します。これにより、すべてのコンテナがDocker Desktopの管理下に入り、競合が解消されます。

---

## 具体的手順

### 1. 既存データのバックアップ

古いPostgreSQLコンテナのデータを失わないようにバックアップします。

```bash
# 古いPostgreSQLコンテナを起動します（もし停止している場合）
sudo docker start [古いPostgreSQLコンテナ名]

# データベースのデータをSQLファイルとしてエクスポートします
sudo docker exec [古いPostgreSQLコンテナ名] pg_dump -U [データベースユーザー名] [データベース名] > db_backup.sql
```
**補足:**
*   `[古いPostgreSQLコンテナ名]` は、以前使用していたPostgreSQLコンテナの名前です。`docker ps -a` で確認できます。
*   `[データベースユーザー名]` は、PostgreSQLデータベースに接続するためのユーザー名です。
*   `[データベース名]` は、バックアップしたいデータベースの名前です。

### 2. 古いコンテナの停止と削除

新しい環境をクリーンに起動するために、古いコンテナを停止し、削除します。

```bash
sudo docker stop [古いPostgreSQLコンテナ名]
sudo docker rm [古いPostgreSQLコンテナ名]
```

### 3. `docker-compose.yml` の作成

プロジェクトのルートディレクトリに `docker-compose.yml` ファイルを作成し、PostgreSQLとDjangoアプリケーションのサービスを定義します。

```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    container_name: kidsplayground_postgres # 例: PostgreSQLコンテナの名前
    environment:
      POSTGRES_DB: kidsplayground_db # 例: データベース名
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: kidsplayground_web # 例: Djangoアプリケーションコンテナの名前
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgres://${DB_USER}:${DB_PASSWORD}@db:5432/${POSTGRES_DB}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
```

### 4. 環境変数の設定 (`.env`)

`docker-compose.yml` で使用する環境変数を、プロジェクトのルートディレクトリにある `.env` ファイルに記述します。

```
# .env (プロジェクトルートに配置)
DB_USER=your_db_username # 例: データベースユーザー名 
DB_PASSWORD=your_db_password # 例: データベースパスワード
POSTGRES_DB=your_db_name # 例: データベース名 
SECRET_KEY=your_django_secret_key_here # DjangoのSECRET_KEYもここに設定
```

※ `.env` は `.gitignore` に追加してGit管理から除外します。

### 5. Docker Composeのインストール

もし `docker-compose` コマンドが利用できない場合は、インストールします。

```bash
sudo apt install docker-compose
```

### 6. Docker Desktopの起動

Docker ComposeがDockerデーモンと通信できるように、Docker Desktopを起動します。

### 7. サービスの起動

```bash
docker-compose up -d
```

### 8. データの復元

バックアップしたデータを新しいPostgreSQLコンテナに復元します。

```bash
docker exec -i kidsplayground_postgres psql -U [データベースユーザー名] [データベース名] < db_backup.sql
```
**補足:**
*   `kidsplayground_postgres` は、`docker-compose.yml` で定義した新しいPostgreSQLコンテナの名前です。
*   `[データベースユーザー名]` は、新しいPostgreSQLデータベースに接続するためのユーザー名です（例: `kina`）。
*   `[データベース名]` は、復元先のデータベースの名前です（例: `kidsplayground_db`）。
*   `kidsplayground_db_backup.sql` は、ステップ1で作成したバックアップファイルです。

### 9. 動作確認

ブラウザで `http://localhost:8000` にアクセスし、Djangoアプリとデータが正しく動作するか確認します。

---

## 得られた知見

-   **Docker Desktop:** GUIとDocker Engineを統合したツールで、ローカルDocker管理が簡単になる。
-   **Docker Compose:** 複数コンテナを一元管理でき、開発環境の再現性が向上する。
-   **ボリュームマウント:** ホストのディレクトリをコンテナにマウントすることで、コード変更が即座に反映される。
-   **環境変数の活用:** 機密情報は `.env` から読み込み、Gitに誤ってアップロードされないようにする。
-   **依存関係管理:** `depends_on` と `healthcheck` でサービスの起動順序を制御できる。

---

## まとめ

Docker DesktopとDocker Composeを組み合わせることで、ローカル開発環境のセットアップと管理が非常にスムーズになります。特に、環境の競合を解消し、機密情報を安全に扱うベストプラクティスを実践できることが大きな利点です。

ぜひこのガイドを参考に、快適なDocker開発ライフを実現してください！