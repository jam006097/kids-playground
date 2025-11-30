import os
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect
import threading
from django.core.management import call_command
from django.conf import settings
from django.test import override_settings

# Make sure to run `playwright install` to install browsers before running tests


# Using StaticLiveServerTestCase to serve static files correctly during tests
@override_settings(
    DEBUG=True,  # Ensure debug is on for static files serving in LiveServerTestCase
    STATICFILES_DIRS=[
        os.path.join(settings.BASE_DIR, "myapp", "static"),
    ],
)
class FrontendModuleLoadingTest(StaticLiveServerTestCase):
    host = "127.0.0.1"  # Listen on localhost
    port = 8081  # Use a specific port for Playwright to connect

    # Removed setUpClass and tearDownClass for Playwright
    # Playwright will be set up and torn down per test method

    def setUp(self):
        super().setUp()
        # Start Playwright browser instance per test method
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page: Page = self.browser.new_page()

        self.console_errors = []
        self.network_errors = []

        self.page.on("console", lambda msg: self.console_errors.append(msg))
        self.page.on(
            "requestfailed", lambda request: self.network_errors.append(request)
        )
        self.page.on("response", self.check_response_for_errors)

    def tearDown(self):
        super().tearDown()
        self.page.close()
        self.browser.close()
        self.playwright.stop()

    def check_response_for_errors(self, response):
        """
        Check if any response is a 404 for a static/js/dist file.
        This is a more specific check than just any network_error.
        """
        if response.status == 404:
            url = response.url
            if "/static/js/dist/" in url and url.endswith(".js"):
                self.network_errors.append(f"404 Not Found for {url}")

    def test_frontend_modules_load_without_404s(self):
        """
        Test that frontend JavaScript modules are loaded without 404 errors.
        """
        # Navigate to the index page which uses the main scripts.
        self.page.goto(self.live_server_url + "/")

        # Wait for network to be idle, or for a specific element to appear.
        # For a module loading test, it's good to wait for network idle to ensure all scripts attempted to load.
        self.page.wait_for_load_state("networkidle")

        # Assert no console errors (other than expected ones)
        # Note: Depending on your project, you might have expected console warnings/errors.
        # You might need to filter self.console_errors here.
        # For now, we'll just check for network errors.
        self.assertEqual(
            len(self.network_errors),
            0,
            f"Found 404 network errors for JS modules: {self.network_errors}",
        )

        # You might also want to check for specific elements that indicate JS is running
        # For example: expect(self.page.locator('#map-container')).to_be_visible()
