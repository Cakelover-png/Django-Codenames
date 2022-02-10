from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from game.choices import LanguageType, GameStatus, TeamType


class AbstractPlayer(models.Model):
    player = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               related_name='%(class)s',
                               verbose_name=_('Player'),
                               null=True)
    game = models.ForeignKey(to='game.Game',
                             on_delete=models.SET_NULL,
                             related_name='%(class)s',
                             verbose_name=_('Game'),
                             null=True)
    team = models.IntegerField(verbose_name=_('Team'), choices=TeamType.choices)

    class Meta:
        abstract = True


class Game(models.Model):
    creator = models.ForeignKey(to=User,
                                on_delete=models.SET_NULL,
                                related_name='created_games',
                                verbose_name=_('Creator'),
                                null=True)
    players_in_lobby = models.ManyToManyField(to=User,
                                              related_name='games',
                                              verbose_name=_('Players in lobby'))
    status = models.IntegerField(verbose_name=_('Status'), choices=GameStatus.choices, default=GameStatus.PENDING)
    last_turn = models.IntegerField(verbose_name=_('Last Turn'), choices=TeamType.choices, blank=True, null=True)
    guess_time = models.DateTimeField(verbose_name=_('Guess time'), blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')

    def change_turn(self):
        self.last_turn = TeamType.BLUE - F('last_turn')
        self.save(update_fields=['last_turn'])

    def set_status_finished(self):
        self.status = GameStatus.FINISHED
        self.save(update_fields=['status'])

    def set_guess_time(self):
        self.guess_time = timezone.now() + timedelta(seconds=120)
        self.save(update_fields=['guess_time'])

    def __str__(self):
        return f"{self.id} | {self.creator}'s Game"


class Spymaster(AbstractPlayer):
    class Meta:
        verbose_name = _('Spymaster')
        verbose_name_plural = _('Spymasters')


class FieldOperative(AbstractPlayer):
    class Meta:
        verbose_name = _('Field Operative')
        verbose_name_plural = _('Field Operatives')


class GameCard(models.Model):
    game = models.ForeignKey(to='game.Game',
                             on_delete=models.SET_NULL,
                             related_name='game_cards',
                             verbose_name=_('Game'),
                             null=True)
    card = models.ForeignKey(to='game.Card',
                             on_delete=models.SET_NULL,
                             related_name='game_cards',
                             verbose_name=_('Card'),
                             null=True)
    team = models.IntegerField(verbose_name=_('Team'), choices=TeamType.choices, blank=True, null=True)
    is_guessed = models.BooleanField(verbose_name=_('Is Guessed'), default=False)
    is_assassin = models.BooleanField(verbose_name=_('Is Assassin'), default=False)

    class Meta:
        verbose_name = _('Game Card')
        verbose_name_plural = _('Game Cards')

    def set_guessed(self):
        self.is_guessed = True
        self.save(update_fields=['is_guessed'])


class Card(models.Model):
    word = models.CharField(verbose_name=_('Word'), max_length=30)
    language = models.IntegerField(verbose_name=_('Language'), choices=LanguageType.choices)
    is_active = models.BooleanField(verbose_name=_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')

    def __str__(self) -> str:
        return self.word
