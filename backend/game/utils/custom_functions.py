import random

from django.contrib.auth.models import User

from game.choices import TeamType
from game.models import Game, GameCard, Card


def shuffled_game_cards(game: Game) -> list:
    cards = random.sample(list(Card.objects.all().values_list('id', flat=True)), 25)
    game_cards = [GameCard(game_id=game.id, card_id=cards[i], team=TeamType.RED) for i in range(9)]
    game_cards.extend([GameCard(game_id=game.id, card_id=cards[i], team=TeamType.BLUE) for i in range(9, 17)])
    game_cards.extend([GameCard(game_id=game.id, card_id=cards[i]) for i in range(17, 24)])
    game_cards.extend([GameCard(game_id=game.id, card_id=cards[24], is_assassin=True)])
    random.shuffle(game_cards)
    return game_cards


def set_finished_if_winner(game: Game, game_card_team: int) -> None:
    guessed_count = game.game_cards.filter(team=game_card_team, is_guessed=True).count()
    if game_card_team == TeamType.RED:
        if guessed_count == 9:
            game.set_status_finished()
    elif guessed_count == 8:
        game.set_status_finished()
