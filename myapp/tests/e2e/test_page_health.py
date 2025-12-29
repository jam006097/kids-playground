import pytest
from playwright.sync_api import Page
from django.urls import reverse

# テスト対象のURL名
URL_NAMES = [
    "myapp:index",
    "myapp:about",
    "myapp:ranking",
    "account_login",
    "account_signup",
]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }


@pytest.mark.e2e
@pytest.mark.parametrize("url_name", URL_NAMES)
def test_page_is_healthy(live_server, page: Page, url_name: str):
    """
    指定されたページにアクセスした際、エラーが発生せず正常に表示されること。
    - ページが200 OKを返す
    - コンソールにエラーが出力されない
    - ページ内でハンドルされない例外が発生しない
    - 参照されているリソースで404が発生しない
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

    # Then: 各種エラーが発生していないことを表明
    assert response is not None, f"ページ '{full_url}' のレスポンスがありません"
    assert (
        response.ok
    ), f"ページ '{full_url}' が 200 OK ではありません (status: {response.status})"
    assert (
        len(console_errors) == 0
    ), f"ページ '{full_url}' でコンソールエラーが発生しました:\n" + "\n".join(
        console_errors
    )
    assert (
        len(page_errors) == 0
    ), f"ページ '{full_url}' でページエラー（JS例外）が発生しました:\n" + "\n".join(
        page_errors
    )
    # NOTE: favicon.icoの404は多くのブラウザでデフォルトでリクエストされるため、一旦除外する
    resource_404_errors = [
        err for err in resource_404_errors if "favicon.ico" not in err
    ]
    assert (
        len(resource_404_errors) == 0
    ), f"ページ '{full_url}' でリソースの404エラーが発生しました:\n" + "\n".join(
        resource_404_errors
    )
