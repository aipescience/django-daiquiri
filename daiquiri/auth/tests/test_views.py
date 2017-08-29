from django.test import TestCase

from test_generator.views import TestListViewMixin


class AuthTestCase(TestCase):

    fixtures = (
        'auth.json',
    )

    users = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('anonymous', None),
    )

    status_map = {
        'list_view': {
            'admin': 200, 'user': 403, 'anonymous': 302
        }
    }


class UsersTests(TestListViewMixin, AuthTestCase):

    url_names = {
        'list_view': 'users'
    }