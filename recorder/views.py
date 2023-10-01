import os
import uuid

from django_q.tasks import async_task
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import (
    append_video_chunk,
    convert_video_to_audio,
    join_blob_chunks,
    transcribe_video,
)


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
class VideoDataView(APIView):
    """
    View to stream blob data
    Save received video data chunk to a session directory.
    And responds with a success message or an error if no data is received.
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


class StopVideoView(APIView):
    def get(self, request, session_id, format=None):
        video_path = os.path.join('recorded_videos', session_id)

        # join blob chunks
        async_task(join_blob_chunks, session_id)

        video_audio = async_task(
            convert_video_to_audio, session_id, video_path
        )

        async_task(transcribe_video, video_audio)


class VideoDetailView(APIView):
    def get(self, request, session_id, format=None):
        # As usual, check if the session directory exists
        session_dir = os.path.join('recorded_videos', session_id)
        if not os.path.exists(session_dir):
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

        # Define the path to the recorded video file
        video_file_path = os.path.join(session_dir, 'final_video.mp4')

        # Check if the video file exists
        if not os.path.exists(video_file_path):
            return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'session_id': session_id,
            'video': video_file_path,
            'transcription': ''
        }

        return Response(data, status=status.HTTP_200_OK)
