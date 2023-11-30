from io import StringIO
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from newspaper import Article
from django.core.management.base import BaseCommand
from news.models import News
from news.helpers.utils import get_parent_link


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://www.futuretools.io/news"

        # Send a GET request to the website
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all the news article links

        news_articles = soup.find_all("a", class_="link-block-8")

        # Find exist link with News model in list
        exist_links = News.objects.values_list("url", flat=True)

        # Extract the titles and URLs of the news articles

        for article in news_articles:
            title = article.text.strip()
            article_url = article["href"].replace("?ref=futuretools.io", "")
            # Append the result to the list if it is not in the list yet
            if article_url in list(exist_links):
                continue

            try:
                crawler = Article(article_url)
                crawler.download()
                crawler.parse()
                content = crawler.text
                published_at = crawler.publish_date
                # set crawled_at is datetime now
                crawled_at = datetime.now()
                # Set source field is the parent link of article
                source = get_parent_link(crawler.source_url)

                if content and published_at:
                    news = News(
                        title=title,
                        url=article_url,
                        source=source,
                        content=content,
                        crawled_at=crawled_at,
                        published_at=published_at,
                    )
                    news.save()

                    # Message success insert to database with article link and title
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully crawled: {title}")
                    )
            except:
                self.stdout.write(
                    self.style.NOTICE(f"Error when crawling: {article_url}")
                )
