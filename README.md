# kidsplayground - 子供が遊べる施設のまとめサイト

## 概要
子供が遊べる施設や子育て支援施設を検索・表示し、お気に入り登録や口コミ投稿ができるWebアプリケーションです。

- サイトURL: https://kidsplayground.onrender.com/

## 主な機能

- **施設情報**: 子供が遊べる施設情報を一覧・地図で表示
- **検索**: 住所や施設名での検索
- **口コミ**: 施設ごとの口コミ投稿・表示
- **お気に入り**: 気になる施設をお気に入り登録
- **ランキング**: 口コミの評価/件数に基づいた施設ランキング
- **ユーザー認証**: 会員登録、ログイン・ログアウト

## 技術スタック
- 言語: Python, JavaScript, HTML, CSS
- フレームワーク: Django, Bootstrap
- データベース: PostgreSQL
- コンテナ化: Docker
- CI/CD: GitHub Actions
- コード品質: Pytest, Flake8, Black, Mypy, pre-commit
- ソース管理: Git, GitHub

---

## ローカル開発環境セットアップ
このプロジェクトでは、コード編集はローカルのPython仮想環境（`venv`）で行い、アプリケーションの実行やテストはDockerコンテナで行うハイブリッドな開発スタイルを採用しています。

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
    # Windowsの場合: venv\Scripts\activate
    ```

3.  **依存パッケージのインストール**
    ```bash
    pip install -r requirements.txt
    npm install
    pre-commit install
    ```

### ステップ2: 実行環境のセットアップ (Docker)

次に、アプリケーションを動かすためのDocker環境をセットアップします。

1.  **環境変数の設定**
    `.env.example` をコピーして `.env` を作成し、中身を環境に合わせて編集します。
    ```bash
    cp .env.example .env
    ```

2.  **Dockerコンテナの起動**
    ```bash
    docker compose up -d --build
    ```
    - `db`（PostgreSQL）と `web`（Django）の2つのサービスが起動します。
    - **注意**: データベースは初回起動時に `.env` の設定に基づき自動作成されます。

3. **データベースの作成**
    ```bash
    # データベースの作成
    docker compose exec -T db psql -U kina -d postgres -c "CREATE DATABASE kidsplayground_db;"
    # 権限の付与
    docker compose exec -T db psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE kidsplayground_db TO kina;"
    ```

4.  **データベースの初期化 (テーブル作成)**
    ```bash
    docker compose exec -T web python manage.py migrate
    ```

### ステップ3: データの準備 (バックアップの有無による分岐)

#### A. バックアップデータから復元する場合
既存のデータ（`sqldata_buckup/*.sql`）がある場合は、以下の手順で復元します。

```bash
# 1. 既存のスキーマをクリア
docker compose exec -T db psql -U kina -d kidsplayground_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 2. バックアップファイルを流し込み
docker compose exec -T db psql -U kina -d kidsplayground_db < sqldata_backup/最新のファイル.sql

# 3. ローカルドメインの設定 (127.0.0.1:8000に更新)
docker compose exec web python manage.py update_site_domain
```

#### B. 新規にデータを構築する場合 (バックアップがない場合)
管理画面にログインするための管理者ユーザーを作成します。

```bash
docker compose exec web python manage.py createsuperuser
```

---

## データの同期 (ローカル → 本番)

ローカルで作成したデータを本番環境（Render）に反映させるための専用コマンドを用意しています。

### 同期コマンドの実行
```bash
python3 manage.py sync_to_render
```

**このコマンドが行うこと:**
1. ローカルDBのバックアップ作成
2. 本番DBの初期化
3. バックアップデータのリストア
4. **本番ドメインの自動再設定**: `.env` の `PRODUCTION_DOMAIN` にドメインを書き戻します。

---

## 開発に役立つコマンド

- **全リビルド**: `python3 manage.py rebuild_all`
- **テスト実行**: `python3 manage.py run_all_tests`
- **リンター・フォーマットチェック**: `pre-commit run --all-files`
- **手動で個別にチェックする場合**:
```
black .        # フォーマット修正
flake8 .       # 構文チェック
mypy .         # 型チェック
bandit -r .    # セキュリティチェック
npm audit      # JSパッケージの脆弱性チェック
pip-audit      # Pythonパッケージの脆弱性チェック
```

## ライセンス
MITライセンス / 作者: jam006097
