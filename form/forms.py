from django import forms
from .models import JobApplication
from magika import Magika
from django.core.exceptions import ValidationError
from .validator import FileUploadValidator


class ApplyModelForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("name", "email", "phone", "position", "cv", "photo")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dosya boyutu ve uzantı sınırlarını belirleyin
        self.pdf_file_validator = FileUploadValidator(
            allowed_extensions=["pdf"],
            max_size=2 * 1024 * 1024,  # 2 MB
        )
        self.photo_file_validator = FileUploadValidator(
            allowed_extensions=["png", "jpg", "jpeg"],
            max_size=2 * 1024 * 1024,  # 2 MB
        )

    def clean_cv(self):
        file = self.cleaned_data.get("cv")
        if file:
            try:
                self.pdf_file_validator(file)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return file

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        if photo:
            try:
                self.photo_file_validator(photo)
            except ValidationError as e:
                raise ValidationError (e.message) 
        return photo
