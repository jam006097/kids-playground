from django.shortcuts import render
from .models import Playground
import urllib.request
import json
import logging
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

API_URL = 'https://data.bodik.jp/api/3/action/datastore_search?resource_id=2ed1eb60-1a5d-46fc-9e55-cd1c35f2be93'
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

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
