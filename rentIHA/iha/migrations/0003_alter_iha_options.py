# Generated by Django 5.0.4 on 2024-05-04 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iha', '0002_iha_weight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iha',
            options={'permissions': (('list_ihas', ''), ('list_ihas_data', ''), ('update_iha', ''))},
        ),
    ]
