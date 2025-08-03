from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/mypage.html"
