# Generated by Django 5.1.2 on 2024-12-25 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0008_remove_gra_nazwa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gra',
            name='liczba_graczy',
        ),
    ]
