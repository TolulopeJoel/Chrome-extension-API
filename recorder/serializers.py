from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model.
    """
    # Changing the serializer field to FileField to ensure the API can accept video files
    # without encountering errors.
    video_file = serializers.FileField()

    class Meta:
        model = Video
        fields = '__all__'
