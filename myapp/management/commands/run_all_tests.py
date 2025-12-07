import subprocess  # nosec B404
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs all tests: Python (pytest) and TypeScript (jest)."

    def _run_command(self, command, description):
        self.stdout.write(self.style.HTTP_INFO(f"Starting {description}..."))
        try:
            # shell=True を使用すると、npm のようなコマンドを仮想環境やパスを気にせず実行しやすくなります。
            # ただし、コマンドインジェクションのリスクがあるため、信頼できるコマンドのみを実行してください。
            result = subprocess.run(
                command,
                shell=True,  # nosec B602
                check=True,
                capture_output=True,
                text=True,
            )
            self.stdout.write(result.stdout)
            self.stderr.write(result.stderr)
            self.stdout.write(self.style.SUCCESS(f"{description} passed!"))
            return True
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"{description} failed."))
            self.stderr.write(e.stdout)
            self.stderr.write(e.stderr)
            return False

    def handle(self, *args, **options):
        self.stdout.write(self.style.SQL_COLTYPE("Running all tests..."))

        # 1. Python/Django/Playwright tests
        self.stdout.write(self.style.HTTP_INFO("Starting Python tests (pytest)..."))
        pytest_command = [
            "venv/bin/pytest",
            "-o",
            "addopts=",
        ]
        try:
            result = subprocess.run(
                pytest_command,  # nosec B603
                check=True,
                capture_output=True,
                text=True,
            )
            self.stdout.write(result.stdout)
            self.stderr.write(result.stderr)
            self.stdout.write(self.style.SUCCESS("Python tests (pytest) passed!"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("Python tests (pytest) failed."))
            self.stderr.write(e.stdout)
            self.stderr.write(e.stderr)
            sys.exit(1)

        # 2. TypeScript/Jest tests
        if not self._run_command("npm run test", "TypeScript tests (jest)"):
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("All tests passed successfully!"))
