from django.db import models


# Create the news model with the following fields: title, url, crawled_at, created_at, updated_at, sent_at, is_summary, is_send, is_valid
class News(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=1000)
    # Add the original source of the news crawled
    source = models.CharField(max_length=1000, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    is_summary = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)

    crawled_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.title


# Create the Thread model with the following fields: thresh_id, channel_name, message, created_at, updated_at, sent_at
class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    thresh_id = models.CharField(max_length=100)
    channel_name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.thresh_id


# Create the Message model with the following fields: thread_id, message, created_at, updated_at
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.id
