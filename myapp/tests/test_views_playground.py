from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import Playground


class PlaygroundListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("index")
        Playground.objects.create(
            name="Test Park 1", address="CityA", phone="123-456-7890"
        )
        Playground.objects.create(
            name="Test Park 2", address="CityB", phone="098-765-4321"
        )

    def test_playground_list_view_no_filter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(len(response.context["playgrounds"]), 2)

    def test_playground_list_view_with_city_filter(self):
        response = self.client.get(self.url, {"city": "CityA"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertEqual(len(response.context["playgrounds"]), 1)
        self.assertEqual(response.context["playgrounds"][0].name, "Test Park 1")
