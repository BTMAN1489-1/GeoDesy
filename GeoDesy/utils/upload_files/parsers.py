from rest_framework.parsers import MultiPartParser, DataAndFiles
from django.conf import settings
from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser
from utils.upload_files.handlers import LimitedTemporaryFileUploadHandler

__all__ = ("LimitedMultiPartParser",)


class LimitedMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        request = parser_context['request']
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        meta = request.META.copy()
        meta['CONTENT_TYPE'] = media_type
        upload_handlers = (LimitedTemporaryFileUploadHandler(stream),)
        parser = DjangoMultiPartParser(meta, stream, upload_handlers, encoding)
        data, files = parser.parse()
        return DataAndFiles(data, files)
