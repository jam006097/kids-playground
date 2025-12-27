import subprocess  # nosec B404
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    カスタムDjango管理コマンド
    フロントエンドアセットのビルドからDockerコンテナの再起動までを一括で行う。
    実行順序:
    1. npm run build
    2. docker compose build
    3. docker compose down
    4. docker compose up -d
    """

    help = "Rebuilds and restarts the entire application environment."

    def run_command(self, command, a, b, c):
        """
        指定されたコマンドをサブプロセスとして実行し、進捗と結果をコンソールに出力する。
        """
        self.stdout.write(self.style.SUCCESS(f"--- {a}/{b}: {c} を開始します ---"))
        try:
            # コマンドを実行し、出力をリアルタイムで表示
            # check=Trueで、コマンドが失敗した場合にCalledProcessErrorを発生させる
            subprocess.run(command, check=True)  # nosec B603
            self.stdout.write(
                self.style.SUCCESS(f"--- {a}/{b}: {c} が正常に完了しました ---\n")
            )
        except FileNotFoundError:
            # 指定されたコマンドが見つからない場合のエラー
            self.stderr.write(
                self.style.ERROR(f"コマンド '{command[0]}' が見つかりません。")
            )
            raise CommandError("特定のコマンドの実行に失敗しました。処理を中断します。")
        except subprocess.CalledProcessError as e:
            # コマンド実行中にエラーが発生した場合
            self.stderr.write(
                self.style.ERROR(
                    f"'{' '.join(command)}' の実行中にエラーが発生しました。"
                )
            )
            self.stderr.write(self.style.ERROR(f"リターンコード: {e.returncode}"))
            raise CommandError(
                "コマンドの実行に失敗しました。詳細は上記のエラーを確認してください。"
            )

    def handle(self, *args, **options):
        """
        コマンドのメインロジック
        定義された一連のビルド＆デプロイコマンドを順次実行する。
        """
        # 実行するコマンドのリスト
        commands_to_run = [
            ("npm run build", ["npm", "run", "build"]),
            ("docker compose build", ["docker", "compose", "build"]),
            ("docker compose down", ["docker", "compose", "down"]),
            ("docker compose up -d", ["docker", "compose", "up", "-d"]),
        ]
        total_steps = len(commands_to_run)

        self.stdout.write(
            self.style.SUCCESS(
                "★★★ アプリケーション全体の再ビルドと再起動を開始します ★★★\n"
            )
        )

        # 各コマンドを順に実行
        for i, (description, command) in enumerate(commands_to_run, 1):
            try:
                self.run_command(command, i, total_steps, description)
            except CommandError:
                # run_commandでエラーが発生した場合、ここで処理を中断
                self.stderr.write(
                    self.style.ERROR(
                        "\n★★★ エラーが発生したため、処理を中断しました ★★★"
                    )
                )
                return  # コマンドの実行を終了

        self.stdout.write(
            self.style.SUCCESS(
                "★★★ すべての処理が正常に完了しました！アプリケーションが再起動されました ★★★"
            )
        )
