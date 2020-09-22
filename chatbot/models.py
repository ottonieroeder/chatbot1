import uuid

from django.db import models


class BotQuestion(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    session_id = models.CharField(max_length=254)


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    conversation = models.ForeignKey("Conversation", on_delete=models.PROTECT)
    bot_question = models.ForeignKey("BotQuestion", on_delete=models.PROTECT)
