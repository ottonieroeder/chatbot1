import factory

from chatbot.models import BotSession, BotQuestion, Conversation, UserAnswer


class BotSessionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BotSession

    id = factory.Faker("uuid4")
    name = factory.Faker("name")


class BotQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BotQuestion

    id = factory.Faker("uuid4")


class ConversationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Conversation

    id = factory.Faker("uuid4")
    session_id = factory.Sequence(lambda n: f"sessionid00{n}")


class UserAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAnswer

    id = factory.Faker("uuid4")
    conversation = factory.SubFactory(ConversationFactory)
    bot_question = factory.SubFactory(BotQuestionFactory)
