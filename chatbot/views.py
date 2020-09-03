import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from chatbot.settings import CORPUS_DIR





class ChatterBotAppView(TemplateView):
    template_name = "app.html"


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    investi_bot = ChatBot(**settings.CHATTERBOT)

    trainer = ChatterBotCorpusTrainer(investi_bot)

    corpus = os.path.join(CORPUS_DIR, "investi.yml")
    trainer.train(
        corpus
    )

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode("utf-8"))

        if "text" not in input_data:
            return JsonResponse(
                {"text": ['The attribute "text" is required.']}, status=400
            )

        response = self.investi_bot.get_response(input_data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({"name": self.investi_bot.name})
