import pytest
from django.urls import reverse
from django.test import Client
from myapp.models import Playground


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def playground():
    return Playground.objects.create(
        name="テスト施設",
        address="テスト住所",
        phone="000-111-2222",
        latitude=35.0,
        longitude=135.0,
        description="テスト説明",
        opening_hours="9:00-17:00",
        website="http://test.com",
        nursing_room_available=True,
        diaper_changing_station_available=True,
        stroller_accessible=True,
        kids_space_available=True,
        notes_for_infants="特記事項テスト",
        # New fields
        google_map_url="http://maps.google.com/test",
        parking_available=True,
        indoor_play_area=True,
        kids_toilet_available=True,
        target_age="0-6歳",
        fee="無料",
        lunch_allowed=True,
    )


@pytest.mark.django_db
def test_存在しない施設IDの場合_404エラーを返すこと(client):
    # 存在しないIDで詳細ページにアクセス
    response = client.get(reverse("myapp:facility_detail", args=[999]))
    assert response.status_code == 404
