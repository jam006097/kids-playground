from django.shortcuts import render
from django.http import JsonResponse
from .models import Playground
import urllib.request
import urllib.parse  # 追加
import json
import logging
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

API_URL = 'https://data.bodik.jp/api/3/action/datastore_search?resource_id=2ed1eb60-1a5d-46fc-9e55-cd1c35f2be93'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # ログをファイルに保存
        logging.StreamHandler()  # コンソールにもログを表示
    ]
)

def fetch_data_from_api():
    """
    データAPIからデータを取得し、データベースに保存する関数。
    """
    logging.info("Starting data fetch process from API")

    try:
        with urllib.request.urlopen(API_URL) as response:
            data = json.loads(response.read().decode())
            records = data['result']['records']
            for row in records:
                Playground.objects.update_or_create(
                    name=row['センター名'],
                    defaults={
                        'address': row['施設住所'],
                        'phone': row['電話番号'],
                    }
                )
        logging.info(f"Successfully fetched data from API")
    except Exception as e:
        logging.error(f"Error fetching data from API: {e}")

    logging.info("Data fetch process from API completed")

def index(request):
    """
    子育て支援施設の一覧を表示するビュー。
    市町村名でフィルタリングが可能。
    """
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

    fetch_data_from_api()  # APIからデータを取得
    selected_city = request.GET.get('city')
    playgrounds = Playground.objects.all()
    if selected_city:
        playgrounds = playgrounds.filter(address__icontains=selected_city)
    total_count = Playground.objects.count()
    filtered_count = playgrounds.count()
    playgrounds_json = json.dumps(list(playgrounds.values('name', 'address', 'phone')))
    return render(request, 'index.html', {
        'playgrounds': playgrounds,
        'selected_city': selected_city,
        'total_count': total_count,
        'filtered_count': filtered_count,
        'playgrounds_json': playgrounds_json,
        'google_maps_api_key': google_maps_api_key
    })

def search_place(request):
    """
    Google Places APIを使用して施設を検索し、最も近い結果を返す関数。
    """
    name = request.GET.get('name')
    address = request.GET.get('address')
    phone = request.GET.get('phone')

    logging.info(f"Searching for place: name={name}, address={address}, phone={phone}")

    search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={urllib.parse.quote(name)}&inputtype=textquery&fields=name,formatted_address,geometry&key={GOOGLE_MAPS_API_KEY}"
    
    try:
        with urllib.request.urlopen(search_url) as response:
            data = json.loads(response.read().decode())
            logging.info(f"Google Places API response: {data}")
            candidates = data.get('candidates', [])
            for candidate in candidates:
                if address in candidate.get('formatted_address', ''):
                    return JsonResponse({'url': f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"})
            if candidates:
                candidate = candidates[0]
                return JsonResponse({'url': f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(name)}"})
            return JsonResponse({'error': 'No matching candidates found'}, status=404)
    except Exception as e:
        logging.error(f"Error searching place: {e}")
        return JsonResponse({'error': str(e)}, status=500)
