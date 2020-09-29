import logging

from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
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


def _build_error_response(
    error_message: str, error_fields: dict = None, error_code: str = None
) -> dict:
    error_data = {"message": error_message}
    if error_code is not None:
        error_data.update({"code": error_code})
    if error_fields is not None:
        error_data.update({"fields": error_fields})

    response = {"error": error_data}

    return response


def _get_isabot_response(user_input: str, conversation_id: str) -> dict:
    response_data = {}
    isa_response = isa_bot.get_response(user_input)
    response_data["text"] = isa_response.text
    response_data["botSessionId"] = ""
    response_data["questionId"] = ""
    response_data["conversationId"] = conversation_id

    return response_data


def _get_session_response(
    session_answer: str, bot_session_id: str, question_id: str, conversation_id: str
) -> dict:
    response_data = {}
    response_data["text"] = session_answer
    response_data["botSessionId"] = bot_session_id
    response_data["questionId"] = question_id
    response_data["conversationId"] = conversation_id

    return response_data


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
def get_conversation(request: Request) -> Response:
    bot_session = models.BotSession.objects.filter(is_main=True).first()
    if bot_session is None:
        return Response(
            _build_error_response(
                "BotSession not found", error_code="BotSessionNotFound"
            ),
            404,
        )
    first_question = bot_session.botquestion_set.filter(position=0).first()
    if first_question is None:
        return Response(
            _build_error_response(
                "No question found for main session", error_code="QuestionNotFound"
            ),
            404,
        )

    request.session.create()
    session_id = request.session.session_key

    conversation, created = models.Conversation.objects.get_or_create(
        session_id=session_id
    )

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
    conversation_id = request.data.get("conversationId")
    bot_session_id = request.data.get("botSessionId")
    question_id = request.data.get("questionId")
    user_input = request.data.get("text").lower()

    if conversation_id != "" and bot_session_id == "":
        return Response(_get_isabot_response(user_input, conversation_id), 200)

    try:
        conversation = models.Conversation.objects.get(id=conversation_id)
    except models.Conversation.DoesNotExist:
        return Response(
            _build_error_response(
                "Conversation not found for provided ID",
                error_code="ConversationNotFound",
            ),
            404,
        )
    try:
        bot_session = models.BotSession.objects.get(id=bot_session_id)
    except models.BotSession.DoesNotExist:
        return Response(
            _build_error_response(
                "BotSession not found for provided ID", error_code="BotSessionNotFound"
            ),
            404,
        )
    try:
        old_question = models.BotQuestion.objects.get(id=question_id)
    except models.BotQuestion.DoesNotExist:
        return Response(
            _build_error_response(
                "BotQuestion not found for provided ID", error_code="BotSessionNotFound"
            ),
            404,
        )

    next_question_position = old_question.position + 1
    next_question = bot_session.botquestion_set.filter(
        position=next_question_position
    ).first()

    if old_question.accepted_keywords:
        keyword_list = old_question.accepted_keywords.split(",")

        # Return bot answer
        if (
            user_input not in keyword_list
            and conversation.last_question == old_question.alternative_question
        ):
            return Response(_get_isabot_response(user_input, conversation.id), 200)

        # Return alternative question
        if (
            user_input not in keyword_list
            and conversation.last_question != old_question.alternative_question
        ):

            conversation.last_question = old_question.alternative_question
            conversation.save()

            return Response(
                _get_session_response(
                    session_answer=old_question.alternative_question,
                    bot_session_id=bot_session.id,
                    question_id=old_question.id,
                    conversation_id=conversation.id,
                ),
                200,
            )

        # Return next question
        if user_input in keyword_list and next_question:
            models.UserAnswer.objects.create(
                conversation=conversation,
                bot_question=old_question,
                answer_text=user_input,
            )
            conversation.last_question = next_question.question
            conversation.save()

            return Response(
                _get_session_response(
                    session_answer=next_question.question,
                    bot_session_id=bot_session.id,
                    question_id=next_question.id,
                    conversation_id=conversation.id,
                ),
                200,
            )

        # Return question of next session
        if user_input in keyword_list and not next_question:
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

                return Response(
                    _get_session_response(
                        session_answer=next_question.question,
                        bot_session_id=bot_session.id,
                        question_id=next_question.id,
                        conversation_id=conversation.id,
                    ),
                    200,
                )
            else:
                return Response(_get_isabot_response(user_input, conversation.id), 200)

    elif next_question:
        models.UserAnswer.objects.create(
            conversation=conversation,
            bot_question=old_question,
            answer_text=user_input,
        )

        conversation.last_question = next_question.question
        conversation.save()

        return Response(
            _get_session_response(
                session_answer=next_question.question,
                bot_session_id=bot_session.id,
                question_id=next_question.id,
                conversation_id=conversation.id,
            ),
            200,
        )

    else:
        return Response(_get_isabot_response(user_input, conversation.id), 200)
