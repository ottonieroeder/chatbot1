import requests

from django.test import LiveServerTestCase
from chatbot.models import Conversation
from chatbot.tests.factories import BotSessionFactory, BotQuestionFactory


class IsabotAPITest(LiveServerTestCase):
    def test_get_conversation_200(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_conversation_creates_a_session(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        self.assertTrue(response.cookies._find("sessionid") != "")

    def test_get_conversation_creates_new_session_if_called_again(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        session_id_1 = response.cookies._find("sessionid")

        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        session_id_2 = response.cookies._find("sessionid")

        self.assertTrue(session_id_1 != "")
        self.assertTrue(session_id_2 != "")
        self.assertTrue(session_id_1 != session_id_2)

    def test_get_conversation_creates_conversation_object(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        conversation = Conversation.objects.first()
        session_id = response.cookies._find("sessionid")

        self.assertTrue(conversation is not None)
        self.assertEquals(session_id, conversation.session_id)

    def test_get_conversation_response_keys(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        # THEN
        response_data = response.json()
        self.assertEqual(4, len(response_data))
        self.assertTrue("text" in response_data)
        self.assertTrue("botSessionId" in response_data)
        self.assertTrue("questionId" in response_data)
        self.assertTrue("conversationId" in response_data)

    def test_get_conversation_returns_error_if_no_bot_session(self):
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        self.assertEqual(response.status_code, 404)

    def test_get_conversation_returns_error_if_no_question_for_bot_session(self):
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)
        BotSessionFactory(is_main=True)

        self.assertEqual(response.status_code, 404)

    def test_get_conversation_saves_current_question_on_conversation(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        requests.get(url)

        # THEN
        conversation = Conversation.objects.first()
        self.assertEqual("First question", conversation.last_question)

    def test_get_conversation_returns_correct_values(self):
        # GIVEN
        botsession = BotSessionFactory(is_main=True)
        question = BotQuestionFactory(bot_session=botsession, question="First question")

        # WHEN
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        # THEN
        conversation = Conversation.objects.first()

        self.assertEqual("First question", response.json().get("text"))
        self.assertEqual(str(botsession.id), response.json().get("botSessionId"))
        self.assertEqual(str(question.id), response.json().get("questionId"))
        self.assertEqual(str(conversation.id), response.json().get("conversationId"))
