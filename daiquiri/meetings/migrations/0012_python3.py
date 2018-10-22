# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_meetings', '0011_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='status',
            field=models.CharField(choices=[('ORGANIZER', 'organizer'), ('DISCUSSION_LEADER', 'discussion leader'), ('INVITED', 'invited'), ('REGISTERED', 'registered'), ('ACCEPTED', 'accepted'), ('REJECTED', 'rejected'), ('CANCELED', 'canceled')], help_text='Status of the participant.', max_length=32, verbose_name='Status'),
        ),
    ]
