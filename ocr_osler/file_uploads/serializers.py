from . models import File_upload
from rest_framework import serializers


class File_uploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File_upload
        fields = ['name','slug','ocrStatusChoice','uploadedFile','uploadedBy']