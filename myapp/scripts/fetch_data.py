import json
import requests
import csv
import logging
import schedule
import time
from myapp.models import Playground

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("data_fetch.log"),  # ログを外部ファイルに保存
        logging.StreamHandler(),  # コンソールにもログを表示
    ],
)

# 定数を使用してマジックナンバーを避ける
URLS_FILE_PATH = "urls.json"  # URLリストが保存されているJSONファイルのパス
ENCODING = "shift_jis"  # CSVファイルのエンコーディング
HTTP_STATUS_OK = 200  # HTTPステータスコード200を定数として定義
LOCAL_CSV_FILE_PATH = "local_data.csv"  # ローカルCSVファイルのパス


def fetch_data():
    """
    URLリストからデータを取得し、データベースに保存する関数。
    """
    logging.info("Starting data fetch process")

    # URLリストを読み込む
    try:
        with open(URLS_FILE_PATH, "r") as file:
            urls = json.load(file)
        logging.info(f"Loaded URLs from {URLS_FILE_PATH}")
    except Exception as e:
        logging.error(f"Failed to load URLs from {URLS_FILE_PATH}: {e}")
        return

    # 各URLからデータを取得し、データベースに保存する
    for prefecture, url in urls.items():
        try:
            response = requests.get(url)
            if response.status_code == HTTP_STATUS_OK:
                data = response.content.decode(ENCODING)
                reader = csv.DictReader(data.splitlines())
                for row in reader:
                    Playground.objects.update_or_create(
                        name=row["センター名"],
                        defaults={
                            "prefecture": prefecture,
                            "address": row["施設住所"],
                            "phone": row["電話番号"],
                        },
                    )
                logging.info(f"Successfully fetched data from {url}")
            else:
                logging.warning(
                    f"Failed to fetch data from {url}: HTTP {response.status_code}"
                )
        except Exception as e:
            logging.error(f"Error fetching data from {url}: {e}")

    logging.info("Data fetch process completed")


def fetch_data_from_local_csv():
    """
    ローカルのCSVファイルからデータを読み込み、データベースに保存する関数。
    """
    logging.info("Starting data fetch process from local CSV")

    try:
        with open(LOCAL_CSV_FILE_PATH, "r", encoding=ENCODING) as file:
            reader = csv.DictReader(file)
            for row in reader:
                Playground.objects.update_or_create(
                    name=row["センター名"],
                    defaults={
                        "prefecture": row["都道府県"],
                        "address": row["施設住所"],
                        "phone": row["電話番号"],
                    },
                )
        logging.info(f"Successfully fetched data from {LOCAL_CSV_FILE_PATH}")
    except Exception as e:
        logging.error(f"Error fetching data from {LOCAL_CSV_FILE_PATH}: {e}")

    logging.info("Data fetch process from local CSV completed")


def schedule_monthly_fetch():
    """
    1ヶ月に一度fetch_data関数を実行するスケジューリング関数。
    """
    schedule.every(30).days.do(fetch_data)
    logging.info("Scheduled fetch_data to run every 30 days")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    fetch_data_from_local_csv()
    # schedule_monthly_fetch()  # 必要に応じてコメントアウトを解除
