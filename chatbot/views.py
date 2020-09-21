import json
import os

from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse

from chatterbot import ChatBot
from chatterbot import comparisons, response_selection
from chatbot.settings import CORPUS_DIR
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

logging.basicConfig(level=logging.INFO)


class ChatterBotAppView(TemplateView):
    template_name = "app.html"


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    isa_bot = ChatBot(
        "Isabot",
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": comparisons.LevenshteinDistance,
                "response_selection_method": response_selection.get_first_response,
            },
        ],
    )

    trainer = ChatterBotCorpusTrainer(isa_bot)

    corpus = os.path.join(CORPUS_DIR, "investi.yml")
    trainer.train(corpus)

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

        response = self.isa_bot.get_response(input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({"name": self.isa_bot.name})
