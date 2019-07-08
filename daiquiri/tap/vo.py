from django.conf import settings
from django.urls import reverse

from daiquiri.core.constants import ACCESS_LEVEL_PUBLIC
from daiquiri.metadata.models import Schema
from daiquiri.registry.vo import get_curation

from .serializers import SchemaSerializer


def get_resource():
    return {
        'service': 'tap',
        'identifier': 'ivo://%s/tap' % settings.SITE_IDENTIFIER,
        'title': '%s TAP Service' % settings.SITE_TITLE,
        'curation': get_curation(),
        'content': {
            'type': 'Catalog',
            'description': 'The TAP Service registry for %s.' % settings.SITE_IDENTIFIER,
            'referenceURL': settings.SITE_URL.rstrip('/') + reverse('tap:root')
        },
        'capabilities': get_capabilities(),
        'tableset': get_tableset(),
        'type': 'vg:CatalogResource',
        'created': settings.SITE_CREATED,
        'updated': settings.SITE_UPDATED,
    }


def get_availability():
    return {
        'available': 'true',
        'note': 'service is accepting queries'
    }


def get_capabilities():
    return [
        {
            'id': 'ivo://ivoa.net/std/TAP',
            'interface': {
                'type': 'vs:ParamHTTP',
                'role': 'std',
                'access_url': {
                    'use': 'base',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:root')
                }
            },
            'languages': [{
                'name': language['key'],
                'version': language['version'],
                'description': language['description'],
            } for language in settings.QUERY_LANGUAGES]
        },
        {
            'id': 'ivo://ivoa.net/std/TAP#async-1.1',
            'interface': {
                'type': 'vs:ParamHTTP',
                'role': 'std',
                'version': '1.1',
                'access_url': {
                    'use': 'base',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:async-list')
                }
            }
        },
        {
            'id': 'ivo://ivoa.net/std/TAP#sync-1.1',
            'interface': {
                'type': 'vs:ParamHTTP',
                'role': 'std',
                'version': '1.1',
                'access_url': {
                    'use': 'base',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:sync-list')
                }
            }
        },
        {
            'id': 'ivo://ivoa.net/std/VOSI#capabilities',
            'interface': {
                'type': 'vs:ParamHTTP',
                'access_url': {
                    'use': 'full',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:capabilities')
                }
            }
        },
        {
            'id': 'ivo://ivoa.net/std/VOSI#tables',
            'interface': {
                'type': 'vs:ParamHTTP',
                'access_url': {
                    'use': 'full',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:tables')
                }
            }
        },
        {
            'id': 'ivo://ivoa.net/std/DALI#examples',
            'interface': {
                'type': 'vr:WebBrowser',
                'access_url': {
                    'use': 'full',
                    'url': settings.SITE_URL.rstrip('/') + reverse('tap:examples')
                }
            }
        }
    ]


def get_tableset():
    queryset = Schema.objects.filter(metadata_access_level=ACCESS_LEVEL_PUBLIC, published__isnull=False)
    serializer = SchemaSerializer(queryset, many=True)
    return serializer.data