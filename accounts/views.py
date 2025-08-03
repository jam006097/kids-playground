from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import AccountNameForm


class MyPageView(LoginRequiredMixin, View):
    template_name = "accounts/mypage.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AccountNameChangeView(LoginRequiredMixin, View):
    template_name = "accounts/account_name_change.html"
    success_url = reverse_lazy("accounts:mypage")

    def get(self, request, *args, **kwargs):
        form = AccountNameForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AccountNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})
