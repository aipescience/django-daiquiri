from django.conf.urls import url, include

from rest_framework import routers

from .views import table, files, archive
from .viewsets import RowViewSet, ColumnViewSet

router = routers.DefaultRouter()
router.register(r'rows', RowViewSet, base_name='row')
router.register(r'columns', ColumnViewSet, base_name='column')

urlpatterns = [
    url(r'^table/(?P<database_name>[A-Za-z0-9_]+)/(?P<table_name>[A-Za-z0-9_]+)/$', table, name='table'),
    url(r'^files/(?P<file_path>.+)$', files, name='files'),
    url(r'^archive/(?P<database_name>[A-Za-z0-9_]+)/(?P<table_name>[A-Za-z0-9_]+)/(?P<column_name>[A-Za-z0-9_]+)/$', archive, name='archive'),

    # rest api
    url(r'^api/', include(router.urls)),
]
