本プロジェクトのデータベースをMySQLからPostgreSQLへ完全に移行します。これにより、開発、テスト、本番環境でのデータベースの一貫性を保ち、CI/CDパイプラインの安定性を向上させます。

**目的:**
*   開発環境、テスト環境、本番環境のデータベースをPostgreSQLに統一する。
*   GitHub Actionsでのテスト実行時のデータベース接続エラーを解消する。
*   RenderへのデプロイをPostgreSQLデータベースと連携させる。

**完了条件:**
*   ローカル開発環境でPostgreSQLが動作し、アプリケーションが接続できること。
*   `requirements.txt`がPostgreSQL関連の依存関係に更新されていること。
*   Djangoの設定ファイルがPostgreSQLを使用するように設定されていること。
*   `Dockerfile`がPostgreSQL関連の依存関係をインストールし、アプリケーションがPostgreSQLに接続できること。
*   GitHub ActionsのCIパイプラインがPostgreSQLサービスを使用して正常にテストを実行できること。
*   RenderにデプロイされたアプリケーションがPostgreSQLデータベースに正常に接続し、動作すること。

**タスクリスト:**

- [x] **ローカル開発環境の準備**
    - [x] PostgreSQLのインストールまたはDockerでの起動
    - [x] ローカルの`.env`ファイルにPostgreSQL接続情報を設定
- [x] **依存関係の更新**
    - [x] `requirements.txt`から`mysqlclient`を削除
    - [x] `requirements.txt`に`psycopg2-binary`を追加
    - [x] `pip install -r requirements.txt` を実行
- [x] **Django設定ファイルの更新**
    - [x] `mysite/settings/base.py`の`DATABASES`設定が`DATABASE_URL`環境変数を使用していることを確認（済）
    - [x] `mysite/settings/dev.py`からMySQLのハードコードされた設定を削除（済）
    - [x] `mysite/settings/prod.py` (もしあれば) のデータベース設定を`DATABASE_URL`環境変数を使用するように変更
- [x] **`Dockerfile`の更新**
    - [x] `Dockerfile`が`psycopg2-binary`をインストールするように変更
    - [x] `Dockerfile`からMySQL関連の依存関係のインストールを削除（もしあれば）
- [x] **GitHub Actionsワークフローの更新**
    - [x] `main.yml`の`services`ブロックを`mysql`から`postgres`に変更
    - [x] `Run Python tests`ステップの`DATABASE_URL`環境変数をPostgreSQLのテスト用接続情報に更新
- [x] **データベースのマイグレーション**
    - [x] `python manage.py makemigrations` を実行
    - [x] `python manage.py migrate` を実行
- [ ] **動作確認**
    - [ ] ローカル環境でアプリケーションが正常に動作することを確認
    - [ ] GitHub ActionsのCIパイプラインが成功することを確認
    - [ ] Renderにデプロイされたアプリケーションが正常に動作することを確認