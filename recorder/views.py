from rest_framework import generics

from .models import Video
from .serializers import VideoSerializer


class VideoCreateView(generics.CreateAPIView):
    """
    View for creating video objects.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class VideoRetrieveView(generics.RetrieveAPIView):
    """
    View for retrieving a specific video object by its ID.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
