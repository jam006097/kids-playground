from django.core.management.base import BaseCommand
from myapp.fetch_data import fetch_data

class Command(BaseCommand):
    """
    Django管理コマンド: fetch_playgrounds
    URLリストから子育て支援施設のデータを取得するコマンド。
    """
    help = 'Fetch playground data from URLs list'

    def handle(self, *args, **kwargs):
        fetch_data()
        self.stdout.write(self.style.SUCCESS('Successfully fetched playground data'))
