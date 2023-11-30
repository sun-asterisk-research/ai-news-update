from django.contrib import admin
from .models import News, Thread, Message


# Create ModelAdmin for News
class NewsAdmin(admin.ModelAdmin):
    # Add the list_display attribute to display the fields: title, url, crawled_at, created_at, updated_at, sent_at, is_summary, is_send, is_valid
    list_display = (
        "title",
        "url",
        "crawled_at",
        "created_at",
        "updated_at",
        "sent_at",
        "is_summary",
        "is_send",
        "is_valid",
    )

    # Create the list filter with is_summary, is_send, is_valid
    list_filter = ("is_summary", "is_send", "is_valid")

    # Create search field
    search_fields = ["title"]


# Create ModelAdmin for Thread and Message
class ThreadAdmin(admin.ModelAdmin):
    # Add the list_display attribute to display the fields: thresh_id, channel_name, message, created_at, updated_at
    list_display = (
        "thresh_id",
        "channel_name",
        "content",
        "created_at",
        "updated_at",
    )

    # Create search field
    search_fields = ["thresh_id"]


class MessageAdmin(admin.ModelAdmin):
    # Add the list_display attribute to display the fields: thread_id, message, created_at, updated_at
    list_display = (
        "thread",
        "content",
        "created_at",
        "updated_at",
    )

    # Create search field
    search_fields = ["thread"]


# Register admin for the models News, Thread, Message
admin.site.register(News, NewsAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
