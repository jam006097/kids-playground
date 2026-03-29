import os
import subprocess  # nosec B404
from django.core.management.base import BaseCommand
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "ローカルのDocker DBからRenderのDBへデータを移行します。"

    def handle(self, *args, **options):
        # .env ファイルを明示的に読み込む
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        load_dotenv(os.path.join(project_root, ".env"))

        # --- 設定 ---
        # バックアップファイル名に日付を追加
        from datetime import datetime

        datestamp = datetime.now().strftime("%Y%m%d")
        backup_dir = "sqldata_buckup"
        backup_filename = f"backup_{datestamp}.sql"
        backup_file = os.path.join(backup_dir, backup_filename)

        # バックアップディレクトリが存在しない場合は作成
        os.makedirs(backup_dir, exist_ok=True)

        local_db_container = "kidsplayground_postgres"
        local_db_user = "kina"
        local_db_name = "kidsplayground_db"
        render_db_url = os.getenv("RENDER_DATABASE_URL")

        if not render_db_url:
            self.stdout.write(
                self.style.ERROR(".envにRENDER_DATABASE_URLが設定されていません。")
            )
            return

        try:
            self.stdout.write(self.style.SUCCESS("--- データ移行プロセス開始 ---"))

            self.stdout.write(
                "\nステップ1: ローカルデータベースからバックアップを作成します..."
            )
            dump_command_args = [
                "docker",
                "exec",
                "-t",
                local_db_container,
                "pg_dump",
                "-U",
                local_db_user,
                "-d",
                local_db_name,
                "-F",
                "p",
                "--no-owner",
            ]
            with open(backup_file, "w") as f:
                subprocess.run(
                    dump_command_args, stdout=f, check=True
                )  # nosec B603 B607
            self.stdout.write(
                self.style.SUCCESS(
                    f" -> バックアップファイル '{backup_file}' を作成しました。"
                )
            )

            # Remove \restrict and \unrestrict lines from backup file
            with open(backup_file, "r") as f:
                lines = f.readlines()
            with open(backup_file, "w") as f:
                for line in lines:
                    if not line.startswith("\\restrict") and not line.startswith(
                        "\\unrestrict"
                    ):
                        f.write(line)

            self.stdout.write(
                "\nステップ2: Renderデータベースの既存テーブルを削除します..."
            )
            drop_command_args = [
                "docker",
                "exec",
                "-t",
                local_db_container,
                "psql",
                render_db_url,
                "-c",
                "DROP SCHEMA public CASCADE; CREATE SCHEMA public;",
            ]
            subprocess.run(
                drop_command_args, check=True, capture_output=True
            )  # nosec B603 B607
            self.stdout.write(self.style.SUCCESS(" -> テーブル削除完了"))

            self.stdout.write(
                "\nステップ3: Renderデータベースへデータをリストアします..."
            )
            # -i (interactive) を付けて標準入力を受け付け可能にする
            restore_command_args = [
                "docker",
                "exec",
                "-i",
                local_db_container,
                "psql",
                render_db_url,
                "--echo-all",
                "-v",
                "ON_ERROR_STOP=1",
            ]
            with open(backup_file, "r") as f:
                subprocess.run(
                    restore_command_args, stdin=f, check=True
                )  # nosec B603 B607
            self.stdout.write(self.style.SUCCESS(" -> リストア処理が完了しました。"))

            self.stdout.write(
                "\nステップ4: Renderデータベースのドメイン設定を本番用に更新します..."
            )
            production_domain = os.getenv(
                "PRODUCTION_DOMAIN", "kidsplayground.onrender.com"
            )
            site_name = "親子で遊ぼうナビ"
            # 既存の重複ドメインがあれば削除してから、id=1を更新する（一意制約エラー防止）
            # シングルクォートをエスケープしてSQLインジェクションを防止
            domain_escaped = production_domain.replace("'", "''")
            name_escaped = site_name.replace("'", "''")
            update_site_sql = (
                f"DELETE FROM django_site WHERE domain = '{domain_escaped}' AND id != 1; "  # nosec B608
                f"UPDATE django_site SET domain = '{domain_escaped}', "
                f"name = '{name_escaped}' WHERE id = 1;"
            )
            update_command_args = [
                "docker",
                "exec",
                "-t",
                local_db_container,
                "psql",
                render_db_url,
                "-c",
                update_site_sql,
            ]
            subprocess.run(
                update_command_args, check=True, capture_output=True
            )  # nosec B603 B607
            self.stdout.write(
                self.style.SUCCESS(
                    f" -> ドメインを '{production_domain}' に更新しました。"
                )
            )

        except subprocess.CalledProcessError as e:
            # エラー内容を標準エラー出力から取得して表示
            self.stdout.write(self.style.ERROR(f"\nエラーが発生しました: {e}"))
            self.stdout.write(
                self.style.ERROR(
                    f"エラー詳細(stdout):\n{e.stdout.decode() if e.stdout else 'N/A'}"
                )
            )
            self.stdout.write(
                self.style.ERROR(
                    f"エラー詳細(stderr):\n{e.stderr.decode() if e.stderr else 'N/A'}"
                )
            )
            # 失敗した場合はバックアップファイルを残す
            self.stdout.write(
                self.style.WARNING(
                    "エラーが発生したため、中間ファイル 'backup.sql' は削除されませんでした。内容を確認してください。"
                )
            )
            return

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "Dockerまたはpsqlコマンドが見つかりません。パスが通っているか確認してください。"
                )
            )
            return

        # 正常終了したことをユーザーに通知
        self.stdout.write(
            self.style.SUCCESS(
                f"\nステップ5: バックアップファイル '{backup_file}' を保存しました。"
            )
        )

        self.stdout.write(self.style.SUCCESS("\n🎉 データ移行がすべて完了しました！"))
