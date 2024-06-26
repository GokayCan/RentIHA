# Generated by Django 5.0.4 on 2024-05-04 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iha', '0003_alter_iha_options'),
        ('rent', '0002_alter_rent_rentenddate_alter_rent_rentstartdate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='iha',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rent_iha', to='iha.iha'),
        ),
        migrations.AlterField(
            model_name='rent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rent_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
