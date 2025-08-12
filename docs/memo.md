# Docker PostgreSQL 接続メモ

ローカル開発環境でDockerコンテナを起動し、その中で動作しているPostgreSQLデータベースに接続するまでの手順です。

## 1. Dockerコンテナの起動

もしコンテナが停止している場合は、以下のコマンドを実行してコンテナを起動します。

```bash
docker start kidsplayground-postgres
```
- `docker start`: 停止している既存のコンテナを起動するためのコマンドです。
- `kidsplayground-postgres`: 起動したいコンテナの名前です。

（補足: `docker ps` コマンドで実行中のコンテナを、`docker ps -a` コマンドで停止中のものも含めた全コンテナを確認できます）

## 2. PostgreSQLへの接続

コンテナが起動したら、以下のコマンドでコンテナ内のPostgreSQLに接続（ログイン）します。

```bash
sudo docker exec -it kidsplayground-postgres psql -U kina -d kidsplayground_db
```

### コマンドの解説
- `sudo`: お使いの環境でDockerコマンドの実行に管理者権限が必要な場合に使用します。
- `docker exec -it`: 実行中のDockerコンテナ内で、対話的にコマンドを実行するためのコマンドです。
- `kidsplayground-postgres`: 接続したいPostgreSQLコンテナの名前です。
- `psql`: PostgreSQLに接続するためのクライアントツールです。
- `-U kina`: `kina` というユーザー名で接続します。
- `-d kidsplayground_db`: `kidsplayground_db` という名前のデータベースに接続します。

---

接続に成功すると、プロンプトが `kidsplayground_db=#` のように変わり、SQLコマンドを実行できるようになります。
接続を終了する場合は `\q` と入力してください。