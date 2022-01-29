from django.contrib.auth.models import User
from django.db import models
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
    status = models.IntegerField(verbose_name=_('Status'), choices=GameStatus.choices)
    created = models.DateTimeField(verbose_name=_('Created date'), auto_now_add=True)

    class Meta:
        verbose_name = _('Game')
        verbose_name_plural = _('Games')


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


class Card(models.Model):
    word = models.CharField(verbose_name=_('Word'), max_length=20, unique=True)
    language = models.IntegerField(verbose_name=_('Language'), choices=LanguageType.choices)

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')

    def __str__(self) -> str:
        return self.word
