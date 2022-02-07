from game.choices import TeamType
from game.models import Game


def get_query_params(query_string) -> dict:
    return dict((x.split('=') for x in query_string.decode().split("&")))


def set_finished_if_winner(game: Game, game_card_team: int) -> None:
    guessed_count = game.game_cards.filter(team=game_card_team, is_guessed=True).count()
    if game_card_team == TeamType.RED:
        if guessed_count == 9:
            game.set_status_finished()
    elif guessed_count == 8:
        game.set_status_finished()
