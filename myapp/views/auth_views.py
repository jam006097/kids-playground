from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView


class UserLoginView(LoginView):
    """
    ユーザーログインビュー。
    ログインフォームと成功時のリダイレクトURLを設定する。
    """

    template_name = "registration/login.html"
    authentication_form = AuthenticationForm

    def get_success_url(self):
        """
        ログイン成功時のリダイレクトURLを返す。
        """
        return "/?tab=mypage"


class UserLogoutView(LogoutView):
    """
    ユーザーログアウトビュー。
    ログアウト後のリダイレクト先を設定する。
    """

    next_page = reverse_lazy("myapp:login")


class UserRegisterView(CreateView):
    """
    ユーザー登録ビュー。
    ユーザー作成フォームと成功時のリダイレクトURLを設定する。
    """

    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = "/"
