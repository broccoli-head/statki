# Generated by Django 5.1.2 on 2024-12-27 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0011_rename_liczba_graczy_gra_ilosc_planszy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gra',
            old_name='ilosc_planszy',
            new_name='kolej_gracza',
        ),
    ]
