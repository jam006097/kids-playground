from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Playground, Favorite, Review
from django.views.decorators.http import require_POST
import urllib.request
import urllib.parse  # URLエンコード用のモジュールを追加
import json
import logging
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# データAPIのURLとGoogle Maps APIキーを環境変数から取得
API_URL = "https://data.bodik.jp/api/3/action/datastore_search?resource_id=2ed1eb60-1a5d-46fc-9e55-cd1c35f2be93"
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


def fetch_data_from_api():
    """
    データAPIからデータを取得し、データベースに保存する関数。
    """
    logging.info("Starting data fetch process from API")

    try:
        # APIからデータを取得
        with urllib.request.urlopen(API_URL) as response:
            data = json.loads(response.read().decode())
            records = data["result"]["records"]
            # 取得したデータをデータベースに保存
            for row in records:
                Playground.objects.update_or_create(
                    name=row["センター名"],
                    defaults={
                        "address": row["施設住所"],
                        "phone": row["電話番号"],
                    },
                )
        logging.info("Successfully fetched data from API")
    except Exception as e:
        logging.error(f"Error fetching data from API: {e}")

    logging.info("Data fetch process from API completed")


def index(request):
    """
    子育て支援施設の一覧を表示するビュー。
    市町村名でフィルタリングが可能。
    """
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    # APIからデータを取得
    fetch_data_from_api()

    # 市町村名でフィルタリング
    selected_city = request.GET.get("city")
    playgrounds = Playground.objects.all()
    if selected_city:
        playgrounds = playgrounds.filter(address__icontains=selected_city)

    # 全件数とフィルタリング後の件数を取得
    total_count = Playground.objects.count()
    filtered_count = playgrounds.count()

    # PlaygroundオブジェクトをJSON形式に変換
    playgrounds_json = json.dumps(
        list(playgrounds.values("id", "name", "address", "phone"))
    )

    # ユーザーのお気に入りの施設IDを取得
    favorite_ids = []
    favorites = []
    favorites_json = "[]"
    if request.user.is_authenticated:
        favorite_ids = list(
            Favorite.objects.filter(user=request.user).values_list(
                "playground_id", flat=True
            )
        )
        favorite_ids = [str(id) for id in favorite_ids]  # IDを文字列に変換
        fav_objs = Favorite.objects.filter(user=request.user).select_related(
            "playground"
        )
        favorites = [fav.playground for fav in fav_objs]
        favorites_json = json.dumps(
            [
                {"name": p.name, "address": p.address, "phone": p.phone}
                for p in favorites
            ]
        )

    # テンプレートにデータを渡してレンダリング
    return render(
        request,
        "index.html",
        {
            "playgrounds": playgrounds,
            "selected_city": selected_city,
            "total_count": total_count,
            "filtered_count": filtered_count,
            "playgrounds_json": playgrounds_json,
            "google_maps_api_key": google_maps_api_key,
            "favorite_ids": favorite_ids,
            "favorites": favorites,
            "favorites_json": favorites_json,
        },
    )


def search_place(request):
    """
    Google Places APIを使用して施設を検索し、最も近い結果を返す関数。
    """
    # リクエストからパラメータを取得
    name = request.GET.get("name")
    address = request.GET.get("address")
    phone = request.GET.get("phone")

    logging.info(f"Searching for place: name={name}, address={address}, phone={phone}")

    # Google Places APIのURLを生成
    search_url = (
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        f"?input={urllib.parse.quote(name)}"
        "&inputtype=textquery"
        "&fields=name,formatted_address,geometry"
        f"&key={GOOGLE_MAPS_API_KEY}"
    )

    try:
        # APIからデータを取得
        with urllib.request.urlopen(search_url) as response:
            data = json.loads(response.read().decode())
            logging.info(f"Google Places API response: {data}")
            candidates = data.get("candidates", [])
            # 住所が一致する候補を探す
            for candidate in candidates:
                if address in candidate.get("formatted_address", ""):
                    return JsonResponse(
                        {
                            "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                        }
                    )
            # 候補が見つからない場合、最初の候補を返す
            if candidates:
                candidate = candidates[0]
                return JsonResponse(
                    {
                        "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                    }
                )
            return JsonResponse({"error": "No matching candidates found"}, status=404)
    except Exception as e:
        logging.error(f"Error searching place: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def user_login(request):
    """
    ユーザーのログインを処理するビュー。
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # 変更: トップページのmypageタブを表示するようリダイレクト
                return redirect("/?tab=mypage")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    """
    ユーザーのログアウトを処理するビュー。
    """
    logout(request)
    return redirect("index")


def register(request):
    """
    ユーザーの登録を処理するビュー。
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # 変更：標準のUserCreationFormを使用
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = UserCreationForm()  # 変更：標準のUserCreationFormを使用
    return render(request, "register.html", {"form": form})


@require_POST
@login_required
def add_favorite(request):
    """
    ユーザーがお気に入りの施設を登録するビュー。
    """
    playground_id = request.POST.get("playground_id")
    playground = Playground.objects.get(id=playground_id)
    Favorite.objects.get_or_create(user=request.user, playground=playground)
    return JsonResponse({"status": "ok"})


@require_POST
@login_required
def remove_favorite(request):
    """
    ユーザーのお気に入りの施設を削除するビュー。
    """
    playground_id = request.POST.get("playground_id")
    playground = Playground.objects.get(id=playground_id)
    Favorite.objects.filter(user=request.user, playground=playground).delete()
    return JsonResponse({"status": "ok"})


@login_required
def mypage(request):
    """
    ユーザーのマイページを表示するビュー。
    """
    favorites = Favorite.objects.filter(user=request.user).select_related("playground")
    favorite_playgrounds = [favorite.playground for favorite in favorites]
    favorite_ids = [
        str(p.id) for p in favorite_playgrounds
    ]  # 追加：お気に入り施設のIDを文字列に変換してリスト化
    playgrounds_json = json.dumps(
        [
            {"name": p.name, "address": p.address, "phone": p.phone}
            for p in favorite_playgrounds
        ]
    )
    return render(
        request,
        "mypage.html",
        {
            "favorites": favorite_playgrounds,
            "favorite_ids": favorite_ids,  # 追加
            "playgrounds_json": playgrounds_json,
            "google_maps_api_key": os.getenv("GOOGLE_MAPS_API_KEY"),
        },
    )


@login_required
def add_review(request, playground_id):
    """
    口コミを投稿するビュー
    """
    if request.method == "POST":
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        # 対象の施設を取得
        playground = get_object_or_404(Playground, id=playground_id)

        # 口コミを作成
        Review.objects.create(
            playground=playground, user=request.user, content=content, rating=rating
        )

        return JsonResponse(
            {"status": "success", "message": "口コミが投稿されました！"}
        )

    return JsonResponse(
        {"status": "error", "message": "無効なリクエストです。"}, status=400
    )


def view_reviews(request, playground_id):
    """
    指定された施設の口コミを表示するビュー
    """
    playground = get_object_or_404(Playground, id=playground_id)
    reviews = Review.objects.filter(playground=playground).select_related("user")
    return render(
        request,
        "view_reviews.html",
        {
            "playground": playground,
            "reviews": reviews,
        },
    )
