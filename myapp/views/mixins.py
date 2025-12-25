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
                return JsonResponse(
                    {"status": "error", "message": "Authentication required"},
                    status=401,
                )
            # それ以外の場合は通常のログインページへリダイレクト
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
