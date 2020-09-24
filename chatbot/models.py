import uuid

from django.db import models

class BotConsultation(models.Model):
    name = models.CharField(max_length=32)


class BotQuestion(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    consultation = models.ForeignKey(
        "BotConsultation", on_delete=models.PROTECT
    )
    question = models.CharField(max_length=64)
    accepted_keywords = models.TextField(blank=True)


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    session_id = models.CharField(max_length=64)
    last_question = models.ForeignKey(
        "BotQuestion", on_delete=models.PROTECT, null=True, blank=True
    )


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    conversation = models.ForeignKey("Conversation", on_delete=models.PROTECT)
    bot_question = models.ForeignKey("BotQuestion", on_delete=models.PROTECT)
    answer_text = models.TextField()
