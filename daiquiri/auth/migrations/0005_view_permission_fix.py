# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 17:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_auth', '0004_view_permission_typo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('user',), 'permissions': (('view_profile', 'Can view Profile'),), 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]
