from io import StringIO
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from newspaper import Article
from django.core.management.base import BaseCommand
from news.models import News
from news.helpers.summary import Summarizer


class Command(BaseCommand):
    def handle(self, *args, **options):
        summarizer = Summarizer()
        news = News.objects.filter(is_summary=False)

        for new in news:
            if not new.content:
                continue
            output = summarizer.summary(new.content)
            new.summary = output
            new.is_summary = True
            new.save()
            # Print success message
            self.stdout.write(
                self.style.SUCCESS(f"Summary content for {new.title} success!")
            )
