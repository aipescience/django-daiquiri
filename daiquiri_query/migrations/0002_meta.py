# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 09:11
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_query', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='queryjob',
            managers=[
                ('submission', django.db.models.manager.Manager()),
            ],
        ),
    ]