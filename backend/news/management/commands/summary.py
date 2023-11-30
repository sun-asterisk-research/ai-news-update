from django.core.management.base import BaseCommand
from news.models import News
from news.helpers.summary import Summarizer
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, *args, **options):
        summarizer = Summarizer()
        compare_today = timezone.now() - timedelta(days=3)

        news = News.objects.filter(
            is_summary=False,
            is_send=False,
            published_at__gte=compare_today,
        )

        for new in news:
            if not new.content:
                continue
            new.summary = summarizer.summary(new.content)
            new.is_summary = True
            new.save()
            # Print success message
            self.stdout.write(
                self.style.SUCCESS(f"Summary content for {new.title} success!")
            )
