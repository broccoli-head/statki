# Generated by Django 5.1.2 on 2024-12-27 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0012_rename_ilosc_planszy_gra_kolej_gracza'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gra',
            old_name='kolej_gracza',
            new_name='ilosc_planszy',
        ),
    ]
