# api/serializers.py
from rest_framework import serializers
from ..models import JobApplication  # Modeli üst klasörden içe aktarın
from ..validator import FileUploadValidator


class JobApplicationSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(validators=[FileUploadValidator()])

    class Meta:
        model = JobApplication
        fields = ["name", "email", "phone", "position", "cv"]
