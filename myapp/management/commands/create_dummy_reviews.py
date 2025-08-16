import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from myapp.models import Playground, Review


class Command(BaseCommand):
    help = 'Creates random dummy reviews for existing playgrounds.'

    def handle(self, *args, **options):
        User = get_user_model()

        # 既存の施設とユーザーを取得
        playgrounds = Playground.objects.all()
        users = User.objects.all()

        if not playgrounds:
            self.stdout.write(self.style.WARNING('No playgrounds found. Please create some playgrounds first.'))
            return
        if not users:
            self.stdout.write(self.style.WARNING('No users found. Please create some users first.'))
            return

        Review.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all existing reviews.'))
        self.stdout.write(self.style.SUCCESS(f'Found {playgrounds.count()} playgrounds and {users.count()} users.'))

        # 評価に応じた口コミテンプレート
        review_templates = {
            5: [
                "最高でした！子供がとても楽しんでいました。また来たいです！",
                "素晴らしい施設です。清潔で設備も充実しており、一日中楽しめました。",
                "スタッフの方々も親切で、安心して遊ばせることができました。大満足です！",
                "期待以上の体験でした。子供の笑顔がたくさん見られて幸せです。",
                "文句なしの星5つです！家族みんなで最高の思い出ができました。"
            ],
            4: [
                "とても良かったです。子供も喜んでいました。",
                "清潔感があり、快適に過ごせました。また利用したいと思います。",
                "概ね満足です。もう少し改善点があれば完璧でした。",
                "楽しい時間を過ごせました。おすすめです。",
                "設備も充実しており、子供が飽きずに遊んでいました。"
            ],
            3: [
                "普通です。可もなく不可もなくといった印象。",
                "特に問題なく利用できました。特筆すべき点はありません。",
                "まあまあ楽しめました。期待していたほどではなかったです。",
                "もう少し改善の余地があると感じました。",
                "悪くはないですが、リピートするかは微妙です。"
            ]
        }

        total_reviews_created = 0
        for playground in playgrounds:
            # 各施設にランダムな数の口コミを生成 (10〜20件)
            num_reviews = random.randint(10, 20)
            self.stdout.write(f'Creating {num_reviews} reviews for {playground.name}...')

            for _ in range(num_reviews):
                # ランダムな評価 (3〜5)
                rating = random.randint(3, 5)
                # 評価に応じた口コミ内容をランダムに選択
                comment = random.choice(review_templates[rating])

                # ランダムなユーザーを選択
                user = random.choice(users)

                Review.objects.create(
                    playground=playground,
                    user=user,
                    rating=rating,
                    content=comment
                )
                total_reviews_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_reviews_created} dummy reviews.'))
