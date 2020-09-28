import uuid

from django.db import models


class BotSession(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=32)
    is_main = models.BooleanField(default=False)
    entry_keyword = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class BotQuestion(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    bot_session = models.ForeignKey(
        "BotSession", on_delete=models.PROTECT, blank=True, null=True
    )
    question = models.TextField(blank=True)
    alternative_question = models.TextField(blank=True)
    accepted_keywords = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)

    class Meta(object):
        ordering = ["position"]

    def __str__(self):
        return self.question if self.question else self.id


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    session_id = models.CharField(max_length=64)
    last_question = models.TextField(blank=True)

    def __str__(self):
        return f"Conversation for session ID {self.session_id}"


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    conversation = models.ForeignKey("Conversation", on_delete=models.CASCADE)
    bot_question = models.ForeignKey("BotQuestion", on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
