# Generated by Django 3.2 on 2021-05-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210525_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_winner',
            field=models.IntegerField(default=0),
        ),
    ]
