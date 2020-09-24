from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        from chatterbot import ChatBot
        from chatterbot.ext.django_chatterbot import settings
        from chatterbot.trainers import ChatterBotCorpusTrainer

        isabot = ChatBot(**settings.CHATTERBOT)
        trainer = ChatterBotCorpusTrainer(isabot)
        trainer.train(*settings.CHATTERBOT['training_data'])

        logger.info(f"Trained isabot successfully")