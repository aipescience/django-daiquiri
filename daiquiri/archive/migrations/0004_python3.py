# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-22 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_archive', '0003_remove_archivejob_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='access_level',
            field=models.CharField(choices=[('PRIVATE', 'Private - access must be granted by group'), ('INTERNAL', 'Internal - logged in users can access'), ('PUBLIC', 'Public - anonymous visitors can access')], max_length=8, verbose_name='Access level'),
        ),
    ]