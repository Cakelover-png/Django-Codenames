from django import forms
from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import path

from game.choices import LanguageType
from game.models import Game, Spymaster, FieldOperative, GameCard, Card


class TxtImportForm(forms.Form):
    language = forms.ChoiceField(choices=LanguageType.choices)
    txt_file = forms.FileField()


class CardForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        word = cleaned_data.get('word')

        if Card.objects.filter(word=word).exists():
            raise ValidationError(
                {'word': _('Card with this Word already exists.')})
        return cleaned_data


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    search_fields = ('word',)
    list_filter = ('language',)
    list_display = ('word', 'language', 'is_active')
    actions = ['set_active', 'set_not_active', 'silent_delete']
    change_list_template = "game/cards_changelist.html"
    form = CardForm

    @admin.action(description='Mark selected cards as active')
    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected cards as not active')
    def set_not_active(self, request, queryset):
        queryset.update(is_active=False)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-txt/', self.import_txt),
        ]
        return my_urls + urls

    def import_txt(self, request):
        if request.method == 'POST':
            txt_file = request.FILES['txt_file']
            language = request.POST.get('language')
            card_list = [Card(word=word.decode().splitlines()[0], language=language) for word in
                         set(txt_file)]
            Card.objects.bulk_create(card_list, batch_size=500)
            duplicated_words = list(Card.objects.values_list('word',
                                                             flat=True).alias(id_count=Count('id')
                                                                              ).filter(id_count__gt=1))
            Card.objects.filter(word__in=duplicated_words).delete()
            card_list = [Card(word=word, language=language) for word in
                         duplicated_words]
            Card.objects.bulk_create(card_list, batch_size=500)
            self.message_user(request, 'Your txt file has been imported')
            return redirect("..")
        form = TxtImportForm()
        payload = {'form': form}
        return render(
            request, 'game/txt_form.html', payload
        )

    @admin.action(description='Bulk delete selected cards')
    def silent_delete(self, request, queryset):
        queryset.delete()


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
