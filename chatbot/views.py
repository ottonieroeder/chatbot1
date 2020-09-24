import json
import os

from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse

from chatterbot import ChatBot

from chatterbot.ext.django_chatterbot import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IsabotAppView(TemplateView):
    template_name = "app.html"


class IsabotApiView(View):
    isa_bot = ChatBot(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        # import pdb;
        # pdb.set_trace()
        input_data = json.loads(request.body.decode("utf-8"))

        if "text" not in input_data:
            return JsonResponse(
                {"text": ['The attribute "text" is required.']}, status=400
            )
        # logger.info(
        #     f"Input: {input_data} /// session_id: {request.session.session_key}"
        # )

        response = self.isa_bot.get_response(input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)
