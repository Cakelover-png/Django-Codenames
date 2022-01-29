from django.db import models
from django.utils.translation import gettext_lazy as _


class LanguageType(models.IntegerChoices):
    GEORGIAN = 0, _('Georgian')
    ENGLISH = 1, _('English')
    RUSSIAN = 2, _('Russian')


class GameStatus(models.IntegerChoices):
    PENDING = 0, _('Pending'),
    STARTED = 1, _('Started')
    FINISHED = 2, _('Finished')


class TeamType(models.IntegerChoices):
    RED = 0, _('Red'),
    BLUE = 1, _('Blue')
