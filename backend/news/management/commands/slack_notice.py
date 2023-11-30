from concurrent.futures import thread
from django.core.management.base import BaseCommand
from news.models import News, Thread, Message
from datetime import datetime, timedelta
from django.conf import settings
from slack_sdk import WebClient
from django.utils import timezone


class Command(BaseCommand):
    def send_message(self, blocks=[], thread_id=None, text=""):
        client = WebClient(token=settings.SLACK_BOT_TOKEN)
        response = client.chat_postMessage(
            channel=settings.SLACK_CHANNEL,
            text=text,
            blocks=blocks,
            username="Thời sự AI",
            thread_ts=thread_id,
            mrkdwn=True,
            link_names=True,
        )
        return response

    def handle(self, *args, **options):
        compare_today = timezone.now() - timedelta(days=3)

        # Get all news with the following condition: is_summary=True and summary != "" and is_sent=False and published_at in last 3 days
        unsent_news = News.objects.filter(
            is_summary=True,
            summary__isnull=False,
            is_send=False,
            published_at__gte=compare_today,
        )

        if unsent_news:
            # Check today thread. If today thread is not exist, create new thread
            thread_obj = Thread.objects.filter(
                created_at__date=timezone.now().date(),
                channel_name=settings.SLACK_CHANNEL,
            ).first()
            if not thread_obj:
                response = self.send_message(
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"@channel *TIN TỨC MỚI NHẤT VỀ AI HÔM NAY*\n\nCác tin tức sẽ được cập nhật dưới thread này_",
                            },
                        }
                    ]
                )
                thread_id = response["ts"]
                # Save the thread in the database
                thread_obj = Thread.objects.create(
                    thresh_id=thread_id, channel_name=settings.SLACK_CHANNEL
                )

            # Get the thread_id
            thread_id = thread_obj.thresh_id

            # Push the message to slack with markdown format
            for article in unsent_news:
                text = f"{article.title} \n {article.summary} \n Link: {article.url}"
                # Send message to slack with thread ts
                response = self.send_message(
                    text=text,
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*<{article.url}|{article.title}>*",
                            },
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"\n\n{article.summary}",
                            },
                        },
                    ],
                    thread_id=thread_id,
                )
                if response["ok"]:
                    # Create message in database
                    Message.objects.create(thread=thread_obj, content=text)

                    # Update article status
                    article.is_send = True
                    article.save()
                    # Print success message
                    self.stdout.write(
                        self.style.SUCCESS(f"Send {article.title} success!")
                    )
                else:
                    self.stdout.write(self.style.ERROR(f"Send {article.title} failed!"))
