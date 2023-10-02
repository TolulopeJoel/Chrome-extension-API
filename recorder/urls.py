from django.urls import path

from .views import VideoSessionView, VideoDataView, StopVideoView, VideoDetailView

urlpatterns = [
    # Start a new video recording session
    path('session/', VideoSessionView.as_view(), name='video-session'),

    # Upload video data for a session
    path('session/<str:session_id>/upload/', VideoDataView.as_view(), name='send-video-data'),
    
    # Stop uploading video data for a session
    path('session/<str:session_id>/stop/', StopVideoView.as_view(), name='stop-video'),

    path('session/<str:session_id>/', VideoDetailView.as_view(), name='video-detail'),
]
