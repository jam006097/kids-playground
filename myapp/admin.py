from django.contrib import admin
from .models import Playground, Favorite, Review

# Register your models here.
admin.site.register(Playground)
admin.site.register(Favorite)
admin.site.register(Review)
