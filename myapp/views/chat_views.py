from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = "chatbot/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dify_chatbot_url"] = "https://udify.app/chatbot/eg44ZevsAZ5WEBPl"
        return context
