import json
from typing import Iterable

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from magika import Magika

from common.constants import DEFAULT_IMAGE_EXTENSIONS


class FileUploadValidator:
    """
    File Upload Validator that uses the Magika package to validate the uploaded file's MIME type.

    Args:
        allowed_extensions (Iterable): List of allowed file extensions without dots.
        max_size (int): Maximum file size in bytes.
        message (str): Invalid file format exception message.
        size_message (str): Max. file size exceeded exception message.
    """
    default_extensions = DEFAULT_IMAGE_EXTENSIONS
    message = _("Allowed file types: %(allowed_extensions)s.")
    size_message = _("File size cannot exceed %(max_size)s bytes.")
    code = "invalid_extension"
    size_code = "invalid_size"

    def __init__(
            self,
            allowed_extensions: Iterable = None,
            max_size: int = None,
            message: str = None,
            size_message: str = None,
    ):
        self.allowed_extensions = allowed_extensions or self.default_extensions
        self.max_size = max_size or getattr(settings, 'FILE_VALIDATOR_MAX_SIZE', 41_943_040)
        self.message = message or self.message
        self.size_message = size_message or self.size_message
        self.magika = Magika()

        with open('common/data/mime_types.json', 'r') as file:
            self.mime_type_mapping = json.load(file)

    def __call__(self, value):
        if hasattr(value, 'read'):
            content = value.read()
            if hasattr(value, 'seek'):
                value.seek(0)
        elif isinstance(value, (str, bytes)):
            content = value
        else:
            raise ValidationError(_("Invalid file format"))

        # File size validation
        if self.max_size is not None:
            if len(content) > self.max_size:  # Comparison in bytes
                raise ValidationError(
                    self.size_message % {'max_size': self.max_size},
                    code=self.size_code,
                )

        # Uploaded files extension
        file_extension = value.name.split('.')[-1].lower()
        file_mime_type = self.mime_type_mapping.get(file_extension, None)

        # MIME type and extension detection
        result = self.magika.identify_bytes(content)
        exact_mime_type = result.output.mime_type
        exact_extension = result.output.ct_label

        # Check if the MIME type matches the expected type and the extension is allowed
        if exact_mime_type != file_mime_type or exact_extension not in self.allowed_extensions:
            raise ValidationError(
                self.message % {'allowed_extensions': ', '.join(self.allowed_extensions)},
                code=self.code,
            )
