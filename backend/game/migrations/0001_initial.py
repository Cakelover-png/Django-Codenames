# Generated by Django 3.2 on 2022-01-29 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=20, unique=True, verbose_name='Word')),
                ('language', models.IntegerField(choices=[(0, 'Georgian'), (1, 'English'), (2, 'Russian')], verbose_name='Language')),
            ],
            options={
                'verbose_name': 'Card',
                'verbose_name_plural': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Started'), (2, 'Finished')], verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_games', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('players_in_lobby', models.ManyToManyField(related_name='games', to=settings.AUTH_USER_MODEL, verbose_name='Players in lobby')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
            },
        ),
        migrations.CreateModel(
            name='Spymaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.IntegerField(choices=[(0, 'Red'), (1, 'Blue')], verbose_name='Team')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spymaster', to='game.game', verbose_name='Game')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spymaster', to=settings.AUTH_USER_MODEL, verbose_name='Player')),
            ],
            options={
                'verbose_name': 'Spymaster',
                'verbose_name_plural': 'Spymasters',
            },
        ),
        migrations.CreateModel(
            name='GameCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.IntegerField(blank=True, choices=[(0, 'Red'), (1, 'Blue')], null=True, verbose_name='Team')),
                ('is_guessed', models.BooleanField(default=False, verbose_name='Is Guessed')),
                ('is_assassin', models.BooleanField(default=False, verbose_name='Is Assassin')),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_cards', to='game.card', verbose_name='Card')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game_cards', to='game.game', verbose_name='Game')),
            ],
            options={
                'verbose_name': 'Game Card',
                'verbose_name_plural': 'Game Cards',
            },
        ),
        migrations.CreateModel(
            name='FieldOperative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.IntegerField(choices=[(0, 'Red'), (1, 'Blue')], verbose_name='Team')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fieldoperative', to='game.game', verbose_name='Game')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fieldoperative', to=settings.AUTH_USER_MODEL, verbose_name='Player')),
            ],
            options={
                'verbose_name': 'Field Operative',
                'verbose_name_plural': 'Field Operatives',
            },
        ),
    ]
