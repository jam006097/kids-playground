import subprocess  # nosec B404
import sys
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs all tests: Python (pytest) and TypeScript (jest)."

    def _run_command(self, command, description):
        self.stdout.write(self.style.HTTP_INFO(f"Starting {description}..."))
        try:
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

        pytest_path = os.path.join(os.path.dirname(sys.executable), "pytest")
        base_env = os.environ.copy()

        # 1. Python/Django unit and integration tests (not E2E)
        self.stdout.write(self.style.HTTP_INFO("Starting Python tests (non-e2e)..."))
        non_e2e_command = [pytest_path]  # Relies on addopts in pytest.ini
        try:
            result = subprocess.run(  # nosec B603
                non_e2e_command,
                env=base_env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.stdout.write(result.stdout)
            self.stderr.write(result.stderr)
            self.stdout.write(self.style.SUCCESS("Python tests (non-e2e) passed!"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("Python tests (non-e2e) failed."))
            self.stderr.write(e.stdout)
            self.stderr.write(e.stderr)
            sys.exit(1)

        # 2. Python/Django/Playwright E2E tests
        self.stdout.write(self.style.HTTP_INFO("Starting Python E2E tests..."))
        e2e_command = [pytest_path, "-m", "e2e"]
        e2e_env = base_env.copy()
        e2e_env.update(
            {
                "DJANGO_ALLOW_ASYNC_UNSAFE": "true",
                "DJANGO_SETTINGS_MODULE": "mysite.settings.e2e",
            }
        )
        try:
            result = subprocess.run(  # nosec B603
                e2e_command,
                env=e2e_env,
                check=True,
                capture_output=True,
                text=True,
            )
            self.stdout.write(result.stdout)
            self.stderr.write(result.stderr)
            self.stdout.write(self.style.SUCCESS("Python E2E tests passed!"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR("Python E2E tests failed."))
            self.stderr.write(e.stdout)
            self.stderr.write(e.stderr)
            sys.exit(1)

        # 3. TypeScript/Jest tests
        if not self._run_command("npm run test", "TypeScript tests (jest)"):
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS("All tests passed successfully!"))
