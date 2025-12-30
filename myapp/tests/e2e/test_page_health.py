import pytest
from playwright.sync_api import Page
from django.urls import reverse
from myapp.models import Playground  # Playgroundモデルをインポート

# テスト対象のURL名
URL_NAMES = [
    "myapp:index",
    "myapp:about",
    "myapp:ranking",
    "myapp:favorites",
    "account_login",
    "account_signup",
]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="function")
def existing_playground_id(db):
    """
    テスト用の既存のPlaygroundのIDを取得（または作成）するフィクスチャ。
    """
    playground = Playground.objects.first()
    if not playground:
        # テスト用にダミーのPlaygroundを作成
        playground = Playground.objects.create(
            name="Test Playground", description="A place to play"
        )
    return playground.id


@pytest.fixture
def page_data_for_health_check(live_server, page: Page, url_name: str):
    """
    指定されたURLにアクセスし、レスポンスと発生した各種エラーを収集するフィクスチャ。
    """
    console_errors: list[str] = []
    page_errors: list[str] = []
    resource_404_errors: list[str] = []

    # エラー監視リスナーを設定
    page.on(
        "console",
        lambda msg: (
            console_errors.append(f"[{msg.type}] {msg.text}")
            if msg.type == "error"
            else None
        ),
    )
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.on(
        "response",
        lambda res: resource_404_errors.append(res.url) if res.status == 404 else None,
    )

    # When: ページにアクセス
    path = reverse(url_name)
    full_url = live_server.url + path
    response = page.goto(full_url)
    page.wait_for_load_state("networkidle")

    # NOTE: favicon.icoの404は多くのブラウザでデフォルトでリクエストされるため、一旦除外する
    filtered_404_errors = [
        err for err in resource_404_errors if "favicon.ico" not in err
    ]

    return {
        "response": response,
        "console_errors": console_errors,
        "page_errors": page_errors,
        "resource_404_errors": filtered_404_errors,
        "full_url": full_url,
    }


@pytest.mark.e2e
@pytest.mark.parametrize("url_name", URL_NAMES)
def test_page_returns_ok_status(page_data_for_health_check: dict):
    """
    指定されたページが200 OKステータスを返すこと。
    """
    response = page_data_for_health_check["response"]
    full_url = page_data_for_health_check["full_url"]
    assert response is not None, f"ページ '{full_url}' のレスポンスがありません"
    assert (
        response.ok
    ), f"ページ '{full_url}' が 200 OK ではありません (status: {response.status})"


@pytest.mark.e2e
@pytest.mark.parametrize("url_name", URL_NAMES)
def test_page_has_no_console_errors(page_data_for_health_check: dict):
    """
    指定されたページにアクセスした際にコンソールエラーが発生しないこと。
    """
    console_errors = page_data_for_health_check["console_errors"]
    full_url = page_data_for_health_check["full_url"]
    assert (
        len(console_errors) == 0
    ), f"ページ '{full_url}' でコンソールエラーが発生しました:\n" + "\n".join(
        console_errors
    )


@pytest.mark.e2e
@pytest.mark.parametrize("url_name", URL_NAMES)
def test_page_has_no_js_exceptions(page_data_for_health_check: dict):
    """
    指定されたページにアクセスした際にページ内でJavaScript例外が発生しないこと。
    """
    page_errors = page_data_for_health_check["page_errors"]
    full_url = page_data_for_health_check["full_url"]
    assert (
        len(page_errors) == 0
    ), f"ページ '{full_url}' でページエラー（JS例外）が発生しました:\n" + "\n".join(
        page_errors
    )


@pytest.mark.e2e
@pytest.mark.parametrize("url_name", URL_NAMES)
def test_page_has_no_404_resource_errors(page_data_for_health_check: dict):
    """
    指定されたページにアクセスした際に参照されているリソースで404エラーが発生しないこと（favicon.icoを除く）。
    """
    resource_404_errors = page_data_for_health_check["resource_404_errors"]
    full_url = page_data_for_health_check["full_url"]
    assert (
        len(resource_404_errors) == 0
    ), f"ページ '{full_url}' でリソースの404エラーが発生しました:\n" + "\n".join(
        resource_404_errors
    )


@pytest.mark.e2e
def test_review_list_page_health(live_server, page: Page, existing_playground_id: int):
    """
    指定されたPlayground IDのレビュー一覧ページがエラーなく表示されること。
    """
    url_name = "myapp:view_reviews"
    path = reverse(url_name, args=[existing_playground_id])
    full_url = live_server.url + path

    # page_data_for_health_checkフィクスチャのロジックを複製してエラーを監視
    console_errors: list[str] = []
    page_errors: list[str] = []
    resource_404_errors: list[str] = []

    page.on(
        "console",
        lambda msg: (
            console_errors.append(f"[{msg.type}] {msg.text}")
            if msg.type == "error"
            else None
        ),
    )
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.on(
        "response",
        lambda res: resource_404_errors.append(res.url) if res.status == 404 else None,
    )

    # When: ページにアクセス
    response = page.goto(full_url)
    page.wait_for_load_state("networkidle")

    # NOTE: favicon.icoの404は多くのブラウザでデフォルトでリクエストされるため、一旦除外する
    filtered_404_errors = [
        err for err in resource_404_errors if "favicon.ico" not in err
    ]

    # Then: 各種エラーが発生しないことを確認
    assert (
        response is not None
    ), f"レビュー一覧ページ '{full_url}' のレスポンスがありません"
    assert (
        response.ok
    ), f"レビュー一覧ページ '{full_url}' が 200 OK ではありません (status: {response.status})"
    assert (
        len(console_errors) == 0
    ), (
        f"レビュー一覧ページ '{full_url}' でコンソールエラーが発生しました:\n"
        + "\n".join(console_errors)
    )
    assert (
        len(page_errors) == 0
    ), (
        f"レビュー一覧ページ '{full_url}' でページエラー（JS例外）が発生しました:\n"
        + "\n".join(page_errors)
    )
    assert (
        len(filtered_404_errors) == 0
    ), (
        f"レビュー一覧ページ '{full_url}' でリソースの404エラーが発生しました:\n"
        + "\n".join(filtered_404_errors)
    )
