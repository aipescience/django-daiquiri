import six

from collections import OrderedDict

from django.conf import settings
from django.utils.translation import ugettext as _

from rest_framework.exceptions import ValidationError

from daiquiri.core.utils import filter_by_access_level
from daiquiri.core.adapter import DatabaseAdapter

from .utils import get_user_schema_name, get_default_table_name


def process_schema_name(user, schema_name):
    user_schema_name = get_user_schema_name(user)

    if schema_name:
        if schema_name == user_schema_name:
            return schema_name
        else:
            raise ValidationError({
                'schema_name': [_('Only the user schema is allowed.')]
            })
    else:
        return user_schema_name


def process_table_name(table_name):
    if table_name:
        # the tablename was checked by the TableNameValidator
        return table_name
    else:
        return get_default_table_name()


def process_query_language(user, query_language):
    # get the possible query languages for this user and create a map
    query_language_map = {}
    for item in filter_by_access_level(user, settings.QUERY_LANGUAGES):
        query_language_map['%(key)s-%(version)s' % item] = '%(key)s-%(version)s' % item
        query_language_map['%(key)s' % item] = '%(key)s-%(version)s' % item

    # check if a query language is set
    if query_language:
        query_language = query_language.lower()

        if query_language in query_language_map:
            return query_language_map[query_language]
        else:
            raise ValidationError({
                'query_language': [_('This query language is not supported.')]
            })

    else:
        # return the default query_language
        return settings.QUERY_LANGUAGES[0]['key']


def process_queue(user, queue):
    # get the possible queues for this user
    queues = filter_by_access_level(user, settings.QUERY_QUEUES)

    # check if a queue is set
    if queue:
        queue = queue.lower()

        # check if this queue is in the possible queues
        try:
            six.next((item for item in queues if item['key'] == queue))
        except StopIteration:
            raise ValidationError({
                'queue': [_('This queue is not supported.')]
            })

        return queue
    else:
        # set the default queue
        return queues[0]['key']


def process_response_format(response_format):
    if response_format:
        response_format = response_format.lower()

        if response_format in [item['key'] for item in settings.QUERY_DOWNLOAD_FORMATS]:
            return response_format
        else:
            raise ValidationError({
                'response_format': [_('This response format is not supported.')]
            })
    else:
        # return the default response_format
        return settings.QUERY_DEFAULT_DOWNLOAD_FORMAT


def process_display_columns(processor_display_columns):
    # process display_columns to expand *
    display_columns = []
    for processor_display_column, original_column in processor_display_columns:
        if processor_display_column == '*':
            schema_name, table_name, tmp = original_column
            for column_name in DatabaseAdapter().fetch_column_names(schema_name, table_name):
                display_columns.append((column_name, (schema_name, table_name, column_name)))

        else:
            display_columns.append((processor_display_column, original_column))

    # check for duplicate columns in display_columns
    seen = set()
    errors = []
    for display_column_name, display_column in display_columns:
        if display_column_name not in seen:
            seen.add(display_column_name)
        else:
            errors.append(_('Duplicate column name %(column)s') % {
                'column': display_column_name
            })

    if errors:
        raise ValidationError({
            'query': [error for error in errors]
        })

    return OrderedDict(display_columns)
