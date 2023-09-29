from django.urls import path

from .views import VideoCreateView, VideoRetrieveView

urlpatterns = [
    path('videos/', VideoCreateView.as_view(), name='video-create'),
    path('videos/<int:pk>/', VideoRetrieveView.as_view(), name='video-retrieve'),
]
