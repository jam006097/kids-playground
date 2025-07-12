from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from myapp.models import Playground, Favorite, Review
import urllib.request
import urllib.parse
import json
import logging
import os
from dotenv import load_dotenv
from django.views.generic import ListView, View, CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

# .envファイルから環境変数を読み込む
load_dotenv()

# APIのURLとGoogle Maps APIキーを環境変数から取得
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # ログをファイルに保存
        logging.StreamHandler(),  # コンソールにもログを表示
    ],
)


class UserLoginView(LoginView):
    """
    ユーザーログインビュー。
    ログインフォームと成功時のリダイレクトURLを設定する。
    """
    template_name = "login.html"
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
    next_page = "index"


class UserRegisterView(CreateView):
    """
    ユーザー登録ビュー。
    ユーザー作成フォームと成功時のリダイレクトURLを設定する。
    """
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = "/"
