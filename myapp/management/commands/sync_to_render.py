import os
import subprocess
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

        # 設定
        local_db_container = "kidsplayground_postgres"
        local_db_user = "kina"
        local_db_name = "kidsplayground_db"
        backup_file = "sqldata_buckup/backup.sql"
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
            dump_command = (
                f"docker exec -t {local_db_container} pg_dump -U {local_db_user} "
                f"-d {local_db_name} -F p --no-owner"
            )
            with open(backup_file, "w") as f:
                subprocess.run(dump_command.split(), stdout=f, check=True)
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
            drop_command = f'psql "{render_db_url}" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"'
            subprocess.run(drop_command, shell=True, check=True, capture_output=True)
            self.stdout.write(self.style.SUCCESS(" -> テーブル削除完了"))

            self.stdout.write(
                "\nステップ3: Renderデータベースへデータをリストアします..."
            )
            # psqlはシェルのリダイレクト<を使うため、shell=Trueで実行
            restore_command = (
                f'psql "{render_db_url}" --echo-all -v ON_ERROR_STOP=1 < {backup_file}'
            )
            # shell=Trueの場合、コマンド全体を文字列として渡す
            subprocess.run(restore_command, shell=True, check=True)
            self.stdout.write(self.style.SUCCESS(" -> リストア処理が完了しました。"))

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

        # 正常終了した場合のみバックアップファイルを削除
        if os.path.exists(backup_file):
            self.stdout.write("\nステップ4: 一時バックアップファイルを削除します...")
            os.remove(backup_file)
            self.stdout.write(
                self.style.SUCCESS(" -> バックアップファイルを削除しました。")
            )

        self.stdout.write(self.style.SUCCESS("\n🎉 データ移行がすべて完了しました！"))
