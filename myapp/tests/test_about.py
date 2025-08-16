from django.test import TestCase
from django.urls import reverse


class AboutPageTest(TestCase):
    def test_概要ページが正常に表示されること(self):
        """
        /about/ にアクセスした際に、ステータスコード200で正常にページが表示されること
        """
        response = self.client.get(reverse("myapp:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "myapp/about.html")
