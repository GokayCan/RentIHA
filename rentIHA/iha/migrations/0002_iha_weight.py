# Generated by Django 5.0.4 on 2024-05-03 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iha', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iha',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
