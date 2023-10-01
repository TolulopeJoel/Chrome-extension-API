import os
import uuid

from django_q.tasks import async_task
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import append_video_chunk


class VideoSessionView(APIView):
    """
    View for returning a session ID
    Start a new video recording session.
    Generates a unique session ID using UUID and creates a directory to store session files.
    """

    def post(self, request, format=None):
        # Start a new video recording session
        session_id = str(uuid.uuid4())
        # Create a directory to store session files
        session_dir = os.path.join('recorded_videos', session_id)
        os.makedirs(session_dir, exist_ok=True)

        return Response({'session_id': session_id}, status=status.HTTP_201_CREATED)


class VideoDataView(APIView):
    """
    View to stream blob data
    Save received video data chunk to a session directory.
    And responds with a success message or an error if no data is received.
    """

    def post(self, request, session_id, format=None):
        # Ensure the session directory exists
        session_dir = os.path.join('recorded_videos', session_id)
        os.makedirs(session_dir, exist_ok=True)

        # Save the received video data chunk to a file
        video_chunk = request.data.get('video_chunk')
        video_chunk = video_chunk.read()

        # Append the video chunk to video file
        if video_chunk:
            async_task(append_video_chunk, session_id, video_chunk)

            return Response({'message': 'Video data chunk saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No video data received'}, status=status.HTTP_400_BAD_REQUEST)
