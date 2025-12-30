import pytest
from django.urls import reverse
from django.test import Client
from myapp.models import Playground, Review
from users.models import CustomUser


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
    )


@pytest.mark.django_db
def test_facility_detail_displays_reviews(client, playground):
    """
    施設詳細ページに、その施設に関連するレビューが表示されることを確認する。
    """
    user = CustomUser.objects.create_user(
        email="testuser@example.com", password="password", account_name="テストユーザー"
    )
    review = Review.objects.create(
        playground=playground,
        user=user,
        content="素晴らしい公園でした！",
        rating=5,
    )

    response = client.get(reverse("myapp:facility_detail", args=[playground.id]))

    assert response.status_code == 200
    assert review.content in response.content.decode("utf-8")
    assert review.user.account_name in response.content.decode("utf-8")


@pytest.mark.django_db
def test_存在しない施設IDの場合_404エラーを返すこと(client):
    # 存在しないIDで詳細ページにアクセス
    response = client.get(reverse("myapp:facility_detail", args=[999]))
    assert response.status_code == 404
