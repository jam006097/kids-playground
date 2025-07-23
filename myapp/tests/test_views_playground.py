from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import Playground


class PlaygroundListViewTest(TestCase):
    # テストのセットアップ
    def setUp(self):
        self.client = Client()
        self.url = reverse("myapp:index")
        Playground.objects.create(
            name="Test Park 1", address="CityA", phone="123-456-7890"
        )
        Playground.objects.create(
            name="Test Park 2", address="CityB", phone="098-765-4321"
        )

    # フィルタなしで公園リストビューが正常に表示されることをテスト
    def test_playground_list_view_no_filter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 2)
        self.assertNotContains(response, 'id="mypage-tab"')

    # 都市フィルタ付きで公園リストビューが正常に表示されることをテスト
    def test_playground_list_view_with_city_filter(self):
        response = self.client.get(self.url, {"city": "CityA"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Test Park 1")
