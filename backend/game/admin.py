from django.contrib import admin

from game.models import Game, Spymaster, FieldOperative, GameCard, Card

admin.site.register([Game, Spymaster, FieldOperative, GameCard, Card])
