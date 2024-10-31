import json
import os
from typing import Iterable
from magika import Magika
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import tempfile
from django.core.exceptions import ValidationError
from pathlib import Path

DEFAULT_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]

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
    message = _("Allowed file types: %(allowed_extensions)s")
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

        # MIME türlerini JSON dosyasından yükleme
        with open('form\data\mime_types.json', 'r') as file:
            self.mime_type_mapping = json.load(file)

    def __call__(self, file):
        if hasattr(file, 'read'):
            content = file.read()
            if hasattr(file, 'seek'):
                file.seek(0)
        elif isinstance(file, (str, bytes)):
            content = file
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
        file_extension = file.name.split('.')[-1].lower()
        file_mime_type = self.mime_type_mapping.get(file_extension, None)
        print('yaml: ', file_mime_type)
        # file_mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        # exact_mime_type = "application/pdf"
        # exact_extension = "pdf"
        
        result = self.magika.identify_bytes(content)
        print('output: ', result.output)
        exact_mime_type = result.output.mime_type
        exact_extension = result.output.ct_label
        # Check if the MIME type matches the expected type and the extension is allowed
        if exact_mime_type != file_mime_type:
            raise ValidationError(
                'Dosya içeriği uzantı ile uyumlu değil' % {'allowed_extensions': ', '.join(self.allowed_extensions)},
                code=self.code,
            )  
        elif exact_extension not in self.allowed_extensions:
            raise ValidationError(
                self.message % {'allowed_extensions': ', '.join(self.allowed_extensions)},
                code=self.code,
            )
        
        # # 1. Dosya boyutu sınırlandırması
        # if file.size > self.max_size:
        #     raise ValueError(self.size_message % {'max_size': self.max_size})

        # # 2. Dosya uzantısı kontrolü
        # ext = os.path.splitext(file.name)[1][1:].lower()
        # if ext not in self.allowed_extensions:
        #     raise ValueError(self.message % {'allowed_extensions': ', '.join(self.allowed_extensions)})

        # # 3. Dosya türü kontrolü - geçici dosya ile
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     for chunk in file.chunks():
        #         temp_file.write(chunk)
        #     temp_file.flush()  # Geçici dosyayı hemen yaz
        #     file_path = temp_file.name

        # # 4. MIME türünü belirle
        # result = self.magika.identify_path(Path(file_path))
        # # content_type_label = result.output.ct_label # Örneğin xlsx, pdf veya txt
        # mime_type = result.output.mime_type
        # os.remove(file_path)  # Geçici dosyayı silme

        # # MIME türü ile uzantı kontrolü
        # valid_extensions = []
        # for mime, exts in self.mime_type_mapping.items():
        #     print(f"Kontrol edilen MIME: {mime}, Uzantılar: {exts}")  # Kontrol yazdır
        #     if mime == mime_type:
        #         valid_extensions.extend(exts)  # Eşleşen uzantıları ekle
        # print('extensions: ', valid_extensions)

        # if ext not in valid_extensions:
        #     raise ValueError(f"Geçersiz dosya türü: {mime_type}. İzin verilen türler: {', '.join(self.allowed_extensions)}")
        # return file
