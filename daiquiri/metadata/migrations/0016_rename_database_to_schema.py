# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-16 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_metadata', '0015_change_doi_to_char'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ('schema__order', 'order'), 'permissions': (('view_table', 'Can view Table'),), 'verbose_name': 'Table', 'verbose_name_plural': 'Tables'},
        ),
        migrations.RenameField(
            model_name='table',
            old_name='database',
            new_name='schema',
        ),
        migrations.AlterField(
            model_name='database',
            name='attribution',
            field=models.TextField(blank=True, help_text='The desired attribution for the schema.', null=True, verbose_name='Attribution'),
        ),
        migrations.AlterField(
            model_name='database',
            name='description',
            field=models.TextField(blank=True, help_text='A brief description of the schema to be displayed in the user interface.', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='database',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups which have access to the schema.', to='auth.Group', verbose_name='Groups'),
        ),
        migrations.AlterField(
            model_name='database',
            name='long_description',
            field=models.TextField(blank=True, help_text='A more extensive description of the schema to be displayed on the public schema page.', null=True, verbose_name='Long description'),
        ),
        migrations.AlterField(
            model_name='database',
            name='name',
            field=models.CharField(help_text='Name of the schema on the database server.', max_length=256, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='database',
            name='title',
            field=models.CharField(blank=True, help_text='Human readable title of the schema.', max_length=256, null=True, verbose_name='Title'),
        ),
    ]
