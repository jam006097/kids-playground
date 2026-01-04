from django.shortcuts import render


def about_view(request):
    return render(request, "myapp/about.html")
