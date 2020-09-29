import requests

from django.test import LiveServerTestCase
from chatbot.models import Conversation, UserAnswer
from chatbot.tests.factories import BotSessionFactory, BotQuestionFactory


class IsabotAPITest(LiveServerTestCase):
    def setUp(self):
        main_session = BotSessionFactory(is_main=True)
        BotQuestionFactory(
            bot_session=main_session,
            question="Hello I am Isabot. I am your consultant to help you to invest in a post-labour future.",
        )
        BotQuestionFactory(
            bot_session=main_session, question="Hello, how are you?", position=1
        )
        BotQuestionFactory(
            bot_session=main_session,
            question="Do you work in the creative field?",
            alternative_question="Imagine that you do work in the field, ok?",
            accepted_keywords="ok,yes,yep,yo,of course,certainly,I do,I work in the creative field",
            position=2,
        )
        BotQuestionFactory(
            bot_session=main_session,
            question="As a creative, do you work in (A) product design, (B) graphic design, (C) web design, (D) architecture or (E) art? Give me the letter of your choice.",
            alternative_question="I am sorry, could you please specify between  (A) product design, (B) graphic design, (C) web design, (D) architecture or (E) art by just typing in the letter in brackets?",
            accepted_keywords="A,B,C,D,E",
            position=3,
        )

        BotSessionFactory(name="A session", entry_keyword="A")
        BotQuestionFactory(
            bot_session=main_session,
            question="Would you be up for that?",
        )
        BotQuestionFactory(
            bot_session=main_session,
            question="Do you have any further questions?",
            alternative_question="Great, thank you, it was nice talking to you. Your session has ended. Goodbye.",
            accepted_keywords="yeah,yes,yo,of course,sure",
            position=1,
        )
        BotSessionFactory(name="B session", entry_keyword="B")
        BotQuestionFactory(
            bot_session=main_session,
            question="Would you be up for that?",
        )
        BotQuestionFactory(
            bot_session=main_session,
            question="Do you have any further questions?",
            alternative_question="Great, thank you, it was nice talking to you. Your session has ended. Goodbye.",
            accepted_keywords="yeah,yes,yo,of course,sure",
            position=1,
        )

    def test_post_message_200(self):
        # Start conversation
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        bot_session_id = response.json().get("botSessionId")
        question_id = response.json().get("questionId")
        conversation_id = response.json().get("conversationId")

        url = f"{self.live_server_url}/isabot/conversation/message/"
        response = requests.post(
            url,
            headers={},
            json={
                "text": "Hi",
                "botSessionId": bot_session_id,
                "questionId": question_id,
                "conversationId": conversation_id,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_post_message_creates_user_answer(self):
        # Start conversation
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        bot_session_id = response.json().get("botSessionId")
        question_id = response.json().get("questionId")
        conversation_id = response.json().get("conversationId")

        url = f"{self.live_server_url}/isabot/conversation/message/"
        requests.post(
            url,
            headers={},
            json={
                "text": "Hi",
                "botSessionId": bot_session_id,
                "questionId": question_id,
                "conversationId": conversation_id,
            },
        )

        self.assertEqual(1, UserAnswer.objects.count())

    def test_post_message_response_keys(self):
        # Start conversation
        url = f"{self.live_server_url}/isabot/conversation/"
        response = requests.get(url)

        bot_session_id = response.json().get("botSessionId")
        question_id = response.json().get("questionId")
        conversation_id = response.json().get("conversationId")

        url = f"{self.live_server_url}/isabot/conversation/message/"
        response = requests.post(
            url,
            headers={},
            json={
                "text": "Hi",
                "botSessionId": bot_session_id,
                "questionId": question_id,
                "conversationId": conversation_id,
            },
        )
        response_data = response.json()
        self.assertEqual(4, len(response_data))
        self.assertTrue("text" in response_data)
        self.assertTrue("botSessionId" in response_data)
        self.assertTrue("questionId" in response_data)
        self.assertTrue("conversationId" in response_data)
