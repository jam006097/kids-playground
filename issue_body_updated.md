本プロジェクトのデプロイプロセスを自動化するため、DockerとGitHub Actionsを用いたCI/CDパイプラインを導入します。デプロイ先としてRenderの無料枠を利用し、コンテナレジストリにはGitHub Container Registry (GHCR) を使用します。

**目的:**
*   コードの変更がプッシュされるたびに自動的にテスト、ビルド、デプロイを実行する。
*   開発環境と本番環境の差異を減らし、デプロイの信頼性を向上させる。
*   手動デプロイの手間を削減する。

**完了条件:**
*   `Dockerfile`がプロジェクトルートに作成され、Djangoアプリケーションのビルドと実行が可能であること。
*   `.dockerignore`が作成され、不要なファイルがDockerイメージに含まれないこと。
*   GitHub Actionsワークフロー (`.github/workflows/main.yml`) が作成され、以下のステップが自動実行されること:
    *   コードのチェックアウト
    *   PythonおよびJavaScriptの依存関係インストール
    *   PythonおよびJavaScriptのテスト実行
    *   Lintおよびフォーマットチェック
    *   DockerイメージのビルドとGHCRへのプッシュ
    *   Renderへのデプロイ（API経由でのトリガー）
*   Render上でWebサービスがDockerイメージから正常にデプロイされ、アプリケーションが動作すること。
*   GitHub SecretsにRenderのAPIキーおよび必要な環境変数が安全に設定されていること。

**タスクリスト:**

- [x] `Dockerfile`の作成
- [x] `.dockerignore`の作成
- [x] GitHub Actionsワークフロー (`.github/workflows/main.yml`) の作成
    - [x] Python環境セットアップと依存関係インストール
    - [x] Pythonテスト (`pytest`) 実行
    - [x] JavaScript環境セットアップと依存関係インストール
    - [x] JavaScriptテスト (`npm test`) 実行
    - [x] Lintおよびフォーマットチェック (`black`, `flake8`, `eslint`, `prettier`)
    - [x] DockerイメージのビルドとGHCRへのプッシュ
    - [x] Renderへのデプロイコマンドの追加
- [x] RenderアカウントのセットアップとWebサービスの作成
- [x] Render APIキーの取得とGitHub Secretsへの登録
- [x] RenderサービスIDの取得とGitHub Actionsワークフローへの設定
- [x] Render側での環境変数（`SECRET_KEY`, データベース接続情報など）の設定
- [ ] デプロイ後の動作確認