# Generated by Django 5.1.2 on 2025-01-07 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0019_rename_trafione_pola_uklad_trafione_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gra',
            name='uzytkownik',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='gry', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uklad',
            name='gra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uklady', to='gra.gra'),
        ),
    ]
