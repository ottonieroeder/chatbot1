from django.contrib import admin

from chatbot.models import BotQuestion, BotSession, Conversation, UserAnswer


class BotQuestionInline(admin.StackedInline):
    model = BotQuestion
    extra = 0


class BotSessionAdmin(admin.ModelAdmin):
    inlines = [
        BotQuestionInline,
    ]


class ConversationAdmin(admin.ModelAdmin):
    pass


class UserAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(BotSession, BotSessionAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
