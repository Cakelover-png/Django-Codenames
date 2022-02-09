from django.contrib import admin

from game.models import Game, Spymaster, FieldOperative, GameCard, Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    search_fields = ('word',)
    list_filter = ('language',)
    list_display = ('word', 'language', 'is_active')
    actions = ['set_active', 'set_not_active']

    @admin.action(description='Mark selected stories as active')
    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected stories as not active')
    def set_not_active(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(FieldOperative)
class FieldOperativeAdmin(admin.ModelAdmin):
    list_select_related = ('player', 'game__creator',)
    search_fields = ('player__username', '=game__id')
    list_filter = ('team',)
    list_display = ('player', 'game', 'team')


@admin.register(Spymaster)
class SpymasterAdmin(admin.ModelAdmin):
    list_select_related = ('player', 'game__creator',)
    search_fields = ('player__username', '=game__id')
    list_filter = ('team',)
    list_display = ('player', 'game', 'team')


class GameCardInline(admin.TabularInline):
    model = GameCard
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('card')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_select_related = ('creator',)
    search_fields = ('creator__username', '=id')
    list_filter = ('last_turn', 'status')
    list_display = ('id', 'creator', 'last_turn', 'status', 'created')
    inlines = (GameCardInline,)
