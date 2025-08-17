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

    # 都市フィルタ付きで公園リストビューが正常に表示されることをテスト
    def test_playground_list_view_with_city_filter(self):
        response = self.client.get(self.url, {"city": "CityA"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Test Park 1")

    def test_playground_list_view_with_keyword_search(self):
        """キーワード検索で公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Unique Park Name",
            address="Search City",
            description="This is a unique description.",
        )
        response = self.client.get(self.url, {"q": "Unique"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Unique Park Name")

    def test_playground_list_view_with_nursing_room_filter(self):
        """授乳室フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Nursing Room Park", address="Filter City", nursing_room_available=True
        )
        Playground.objects.create(
            name="No Nursing Room Park",
            address="Filter City",
            nursing_room_available=False,
        )
        response = self.client.get(self.url, {"nursing_room": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Nursing Room Park")

    def test_playground_list_view_with_diaper_changing_station_filter(self):
        """おむつ交換台フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Diaper Park",
            address="Filter City",
            diaper_changing_station_available=True,
        )
        Playground.objects.create(
            name="No Diaper Park",
            address="Filter City",
            diaper_changing_station_available=False,
        )
        response = self.client.get(self.url, {"diaper_changing_station": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Diaper Park")

    def test_playground_list_view_with_stroller_accessible_filter(self):
        """ベビーカー可フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Stroller Park", address="Filter City", stroller_accessible=True
        )
        Playground.objects.create(
            name="No Stroller Park",
            address="Filter City",
            stroller_accessible=False,
        )
        response = self.client.get(self.url, {"stroller_accessible": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Stroller Park")
