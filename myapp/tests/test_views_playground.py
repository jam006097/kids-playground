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

    def test_playground_list_view_with_lunch_allowed_filter(self):
        """飲食可フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Lunch Allowed Park", address="Filter City", lunch_allowed=True
        )
        Playground.objects.create(
            name="No Lunch Allowed Park",
            address="Filter City",
            lunch_allowed=False,
        )
        response = self.client.get(self.url, {"lunch_allowed": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Lunch Allowed Park")

    def test_playground_list_view_with_indoor_play_area_filter(self):
        """屋内遊び場フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Indoor Play Park", address="Filter City", indoor_play_area=True
        )
        Playground.objects.create(
            name="No Indoor Play Park",
            address="Filter City",
            indoor_play_area=False,
        )
        response = self.client.get(self.url, {"indoor_play_area": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Indoor Play Park")

    def test_playground_list_view_with_kids_toilet_filter(self):
        """子供用トイレフィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Kids Toilet Park", address="Filter City", kids_toilet_available=True
        )
        Playground.objects.create(
            name="No Kids Toilet Park",
            address="Filter City",
            kids_toilet_available=False,
        )
        response = self.client.get(self.url, {"kids_toilet": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Kids Toilet Park")

    def test_playground_list_view_with_target_age_min_filter(self):
        """対象年齢（最小）フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Age 5 Park", address="Filter City", target_age_start=5
        )
        Playground.objects.create(
            name="Age 10 Park", address="Filter City", target_age_start=10
        )
        response = self.client.get(self.url, {"target_age_min": 7})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Age 10 Park")

    def test_playground_list_view_with_target_age_max_filter(self):
        """対象年齢（最大）フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Age 10 Max Park", address="Filter City", target_age_end=10
        )
        Playground.objects.create(
            name="Age 5 Max Park", address="Filter City", target_age_end=5
        )
        response = self.client.get(self.url, {"target_age_max": 7})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Age 5 Max Park")

    def test_playground_list_view_with_fee_min_filter(self):
        """料金（最小）フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Fee 500 Park", address="Filter City", fee_decimal=500
        )
        Playground.objects.create(
            name="Fee 1000 Park", address="Filter City", fee_decimal=1000
        )
        response = self.client.get(self.url, {"fee_min": 700})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Fee 1000 Park")

    def test_playground_list_view_with_fee_max_filter(self):
        """料金（最大）フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Fee 1000 Max Park", address="Filter City", fee_decimal=1000
        )
        Playground.objects.create(
            name="Fee 500 Max Park", address="Filter City", fee_decimal=500
        )
        response = self.client.get(self.url, {"fee_max": 700})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Fee 500 Max Park")

    def test_playground_list_view_with_parking_info_filter(self):
        """駐車場情報フィルターで公園リストビューが正常に表示されることをテスト"""
        Playground.objects.create(
            name="Free Parking Park", address="Filter City", parking_info="FREE"
        )
        Playground.objects.create(
            name="Paid Parking Park", address="Filter City", parking_info="PAID"
        )
        Playground.objects.create(
            name="No Parking Park", address="Filter City", parking_info="NO"
        )
        response = self.client.get(self.url, {"parking_info": "FREE"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "playgrounds/list.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Free Parking Park")

    def test_search_form_opened_context_with_get_params(self):
        """GETパラメータがある場合にsearch_form_openedがTrueになることをテスト"""
        response = self.client.get(self.url, {"q": "Test"})
        self.assertTrue(response.context["search_form_opened"])

    def test_search_form_opened_context_without_get_params(self):
        """GETパラメータがない場合にsearch_form_openedがFalseになることをテスト"""
        response = self.client.get(self.url)
        self.assertFalse(response.context.get("search_form_opened", False))

    # --- TDD for SSI Vulnerability ---

    def test_ssi_injection_attempt_on_fee_min(self):
        """fee_minパラメータへのSSI攻撃をしてもサーバーエラーが発生しないことをテスト"""
        with self.settings(DEBUG=True):
            response = self.client.get(self.url, {"fee_min": '<!--#EXEC cmd="ls /"-->'})
            self.assertEqual(response.status_code, 200)

    def test_ssi_injection_attempt_on_fee_max(self):
        """fee_maxパラメータへのSSI攻撃をしてもサーバーエラーが発生しないことをテスト"""
        with self.settings(DEBUG=True):
            response = self.client.get(self.url, {"fee_max": '<!--#EXEC cmd="ls /"-->'})
            self.assertEqual(response.status_code, 200)

    def test_ssi_injection_attempt_on_target_age_min(self):
        """target_age_minパラメータへのSSI攻撃をしてもサーバーエラーが発生しないことをテスト"""
        with self.settings(DEBUG=True):
            response = self.client.get(
                self.url, {"target_age_min": '<!--#EXEC cmd="ls /"-->'}
            )
            self.assertEqual(response.status_code, 200)

    def test_ssi_injection_attempt_on_target_age_max(self):
        """target_age_maxパラメータへのSSI攻撃をしてもサーバーエラーが発生しないことをテスト"""
        with self.settings(DEBUG=True):
            response = self.client.get(
                self.url, {"target_age_max": '<!--#EXEC cmd="ls /"-->'}
            )
            self.assertEqual(response.status_code, 200)
