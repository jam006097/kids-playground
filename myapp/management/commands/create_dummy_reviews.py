import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from myapp.models import Playground, Review


class Command(BaseCommand):
    help = "Creates random dummy reviews for existing playgrounds."

    def handle(self, *args, **options):
        User = get_user_model()

        # 既存の施設とユーザーを取得
        playgrounds = Playground.objects.all()
        users = User.objects.all()

        if not playgrounds:
            self.stdout.write(
                self.style.WARNING(
                    "No playgrounds found. Please create some playgrounds first."
                )
            )
            return
        if not users:
            self.stdout.write(
                self.style.WARNING("No users found. Please create some users first.")
            )
            return

        Review.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted all existing reviews."))
        self.stdout.write(
            self.style.SUCCESS(
                f"Found {playgrounds.count()} playgrounds and {users.count()} users."
            )
        )

        # 評価に応じた口コミテンプレート
        review_templates = {
            5: [
                "最高でした！子供がとても楽しんでいました。また来たいです！",
                "素晴らしい施設です。清潔で設備も充実しており、一日中楽しめました。",
                "スタッフの方々も親切で、安心して遊ばせることができました。大満足です！",
                "期待以上の体験でした。子供の笑顔がたくさん見られて幸せです。",
                "文句なしの星5つです！家族みんなで最高の思い出ができました。",
                "リピート確定です。子供のお気に入りの場所になりました。",
                "施設が新しく、とても綺麗でした。隅々まで清掃が行き届いています。",
                "一日中いても飽きないくらい、遊具が豊富で楽しかったです。",
                "食事ができるスペースもあって、一日中過ごせます。",
                "アクセスも良く、駐車場も広くて便利でした。",
            ],
            4: [
                "とても良かったです。子供も喜んでいました。",
                "清潔感があり、快適に過ごせました。また利用したいと思います。",
                "概ね満足です。一日中楽しめました。",
                "楽しい時間を過ごせました。おすすめです。",
                "設備も充実しており、子供が飽きずに遊んでいました。",
                "週末は少し混んでいましたが、それでも十分楽しめました。",
                "食事がもう少し充実していると、さらに良いと思います。",
                "また来たいと思える、良い施設でした。",
                "スタッフの対応も丁寧で、好感が持てました。",
            ],
            3: [
                "普通です。可もなく不可もなくといった印象。",
                "特に問題なく利用できました。特筆すべき点はありません。",
                "まあまあ楽しめました。期待していたほどではなかったです。",
                "もう少し改善の余地があると感じました。",
                "悪くはないですが、リピートするかは微妙です。",
                "一度行けば十分かな、という感じです。",
                "料金相応の内容だと思います。",
            ],
            2: [
                "少し残念な点がありました。改善に期待します。",
                "想像していたより狭く、少し窮屈に感じました。",
                "休日は人が多くて、ゆっくり遊ぶのは難しいかもしれません。",
                "設備の一部が古くなっているのが気になりました。",
                "案内が少し分かりにくく、迷ってしまいました。",
                "トイレが少し汚れていて、気になりました。",
                "スタッフさんの私語が少し気になりました。",
            ],
            1: [
                "あまり楽しめませんでした。期待外れでした。",
                "清掃が少し行き届いていないように感じました。",
                "スタッフの方の対応が少し気になりました。",
                "料金の割には、内容が少し物足りないかもしれません。",
                "子供には合わなかったようです。すぐに飽きてしまいました。",
                "もう行くことはないと思います。",
                "安全面で少し不安に感じる部分がありました。",
            ],
        }

        total_reviews_created = 0
        for playground in playgrounds:
            # 各施設にランダムな数の口コミを生成 (20〜50件)
            num_reviews = random.randint(20, 50)
            self.stdout.write(
                f"Creating {num_reviews} reviews for {playground.name}..."
            )

            for _ in range(num_reviews):
                # 90%の確率でポジティブ(4-5)、10%の確率でネガティブ(1-2)な評価を生成
                if random.random() < 0.9:
                    rating = random.randint(4, 5)
                else:
                    rating = random.randint(1, 2)

                comment = random.choice(review_templates[rating])
                user = random.choice(users)

                Review.objects.create(
                    playground=playground, user=user, rating=rating, content=comment
                )
                total_reviews_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {total_reviews_created} dummy reviews."
            )
        )
