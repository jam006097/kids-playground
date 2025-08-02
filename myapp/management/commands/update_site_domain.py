from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Updates the default site domain and name for local development."

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(pk=1)
            original_domain = site.domain
            site.domain = "127.0.0.1:8000"
            site.name = "KidsPlayGround Local"
            site.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully updated site domain from '{original_domain}' to '{site.domain}'"
                )
            )
        except Site.DoesNotExist:
            self.stderr.write(self.style.ERROR("Site with pk=1 does not exist."))
