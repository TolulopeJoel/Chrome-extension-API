from django.urls import path

from .views import VideoSessionView, VideoDataView, StopVideoView, VideoDetailView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Start a new video recording session
    path('session/', VideoSessionView.as_view(), name='video-session'),

    # Upload video data for a session
    path('session/<str:session_id>/upload/', VideoDataView.as_view(), name='send-video-data'),
    
    # Stop uploading video data for a session
    path('session/<str:session_id>/stop/', StopVideoView.as_view(), name='stop-video'),

    path('session/<str:session_id>/', VideoDetailView.as_view(), name='video-detail'),
    
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path(
        '',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
]
