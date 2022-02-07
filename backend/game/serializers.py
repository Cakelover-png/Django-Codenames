from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from game.choices import GameStatus, TeamType
from game.models import Game, Spymaster, FieldOperative, GameCard


class FieldOperativeSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = FieldOperative
        exclude = ('game',)

    @staticmethod
    def get_player(obj: FieldOperative):
        return obj.player.username


class SpymasterSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = Spymaster
        exclude = ('game',)

    @staticmethod
    def get_player(obj: Spymaster):
        return obj.player.username


class SpyMasterGameCardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = GameCard
        exclude = ('game', 'card')

    @staticmethod
    def get_name(obj: GameCard):
        return obj.card.word


class FieldOperativeGameCardSerializer(SpyMasterGameCardSerializer):
    team = serializers.SerializerMethodField()
    is_assassin = serializers.SerializerMethodField()

    @staticmethod
    def get_team(obj: GameCard):
        if obj.is_guessed:
            return obj.team
        return None

    @staticmethod
    def get_is_assassin(obj: GameCard):
        if obj.is_guessed:
            return obj.is_assassin
        return False


class RetrieveGameSerializer(serializers.ModelSerializer):
    field_operatives = serializers.SerializerMethodField()
    spymasters = serializers.SerializerMethodField()
    game_cards = serializers.SerializerMethodField()
    left_red_card_count = serializers.SerializerMethodField()
    left_blue_card_count = serializers.SerializerMethodField()
    can_play = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'field_operatives', 'spymasters', 'is_creator',
                  'game_cards', 'status', 'last_turn', 'can_play', 'guess_time',
                  'left_red_card_count', 'left_blue_card_count')

    @staticmethod
    def get_field_operatives(obj: Game):
        return FieldOperativeSerializer(obj.fieldoperative, many=True).data

    @staticmethod
    def get_spymasters(obj: Game):
        return SpymasterSerializer(obj.spymaster, many=True).data

    def get_game_cards(self, obj: Game):
        user = self.context['scope']['user']
        if obj.spymaster.filter(player_id=user.id).exists() or obj.status == GameStatus.FINISHED:
            return SpyMasterGameCardSerializer(obj.game_cards, many=True).data
        else:
            return FieldOperativeGameCardSerializer(obj.game_cards, many=True).data

    @staticmethod
    def get_left_red_card_count(obj: Game):
        return 9 - obj.game_cards.filter(is_guessed=True, team=TeamType.RED).count()

    @staticmethod
    def get_left_blue_card_count(obj: Game):
        return 8 - obj.game_cards.filter(is_guessed=True, team=TeamType.BLUE).count()

    def get_can_play(self, obj: Game):
        user = self.context['scope']['user']
        last_turn = obj.last_turn
        return obj.fieldoperative.filter(player_id=user.id, team=last_turn).exists()

    def get_is_creator(self, obj: Game):
        user = self.context['scope']['user']
        return obj.creator.id == user.id


class CreateGameSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Game
        fields = ('id', 'creator',)

    def create(self, validated_data):
        game = Game(**validated_data)
        game.save()
        game.players_in_lobby.add(validated_data['creator'])
        return game


class ListGameSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    player_count_in_lobby = serializers.SerializerMethodField()

    class Meta:
        model = Game
        exclude = ('players_in_lobby', 'last_turn')

    @staticmethod
    def get_creator(obj: Game):
        return obj.creator.username

    @staticmethod
    def get_player_count_in_lobby(obj: Game):
        return obj.players_in_lobby.count()
