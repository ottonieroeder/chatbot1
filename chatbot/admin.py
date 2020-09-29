from django.contrib import admin

from chatbot.models import BotQuestion, BotSession, Conversation, UserAnswer


class BotQuestionInline(admin.StackedInline):
    model = BotQuestion
    extra = 0


class BotSessionAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    inlines = [
        BotQuestionInline,
    ]


class ConversationAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "session_id", "last_question"]


class UserAnswerAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "conversation", "bot_question", "answer_text"]


admin.site.register(BotSession, BotSessionAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
