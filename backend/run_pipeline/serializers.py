from rest_framework import serializers
from .models import FileUpload, UploadProcess

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file']

class UploadProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadProcess
        fields = ['process_id', 'description']
