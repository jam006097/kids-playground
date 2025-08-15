import pytest
from django.urls import reverse
from myapp.models import Playground, Review
from users.models import CustomUser
from django.test import Client
from typing import Any, Dict


@pytest.fixture
def setup_data(db) -> Dict[str, Any]:
    """テスト用のデータを作成するフィクスチャ"""
    user = CustomUser.objects.create_user(email="user@example.com", password="password")
    p1 = Playground.objects.create(
        name="公園A", address="住所A"
    )  # 評価平均3.0, 口コミ2件
    p2 = Playground.objects.create(
        name="公園B", address="住所B"
    )  # 評価平均5.0, 口コミ1件
    p3 = Playground.objects.create(
        name="公園C", address="住所C"
    )  # 評価平均4.0, 口コミ3件

    Review.objects.create(playground=p1, user=user, rating=2, content="")
    Review.objects.create(playground=p1, user=user, rating=4, content="")
    Review.objects.create(playground=p2, user=user, rating=5, content="")
    Review.objects.create(playground=p3, user=user, rating=4, content="")
    Review.objects.create(playground=p3, user=user, rating=4, content="")
    Review.objects.create(playground=p3, user=user, rating=4, content="")

    return {"p1": p1, "p2": p2, "p3": p3}


def test_ranking_view_default_sort_by_rating(
    client: Client, setup_data: Dict[str, Any]
) -> None:
    """ランキングページがデフォルト（評価順）で正しく表示されること"""
    url = reverse("myapp:ranking")
    response = client.get(url)

    assert response.status_code == 200
    assert "ranking/list.html" in [t.name for t in response.templates]

    # コンテキストの順序を検証
    expected_order = [setup_data["p2"], setup_data["p3"], setup_data["p1"]]
    assert list(response.context["playgrounds"]) == expected_order


def test_ranking_view_sort_by_review_count(
    client: Client, setup_data: Dict[str, Any]
) -> None:
    """ランキングページが口コミ数順で正しく表示されること"""
    url = reverse("myapp:ranking") + "?sort=review_count"
    response = client.get(url)

    assert response.status_code == 200

    # コンテキストの順序を検証
    expected_order = [setup_data["p3"], setup_data["p1"], setup_data["p2"]]
    assert list(response.context["playgrounds"]) == expected_order
