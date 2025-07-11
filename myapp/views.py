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
    model = Playground
    template_name = "index.html"
    context_object_name = "playgrounds"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.selected_city = self.request.GET.get("city")
        if self.selected_city:
            queryset = queryset.filter(address__icontains=self.selected_city)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playgrounds = context["playgrounds"]

        total_count = Playground.objects.count()
        filtered_count = playgrounds.count()

        playgrounds_json = json.dumps(
            list(playgrounds.values("id", "name", "address", "phone"))
        )

        favorite_ids = []
        favorites = []
        favorites_json = "[]"
        if self.request.user.is_authenticated:
            favorite_ids = list(
                Favorite.objects.filter(user=self.request.user).values_list(
                    "playground_id", flat=True
                )
            )
            favorite_ids = [str(id) for id in favorite_ids]
            fav_objs = Favorite.objects.filter(user=self.request.user).select_related(
                "playground"
            )
            favorites = [fav.playground for fav in fav_objs]
            favorites_json = json.dumps(
                [
                    {"name": p.name, "address": p.address, "phone": p.phone}
                    for p in favorites
                ]
            )

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
    def get(self, request, *args, **kwargs):
        name = request.GET.get("name")
        address = request.GET.get("address")
        phone = request.GET.get("phone")

        logging.info(
            f"Searching for place: name={name}, address={address}, phone={phone}"
        )

        search_url = (
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            f"?input={urllib.parse.quote(name)}"
            "&inputtype=textquery"
            "&fields=name,formatted_address,geometry"
            f"&key={GOOGLE_MAPS_API_KEY}"
        )

        try:
            with urllib.request.urlopen(search_url) as response:
                data = json.loads(response.read().decode())
                logging.info(f"Google Places API response: {data}")
                candidates = data.get("candidates", [])
                for candidate in candidates:
                    if address in candidate.get("formatted_address", ""):
                        return JsonResponse(
                            {
                                "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                            }
                        )
                if candidates:
                    candidate = candidates[0]
                    return JsonResponse(
                        {
                            "url": f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"
                        }
                    )
                return JsonResponse(
                    {"error": "No matching candidates found"}, status=404
                )
        except Exception as e:
            logging.error(f"Error searching place: {e}")
            return JsonResponse({"error": str(e)}, status=500)


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = AuthenticationForm

    def get_success_url(self):
        return "/?tab=mypage"


class UserLogoutView(LogoutView):
    next_page = "index"


class UserRegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm
    success_url = "/"


class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        Favorite.objects.get_or_create(user=request.user, playground=playground)
        return JsonResponse({"status": "ok"})


class RemoveFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        playground_id = request.POST.get("playground_id")
        playground = Playground.objects.get(id=playground_id)
        Favorite.objects.filter(user=request.user, playground=playground).delete()
        return JsonResponse({"status": "ok"})


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "mypage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favorites = Favorite.objects.filter(user=self.request.user).select_related(
            "playground"
        )
        favorite_playgrounds = [favorite.playground for favorite in favorites]
        favorite_ids = [str(p.id) for p in favorite_playgrounds]
        playgrounds_json = json.dumps(
            [
                {"name": p.name, "address": p.address, "phone": p.phone}
                for p in favorite_playgrounds
            ]
        )
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
    def post(self, request, playground_id, *args, **kwargs):
        content = request.POST.get("content")
        rating = request.POST.get("rating")

        playground = get_object_or_404(Playground, id=playground_id)

        Review.objects.create(
            playground=playground, user=request.user, content=content, rating=rating
        )

        return JsonResponse(
            {"status": "success", "message": "口コミが投稿されました！"}
        )

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"status": "error", "message": "無効なリクエストです。"}, status=400
        )


class ReviewListView(ListView):

    model = Review
    template_name = "view_reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        playground_id = self.kwargs["playground_id"]
        self.playground = get_object_or_404(Playground, id=playground_id)
        return Review.objects.filter(playground=self.playground).select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playground"] = self.playground
        return context
