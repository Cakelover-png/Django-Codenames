# Generated by Django 3.2 on 2022-01-29 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_turn',
            field=models.IntegerField(blank=True, choices=[(0, 'Red'), (1, 'Blue')], null=True, verbose_name='Last Turn'),
        ),
    ]