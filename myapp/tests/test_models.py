import pytest
from myapp.models import Playground, Review
from users.models import CustomUser


@pytest.mark.django_db
def test_get_by_rating_rank_returns_playgrounds_ordered_by_average_rating() -> None:
    """評価の平均点が高い順に施設が返されること"""
    # ユーザー作成
    user1 = CustomUser.objects.create_user(
        email="user1@example.com", password="password"
    )
    user2 = CustomUser.objects.create_user(
        email="user2@example.com", password="password"
    )

    # 施設作成
    p1 = Playground.objects.create(name="公園A", address="住所A")  # 平均3.0
    p2 = Playground.objects.create(name="公園B", address="住所B")  # 平均5.0
    p3 = Playground.objects.create(name="公園C", address="住所C")  # 平均4.0
    p4 = Playground.objects.create(name="公園D", address="住所D")  # 口コミなし

    # 口コミ作成
    Review.objects.create(playground=p1, user=user1, rating=2, content="うーん")
    Review.objects.create(playground=p1, user=user2, rating=4, content="まあまあ")

    Review.objects.create(playground=p2, user=user1, rating=5, content="最高！")
    Review.objects.create(playground=p2, user=user2, rating=5, content="素晴らしい")

    Review.objects.create(playground=p3, user=user1, rating=4, content="良い")

    # ランキング取得
    ranked_playgrounds = Playground.objects.get_by_rating_rank()

    # 検証
    expected_order = [p2, p3, p1]
    assert (
        list(ranked_playgrounds) == expected_order
    ), f"ランキングの順序が正しくありません。期待値: {[p.name for p in expected_order]}, 実際: {[p.name for p in ranked_playgrounds]}"

    # 口コミのない公園Dは含まれないことを検証
    assert (
        p4 not in ranked_playgrounds
    ), "口コミのない施設がランキングに含まれています。"


@pytest.mark.django_db
def test_get_by_review_count_rank_returns_playgrounds_ordered_by_review_count() -> None:
    """口コミの件数が多い順に施設が返されること"""
    # ユーザー作成
    user1 = CustomUser.objects.create_user(
        email="user1@example.com", password="password"
    )

    # 施設作成
    p1 = Playground.objects.create(name="公園A", address="住所A")  # 口コミ2件
    p2 = Playground.objects.create(name="公園B", address="住所B")  # 口コミ3件
    p3 = Playground.objects.create(name="公園C", address="住所C")  # 口コミ1件
    p4 = Playground.objects.create(name="公園D", address="住所D")  # 口コミなし

    # 口コミ作成
    Review.objects.create(playground=p1, user=user1, rating=4, content="良い")
    Review.objects.create(playground=p1, user=user1, rating=5, content="最高")

    Review.objects.create(playground=p2, user=user1, rating=5, content="最高！")
    Review.objects.create(playground=p2, user=user1, rating=5, content="素晴らしい")
    Review.objects.create(playground=p2, user=user1, rating=4, content="また来たい")

    Review.objects.create(playground=p3, user=user1, rating=3, content="普通")

    # ランキング取得
    ranked_playgrounds = Playground.objects.get_by_review_count_rank()

    # 検証
    expected_order = [p2, p1, p3]
    assert (
        list(ranked_playgrounds) == expected_order
    ), f"ランキングの順序が正しくありません。期待値: {[p.name for p in expected_order]}, 実際: {[p.name for p in ranked_playgrounds]}"
    assert (
        p4 not in ranked_playgrounds
    ), "口コミのない施設がランキングに含まれています。"
