from django.core.files.uploadhandler import MemoryFileUploadHandler, StopFutureHandlers, StopUpload, SkipFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.conf import settings
import uuid
import pathlib


class SkipUploadTooLargeFileError(SkipFile):
    """
    Класс исключения для пропуска загрузки недопустимо больших загружаемых файлов
    """


class StopUploadTooLargeFileError(StopUpload):
    """
    Класс исключения для остановки загрузки недопустимо больших загружаемых файлов
    """


class LimitedTemporaryFileUploadHandler(MemoryFileUploadHandler):

    def __init__(self, request=None):
        super().__init__(request)
        self.current_size_data = 0
        self.current_size_file = 0
        self.activated = None
        self.file = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.activated = self.check_size_data(content_length)

    @staticmethod
    def check_size_data(size):
        return size <= settings.DATA_UPLOAD_MAX_MEMORY_SIZE

    @staticmethod
    def check_size_file(size):
        return size <= settings.FILE_UPLOAD_MAX_MEMORY_SIZE

    def new_file(self, *args, **kwargs):
        super().new_file(*args, **kwargs)
        self.file = BytesIO()
        if self.activated:
            raise StopFutureHandlers()
        else:
            raise StopUploadTooLargeFileError()

    def receive_data_chunk(self, raw_data, start):
        """Add the data to the BytesIO file."""
        length = len(raw_data)
        if not self.check_size_file(self.current_size_file + length):
            self.current_size_file = 0
            raise SkipUploadTooLargeFileError()
        elif not self.check_size_data(self.current_size_data + length):
            self.current_size_data = 0
            raise StopUploadTooLargeFileError()
        else:
            self.current_size_data += length
            self.current_size_file += length
            self.file.write(raw_data)

    def upload_interrupted(self):
        self.current_size_file = 0
        self.current_size_data = 0

        if hasattr(self.file, "close"):
            self.file.close()

    def file_complete(self, file_size):
        """Return a file object if this handler is activated."""
        if not self.activated:
            return

        self.file.seek(0)
        self.current_size_file = 0
        suffix = pathlib.PurePath(self.file_name).suffix
        return InMemoryUploadedFile(
            file=self.file,
            field_name=self.field_name,
            name=''.join((uuid.uuid4().hex, suffix)),
            content_type=self.content_type,
            size=file_size,
            charset=self.charset,
            content_type_extra=self.content_type_extra,
        )
