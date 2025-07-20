
from django.test import TestCase
from django.urls import reverse
from bs4 import BeautifulSoup

class TemplateRenderTest(TestCase):
    def test_login_page_renders_correctly(self):
        """
        GETリクエストに対してlogin.htmlが正しくレンダリングされるかテスト
        """
        response = self.client.get(reverse('login'))

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

        # 使用されているテンプレートの確認
        self.assertTemplateUsed(response, 'login.html')

        # HTMLの内容の確認
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNotNone(soup.find('h1', text='ログイン'))
        self.assertIsNotNone(soup.find('form'))
        self.assertIsNotNone(soup.find('button', type='submit', class_='btn-primary'))
        self.assertTrue('新規登録は' in response.content.decode())
