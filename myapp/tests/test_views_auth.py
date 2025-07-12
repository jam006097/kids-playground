from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_user_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_user_login(self):
        response = self.client.post(self.login_url, self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_user_logout_view(self):
        self.client.login(**self.user_data)
        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)
