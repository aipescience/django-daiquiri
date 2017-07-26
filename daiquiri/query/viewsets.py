from sendfile import sendfile

from django.conf import settings
from django.urls import reverse
from django.http import Http404, StreamingHttpResponse

from rest_framework import viewsets, mixins, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.decorators import list_route, detail_route

from daiquiri.core.viewsets import ChoicesViewSet
from daiquiri.core.permissions import HasModelPermission
from daiquiri.core.paginations import ListPagination

from daiquiri.dali.viewsets import SyncJobViewSet, AsyncJobViewSet

from .models import QueryJob, Example
from .serializers import (
    FormSerializer,
    DropdownSerializer,
    QueryJobSerializer,
    QueryJobListSerializer,
    QueryJobRetrieveSerializer,
    QueryJobCreateSerializer,
    QueryJobUpdateSerializer,
    ExampleSerializer,
    UserExampleSerializer,
    SyncQueryJobSerializer,
    AsyncQueryJobSerializer
)

from .permissions import HasPermission
from .utils import get_quota, fetch_user_database_metadata


class StatusViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (HasPermission, )

    def get_queryset(self):
        return []

    def list(self, request):
        return Response([{
            'guest': not request.user.is_authenticated(),
            'queued_jobs': None,
            'size': QueryJob.objects.get_size(request.user),
            'quota': get_quota(request.user)
        }])


class FormViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (HasPermission, )

    serializer_class = FormSerializer

    def get_queryset(self):
        return settings.QUERY['forms']


class DropdownViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (HasPermission, )

    serializer_class = DropdownSerializer

    def get_queryset(self):
        return settings.QUERY['dropdowns']


class QueryJobViewSet(viewsets.ModelViewSet):
    permission_classes = (HasPermission, )

    def get_queryset(self):
        return QueryJob.objects.filter_by_owner(self.request.user).exclude(phase=QueryJob.PHASE_ARCHIVED)

    def get_serializer_class(self):
        if self.action == 'list':
            return QueryJobListSerializer
        elif self.action == 'retrieve' or self.action == 'abort':
            return QueryJobRetrieveSerializer
        elif self.action == 'create':
            return QueryJobCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return QueryJobUpdateSerializer
        else:
            return QueryJobSerializer

    def perform_create(self, serializer):
        job = QueryJob(
            owner=(None if self.request.user.is_anonymous() else self.request.user),
            table_name=serializer.data.get('table_name'),
            query_language=serializer.data.get('query_language'),
            query=serializer.data.get('query'),
            queue=serializer.data.get('queue'),
        )
        job.clean()
        job.save()
        job.run()

        # inject the job id into the serializers data
        serializer._data['id'] = job.id

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.archive()

    @list_route(methods=['get'])
    def tables(self, request):
        return Response(fetch_user_database_metadata(request.user, self.get_queryset()))

    @detail_route(methods=['put'])
    def abort(self, request, pk=None):
        try:
            job = self.get_queryset().get(pk=pk)
            job.abort()

            serializer = QueryJobRetrieveSerializer(instance=job)
            return Response(serializer.data)
        except QueryJob.DoesNotExist:
            raise Http404

    @detail_route(methods=['get', 'put'], url_path='download/(?P<format_key>[A-Za-z0-9\-]+)', url_name='download')
    def download(self, request, pk=None, format_key=None):
        try:
            job = self.get_queryset().get(pk=pk)
        except QueryJob.DoesNotExist:
            raise NotFound

        result, file_name = job.download(self._get_format(format_key))

        if result.successful():
            if self.request.method == 'GET':
                return sendfile(request, file_name, attachment=True)
            else:
                return Response(result.status)

        else:
            if result.status == 'FAILURE':
                return Response(result.status, status=500)
            else:
                return Response(result.status)

    @detail_route(methods=['get'], url_path='stream/(?P<format_key>[A-Za-z0-9\-]+)', url_name='stream')
    def stream(self, request, pk=None, format_key=None):
        try:
            job = self.get_queryset().get(pk=pk)
        except QueryJob.DoesNotExist:
            raise NotFound

        format_config = self._get_format(format_key)
        return StreamingHttpResponse(job.stream(format_config), content_type=format_config['content_type'])

    def _get_format(self, format_key):
        try:
            return [f for f in settings.QUERY['download_formats'] if f['key'] == format_key][0]
        except IndexError:
            raise ValidationError({'format': "Not supported."})


class ExampleViewSet(viewsets.ModelViewSet):
    permission_classes = (HasModelPermission, )
    serializer_class = ExampleSerializer
    pagination_class = ListPagination
    queryset = Example.objects.all()

    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = ('name', 'description', 'query_string')

    @list_route(methods=['get'], permission_classes=(HasPermission, ))
    def user(self, request):
        examples = Example.objects.filter_by_access_level(self.request.user)
        serializer = UserExampleSerializer(examples, many=True)
        return Response(serializer.data)


class QueueViewSet(ChoicesViewSet):
    permission_classes = (HasPermission, )
    queryset = [(item['key'], item['label']) for item in settings.QUERY['queues']]


class QueryLanguageViewSet(ChoicesViewSet):
    permission_classes = (HasPermission, )
    queryset = [('%(key)s-%(version)s' % item, item['label']) for item in settings.QUERY['query_languages']]


class SyncQueryJobViewSet(SyncJobViewSet):

    serializer_class = SyncQueryJobSerializer

    parameter_map = {
        'FORMAT': 'response_format',
        'TABLE_NAME': 'table_name',
        'LANG': 'query_language',
        'QUERY': 'query'
    }

    def get_queryset(self):
        return QueryJob.objects.filter_by_owner(self.request.user).exclude(phase=QueryJob.PHASE_ARCHIVED)


class AsyncQueryJobViewSet(AsyncJobViewSet):

    serializer_class = AsyncQueryJobSerializer

    parameter_map = {
        'FORMAT': 'response_format',
        'TABLE_NAME': 'table_name',
        'LANG': 'query_language',
        'QUEUE': 'queue',
        'QUERY': 'query'
    }

    def get_queryset(self):
        return QueryJob.objects.filter_by_owner(self.request.user).exclude(phase=QueryJob.PHASE_ARCHIVED)
