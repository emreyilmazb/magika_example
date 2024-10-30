from django import forms
from .models import JobApplication
from magika import Magika
from django.core.exceptions import ValidationError
from .validator import FileUploadValidator


class ApplyModelForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("name", "email", "phone", "position", "cv")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dosya boyutu ve uzantı sınırlarını belirleyin
        self.file_validator = FileUploadValidator(
            allowed_extensions=["png", "jpg", "jpeg", "pdf"],
            max_size=2 * 1024 * 1024,  # 2 MB
        )

    def clean_cv(self):
        file = self.cleaned_data.get("cv")
        if file:
            try:
                self.file_validator(file)
            except ValidationError as e:
                raise ValidationError(e.messages)
        return file

    # def clean_photo(self):
    #     photo = self.cleaned_data['photo']

    #     # Magika kullanarak fotoğrafın türünü kontrol et
    #     magika = Magika()
    #     magika.load()
    #     photo_bytes = photo.read()
    #     result = magika.identify_bytes(photo_bytes)

    #     if result.output.label not in ['jpeg', 'png']:
    #         raise forms.ValidationError("Sadece JPEG veya PNG formatında fotoğraf kabul edilir.")
    #     return photo
