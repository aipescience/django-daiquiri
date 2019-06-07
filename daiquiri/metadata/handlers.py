from django.apps import apps
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from daiquiri.oai.utils import update_records, delete_records

from .models import Schema, Table, Column


@receiver(post_save, sender=Schema)
def schema_updated_handler(sender, **kwargs):
    if apps.is_installed('daiquiri.oai'):
        update_records(kwargs['instance'])


@receiver(post_delete, sender=Schema)
def schema_deleted_handler(sender, **kwargs):
    if apps.is_installed('daiquiri.oai'):
        delete_records(kwargs['instance'])


@receiver(post_save, sender=Table)
def table_updated_handler(sender, **kwargs):
    if apps.is_installed('daiquiri.oai'):
        update_records(kwargs['instance'])


@receiver(post_delete, sender=Table)
def table_deleted_handler(sender, **kwargs):
    if apps.is_installed('daiquiri.oai'):
        delete_records(kwargs['instance'])


@receiver(post_save, sender=Column)
def column_updated_handler(sender, **kwargs):
    cache.delete('processor')
