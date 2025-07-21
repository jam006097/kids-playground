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
