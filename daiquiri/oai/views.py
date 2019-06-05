from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site

from rest_framework.views import APIView
from rest_framework.response import Response

from .renderers import OaiRenderer


class OaiView(APIView):

    renderer_classes = (OaiRenderer, )

    def get(self, request):
        return self.get_response(request, request.GET)

    def post(self, request):
        return self.get_response(request, request.POST)

    def get_response(self, request, params):
        # initialize response and errors array
        self.response = None
        self.errors = []

        # validate keys in params
        for key in params:
            if len(params.getlist(key)) > 1:
                if key == 'verb':
                    self.errors.append(('badVerb', 'Found illegal duplicate of verb'))
                else:
                    self.errors.append(('badArgument', 'Found illegal duplicate of argument \'%s\'.' % key))

        verb = params.get('verb')

        if verb is None:
            self.errors.append(('badArgument', 'OAI verb missing'))
        elif verb == 'GetRecord':
            self.get_record(params)
        elif verb == 'Identify':
            self.identify(params)
        elif verb == 'ListIdentifiers':
            self.list_identifiers(params)
        elif verb == 'ListMetadataFormats':
            self.list_metadata_formats(params)
        elif verb == 'ListRecords':
            self.list_records(params)
        elif verb == 'ListSets':
            self.list_sets(params)
        else:
            self.errors.append(('badVerb', 'Illegal OAI verb'))

        return Response({
            'responseDate': datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
            'baseUrl': request.build_absolute_uri(request.path),
            'params': params,
            'errors': self.errors,
            'response': self.response
        })

    def get_record(self, params):
        pass

    def identify(self, params):
        self.response = {
            'repositoryName': Site.objects.get_current(),
            'adminEmails': settings.OAI_ADMIN_EMAILS,
            'earliestDatestamp': None,
        }

    def list_identifiers(self, params):
        if 'metadataPrefix' not in params:
            self.errors.append(('badArgument', 'Verb \'ListIdentifiers\', argument \'metadataPrefix\' required but not supplied.'))
        else:
            return []

    def list_metadata_formats(self, params):
        pass

    def list_records(self, params):
        pass

    def list_sets(self, params):
        pass
