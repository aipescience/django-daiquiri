# Generated by Django 2.1.3 on 2018-11-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daiquiri_files', '0004_django2'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='layout',
            field=models.BooleanField(default=False, help_text='Use the page layout with the content.', verbose_name='Layout'),
            preserve_default=False,
        ),
    ]
