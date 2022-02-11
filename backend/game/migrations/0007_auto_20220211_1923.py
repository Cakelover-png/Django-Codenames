# Generated by Django 3.2 on 2022-02-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_card_word'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='guess_time',
        ),
        migrations.RemoveField(
            model_name='game',
            name='last_turn',
        ),
        migrations.AddField(
            model_name='game',
            name='time_for_last_turn',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time For Last Turn'),
        ),
        migrations.AddField(
            model_name='game',
            name='time_for_turn_change',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Time For Turn Change'),
        ),
        migrations.AddField(
            model_name='game',
            name='turn',
            field=models.IntegerField(blank=True, choices=[(0, 'Red'), (1, 'Blue')], null=True, verbose_name='Current Turn'),
        ),
    ]