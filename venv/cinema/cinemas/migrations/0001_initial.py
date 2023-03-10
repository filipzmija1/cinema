# Generated by Django 4.1.5 on 2023-02-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScreeningRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255, unique=True)),
                ('places', models.IntegerField()),
                ('projector_availability', models.BooleanField()),
            ],
        ),
    ]
