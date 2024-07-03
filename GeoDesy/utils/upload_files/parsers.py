from rest_framework.parsers import MultiPartParser, DataAndFiles
from django.conf import settings
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser
from django.http.multipartparser import MultiPartParserError
from rest_framework.exceptions import ParseError
from . import handlers
from main_app.exceptions import BadEnterAPIError


class LimitedMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = (handlers.LimitedTemporaryFileUploadHandler(stream),)
        parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
        data, files = parser.parse()
        return DataAndFiles(data, files)
