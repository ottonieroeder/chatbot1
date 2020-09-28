import json
import logging
import os

from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from chatbot import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

isa_bot = ChatBot(**settings.CHATTERBOT)


class IsabotAppView(TemplateView):
    template_name = "chatbot/app.html"


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def get_conversation(request: Request) -> Response:
    if not request.session.session_key:
        request = request.session.create()

    session_id = request.session.session_key
    conversation, created = models.Conversation.objects.get_or_create(
        session_id=session_id
    )
    bot_session = models.BotSession.objects.filter(is_main=True).first()
    first_question = bot_session.botquestion_set.filter(position=0).first()
    conversation.last_question = first_question.question
    conversation.save()

    response_data = {
        "text": first_question.question,
        "botSessionId": first_question.bot_session.id,
        "questionId": first_question.id,
        "conversationId": conversation.id,
    }
    return Response(response_data, 200)


@api_view(["POST"])
@renderer_classes((JSONRenderer,))
def post_message(request: Request) -> Response:
    response_data = {}

    # catch if no session Id
    session_id = request.session.session_key
    conversationId = request.data.get("conversationId")
    bot_session_id = request.data.get("botSessionId")
    questionId = request.data.get("questionId")
    user_input = request.data.get("text")

    # catch ConversationDoesNotExist
    conversation = models.Conversation.objects.get(id=conversationId)
    bot_session = models.BotSession.objects.get(id=bot_session_id)
    old_question = models.BotQuestion.objects.get(id=questionId)
    # get next question
    next_question_position = old_question.position + 1
    next_question = bot_session.botquestion_set.filter(
        position=next_question_position
    ).first()

    if old_question.accepted_keywords:
        keyword_list = old_question.accepted_keywords.split(",")
        if (
            user_input not in keyword_list
            and conversation.last_question == old_question.alternative_question
        ):
            # return bot answer
            isa_response = isa_bot.get_response(user_input)
            response_data["text"] = isa_response.text
            response_data["botSessionId"] = ""
            response_data["questionId"] = ""
            response_data["conversationId"] = conversation.id

            return Response(response_data, 200)
        if (
            user_input not in keyword_list
            and conversation.last_question != old_question.alternative_question
        ):
            # return alternative question
            conversation.last_question = old_question.alternative_question
            conversation.save()

            response_data["text"] = old_question.alternative_question
            response_data["botSessionId"] = bot_session.id
            response_data["questionId"] = old_question.id
            response_data["conversationId"] = conversation.id

            return Response(response_data, 200)

        if user_input in keyword_list and next_question:
            # return next question
            models.UserAnswer.objects.create(
                conversation=conversation,
                bot_question=old_question,
                answer_text=user_input,
            )

            conversation.last_question = next_question.question
            conversation.save()

            response_data["text"] = next_question.question
            response_data["botSessionId"] = bot_session.id
            response_data["questionId"] = next_question.id
            response_data["conversationId"] = conversation.id

            return Response(response_data, 200)

        if user_input in keyword_list and not next_question:
            # check if new bot session (entry_keys) exists
            bot_session = models.BotSession.objects.filter(
                is_main=False, entry_keyword=user_input
            ).first()

            if bot_session:
                models.UserAnswer.objects.create(
                    conversation=conversation,
                    bot_question=old_question,
                    answer_text=user_input,
                )
                next_question = bot_session.botquestion_set.filter(position=0).first()
                conversation.last_question = next_question.question
                conversation.save()

                response_data["text"] = next_question.question
                response_data["botSessionId"] = bot_session.id
                response_data["questionId"] = next_question.id
                response_data["conversationId"] = conversation.id

            return Response(response_data, 200)

    elif next_question:
        # return next question
        models.UserAnswer.objects.create(
            conversation=conversation,
            bot_question=old_question,
            answer_text=user_input,
        )

        conversation.last_question = next_question.question
        conversation.save()

        response_data["text"] = next_question.question
        response_data["botSessionId"] = bot_session.id
        response_data["questionId"] = next_question.id
        response_data["conversationId"] = conversation.id

        return Response(response_data, 200)

    else:
        # return bot answer
        isa_response = isa_bot.get_response(user_input)
        response_data["text"] = isa_response.text
        response_data["botSessionId"] = ""
        response_data["questionId"] = ""
        response_data["conversationId"] = conversation.id

        return Response(response_data, 200)
