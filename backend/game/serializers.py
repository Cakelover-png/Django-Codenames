from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from django_codenames.utils.serializers import DynamicFieldsModelSerializer
from game.choices import GameStatus
from game.models import Game, Spymaster, FieldOperative, GameCard


class CurrentGameDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['game']


class AbstractPlayerSerializer(serializers.ModelSerializer):
    game = serializers.HiddenField(default=CurrentGameDefault())
    player = serializers.HiddenField(default=CurrentUserDefault())

    def create(self, validated_data):
        game, player = validated_data['game'], validated_data['player']
        Spymaster.objects.filter(game_id=game.id, player_id=player.id).delete()
        FieldOperative.objects.filter(game_id=game.id, player_id=player.id).delete()
        return super(AbstractPlayerSerializer, self).create(validated_data)


class CreateFieldOperativeSerializer(AbstractPlayerSerializer):
    class Meta:
        model = FieldOperative
        fields = '__all__'


class CreateSpymasterSerializer(AbstractPlayerSerializer):
    class Meta:
        model = Spymaster
        fields = '__all__'

    def validate(self, attrs):
        game, team = attrs['game'], attrs['team']
        if Spymaster.objects.filter(game_id=game.id, team=team).exists():
            raise serializers.ValidationError(_('This team already has spymaster'))
        return attrs


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
    creator = serializers.SerializerMethodField()
    field_operatives = serializers.SerializerMethodField()
    spymasters = serializers.SerializerMethodField()
    game_cards = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'creator', 'field_operatives', 'spymasters', 'game_cards')

    @staticmethod
    def get_field_operatives(obj: Game):
        return FieldOperativeSerializer(obj.fieldoperative, many=True).data

    @staticmethod
    def get_spymasters(obj: Game):
        return SpymasterSerializer(obj.spymaster, many=True).data

    @staticmethod
    def get_creator(obj: Game):
        return obj.creator.username

    def get_game_cards(self, obj: Game):
        user = self.context['request'].user
        if obj.spymaster.filter(player_id=user.id).exists() or obj.status == GameStatus.FINISHED:
            return SpyMasterGameCardSerializer(obj.game_cards, many=True).data
        else:
            return FieldOperativeGameCardSerializer(obj.game_cards, many=True).data


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
