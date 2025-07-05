from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json  # 追加: jsonモジュールをインポート
from .models import Playground

class PlaygroundTests(TestCase):
    def setUp(self):
        # テストクライアントをセットアップし、テスト用のPlaygroundオブジェクトを作成
        self.client = Client()
        Playground.objects.create(name="Test Playground", address="Test Address", phone="123456789")

    @patch('myapp.views.fetch_data_from_api')
    def test_index_view(self, mock_fetch_data):
        # indexビューのテスト
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # ステータスコードが200であることを確認
        self.assertTemplateUsed(response, 'index.html')  # 使用されるテンプレートが正しいことを確認
        self.assertIn('playgrounds', response.context)  # コンテキストにplaygroundsが含まれていることを確認
        self.assertIn('total_count', response.context)  # コンテキストにtotal_countが含まれていることを確認
        self.assertIn('filtered_count', response.context)  # コンテキストにfiltered_countが含まれていることを確認
        self.assertIn('google_maps_api_key', response.context)  # コンテキストにgoogle_maps_api_keyが含まれていることを確認

    @patch('myapp.views.urllib.request.urlopen')
    def test_search_place_view(self, mock_urlopen):
        # search_placeビューのテスト（候補が見つかる場合）
        mock_response = {
            'candidates': [
                {'name': 'Test Place', 'formatted_address': 'Test Address'}
            ]
        }
        mock_urlopen.return_value.read.return_value = json.dumps(mock_response).encode()
        response = self.client.get(reverse('search_place'), {'name': 'Test Place', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 200)  # ステータスコードが200であることを確認
        self.assertIn('url', response.json())  # レスポンスにurlが含まれていることを確認

    @patch('myapp.views.urllib.request.urlopen')
    def test_search_place_view_no_candidates(self, mock_urlopen):
        # search_placeビューのテスト（候補が見つからない場合）
        mock_response = {'candidates': []}
        mock_urlopen.return_value.read.return_value = json.dumps(mock_response).encode()
        response = self.client.get(reverse('search_place'), {'name': 'Test Place', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 404)  # ステータスコードが404であることを確認
        self.assertIn('error', response.json())  # レスポンスにerrorが含まれていることを確認

    @patch('myapp.views.urllib.request.urlopen')
    def test_search_place_view_error(self, mock_urlopen):
        # search_placeビューのテスト（APIエラーが発生する場合）
        mock_urlopen.side_effect = Exception('API Error')
        response = self.client.get(reverse('search_place'), {'name': 'Test Place', 'address': 'Test Address'})
        self.assertEqual(response.status_code, 500)  # ステータスコードが500であることを確認
        self.assertIn('error', response.json())  # レスポンスにerrorが含まれていることを確認
