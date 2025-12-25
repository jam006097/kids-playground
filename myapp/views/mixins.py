from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View


class LoginRequiredJsonMixin(AccessMixin, View):
    """
    ログインが必須なビューのためのMixin。
    未認証のユーザーがアクセスした場合、AJAXリクエストであればJSONレスポンスを返し、
    そうでなければ通常のログインページへのリダイレクトを行います。
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # AJAXリクエスト(X-Requested-Withヘッダーを持つ)の場合はJSONレスポンスを返す
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # `get_login_url()` は AccessMixin から提供される
                login_url = self.get_login_url()
                # ログイン後のリダイレクト先として現在のURLを指定
                next_url = request.get_full_path()
                redirect_url = f"{login_url}?next={next_url}"
                return JsonResponse({"redirect_url": redirect_url}, status=401)
            # それ以外の場合は通常のログインページへリダイレクト
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
