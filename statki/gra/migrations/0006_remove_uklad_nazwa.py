# Generated by Django 5.1.2 on 2024-12-25 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0005_alter_uklad_nazwa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uklad',
            name='nazwa',
        ),
    ]
