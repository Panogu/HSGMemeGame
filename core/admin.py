from django.contrib import admin

from .models import Card, Player, Game

# Register your models here.
admin.site.register(Card)
admin.site.register(Player)
admin.site.register(Game)