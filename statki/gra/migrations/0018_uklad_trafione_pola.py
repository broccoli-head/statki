# Generated by Django 5.1.2 on 2025-01-04 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0017_alter_uklad_pola'),
    ]

    operations = [
        migrations.AddField(
            model_name='uklad',
            name='trafione_pola',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
