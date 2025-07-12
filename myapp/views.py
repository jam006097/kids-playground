from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Playground, Favorite, Review
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


class PlaygroundListView(ListView):
    """
    公園一覧を表示するビュー。
    都市によるフィルタリング機能と、ユーザーのお気に入り公園情報を表示する。
    """
    model = Playground
    template_name = "index.html"
    context_object_name = "playgrounds"

    def get_queryset(self):
        """
        クエリセットを取得する。
        リクエストに'city'パラメータがあれば、その都市でフィルタリングする。
        """
        queryset = super().get_queryset()
        self.selected_city = self.request.GET.get("city")
        if self.selected_city:
            # 都市名で部分一致検索
            queryset = queryset.filter(address__icontains=self.selected_city)
        return queryset

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        公園の総数、フィルタリングされた公園の数、お気に入り公園の情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        playgrounds = context["playgrounds"]

        # 公園の総数とフィルタリングされた公園の数を取得
        total_count = Playground.objects.count()
        filtered_count = playgrounds.count()

        # 公園データをJSON形式に変換
        playgrounds_json = json.dumps(
            list(playgrounds.values("id", "name", "address", "phone"))
        )

        favorite_ids = []
        favorites = []
        favorites_json = "[]"
        # ユーザーが認証済みの場合、お気に入り公園の情報を取得
        if self.request.user.is_authenticated:
            # お気に入り公園のIDリストを取得
            favorite_ids = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "playground_id", flat=True
                )
            )
            favorite_ids = [str(id) for id in favorite_ids]
            # お気に入り公園オブジェクトを取得
            fav_objs = Favorite.objects.filter(user=self.request.user).select_related(
                "playground"
            )
            favorites = [fav.playground for fav in fav_objs]
            # お気に入り公園データをJSON形式に変換
            favorites_json = json.dumps(
                [
                    {"name": p.name, "address": p.address, "phone": p.phone}
                    for p in favorites
                ]
            )

        # コンテキストを更新
        context.update(
            {
                "selected_city": self.selected_city,
                "total_count": total_count,
                "filtered_count": filtered_count,
                "playgrounds_json": playgrounds_json,
                "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
                "favorite_ids": favorite_ids,
                "favorites": favorites,
                "favorites_json": favorites_json,
            }
        )
        return context


class SearchPlaceView(View):
    """
    Google Places APIを使用して場所を検索し、その場所のGoogleマップURLを返すビュー。
    """
    def get(self, request, *args, **kwargs):
        """
        GETリクエストを処理し、場所を検索してJSONレスポンスを返す。
        クエリパラメータ: name, address, phone
        """
        name = request.GET.get("name")
        address = request.GET.get("address")
        phone = request.GET.get("phone")

        logging.info(
            f"Searching for place: name={name}, address={address}, phone={phone}"
        )

        # Google Places APIのURLを構築
        search_url = (
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            f"?input={urllib.parse.quote(name)}"
            "&inputtype=textquery"
            "&fields=name,formatted_address,geometry"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        try:
            # APIリクエストを実行し、レスポンスを処理
            with urllib.request.urlopen(search_url) as response:
                data = json.loads(response.read().decode())
                logging.info(f"Google Places API response: {data}")
                candidates = data.get("candidates", [])
                # アドレスが一致する候補を探す
                for candidate in candidates:
                    if address in candidate.get("formatted_address", ""):
                        return JsonResponse(
                            {
                                "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                            }
                        )
                # 一致する候補がない場合、最初の候補を返す（もしあれば）
                if candidates:
                    candidate = candidates[0]
                    return JsonResponse(
                        {
                            "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                        }
                    )
                # 候補が見つからない場合
                return JsonResponse(
                    {"error": "No matching candidates found"}, status=404
                )
        except Exception as e:
            # エラーハンドリング
            logging.error(f"Error searching place: {e}")
            return JsonResponse({"error": str(e)}, status=500)


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


class AddFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """
    def post(self, request, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園をお気に入りに追加する。
        """
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを作成または取得
        Favorite.objects.get_or_create(user=request.user, playground=playground)
        return JsonResponse({"status": "ok"})


class RemoveFavoriteView(LoginRequiredMixin, View):
    """
    お気に入り削除ビュー。
    ログインしているユーザーのみがアクセス可能。
    """
    def post(self, request, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園をお気に入りから削除する。
        """
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        # お気に入りを削除
        Favorite.objects.filter(user=request.user, playground=playground).delete()
        return JsonResponse({"status": "ok"})


class MyPageView(LoginRequiredMixin, TemplateView):
    """
    マイページビュー。
    ログインしているユーザーのみがアクセス可能。
    ユーザーのお気に入り公園一覧を表示する。
    """
    template_name = "mypage.html"

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        ユーザーのお気に入り公園情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        # ユーザーのお気に入り公園を取得
        favorites = Favorite.objects.filter(user=self.request.user).select_related(
            "playground"
        )
        favorite_playgrounds = [favorite.playground for favorite in favorites]
        favorite_ids = [str(p.id) for p in favorite_playgrounds]
        # お気に入り公園データをJSON形式に変換
        playgrounds_json = json.dumps(
            [
                {"name": p.name, "address": p.address, "phone": p.phone}
                for p in favorite_playgrounds
            ]
        )
        # コンテキストを更新
        context.update(
            {
                "favorites": favorite_playgrounds,
                "favorite_ids": favorite_ids,
                "playgrounds_json": playgrounds_json,
                "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
            }
        )
        return context


class AddReviewView(LoginRequiredMixin, View):
    """
    レビュー追加ビュー。
    ログインしているユーザーのみがアクセス可能。
    """
    def post(self, request, playground_id, *args, **kwargs):
        """
        POSTリクエストを処理し、指定された公園にレビューを追加する。
        """
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        # 公園オブジェクトを取得
        playground = get_object_or_404(Playground, id=playground_id)

        # レビューを作成
        Review.objects.create(
            playground=playground, user=request.user, content=content, rating=rating
        )

        return JsonResponse(
            {"status": "success", "message": "口コミが投稿されました！"}
        )

    def get(self, request, *args, **kwargs):
        """
        GETリクエストは無効。
        """
        return JsonResponse(
            {"status": "error", "message": "無効なリクエストです。"}, status=400
        )


class ReviewListView(ListView):
    """
    レビュー一覧ビュー。
    指定された公園のレビュー一覧を表示する。
    """
    model = Review
    template_name = "view_reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        """
        クエリセットを取得する。
        URLから公園IDを取得し、その公園のレビューをフィルタリングして返す。
        """
        playground_id = self.kwargs["playground_id"]
        self.playground = get_object_or_404(Playground, id=playground_id)
        return Review.objects.filter(playground=self.playground).select_related("user")

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストデータを取得する。
        現在の公園情報を追加する。
        """
        context = super().get_context_data(**kwargs)
        context["playground"] = self.playground
        return context
