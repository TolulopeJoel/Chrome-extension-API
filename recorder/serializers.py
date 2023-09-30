from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model.
    """
    video_file = serializers.FileField()

    class Meta:
        model = Video
        fields = [
            "id",
            "video_file",
            "title",
            "transcription",
            "upload_date",
        ]
