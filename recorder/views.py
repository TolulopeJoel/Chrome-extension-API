import tempfile

import assemblyai as aai
import cloudinary
import cloudinary.uploader
from environs import Env
from moviepy.editor import VideoFileClip
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Video
from .serializers import VideoSerializer

env = Env()
env.read_env()

cloudinary.config(
    cloud_name=env.str('CLOUD_NAME'),
    api_key=env.str('CLOUDINARY_API_KEY'),
    api_secret=env.str("CLOUDINARY_API_SECRET"),
)


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

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific video object by its ID, and provide its details including
        transcription if available. If the transcription is missing, generate it
        from the video's audio.
        """
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data

        if serializer_data['transcription'] == None:

            video_path = serializer_data['video_file']

            video = VideoFileClip(video_path)
            video_audio = video.audio

            # Create a temporary in-memory file to store the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio_file:
                video_audio.write_audiofile(temp_audio_file.name)

            cloud_audio = cloudinary.uploader.upload(
                temp_audio_file.name, resource_type='auto'
            )
            object = Video.objects.get(id=serializer_data['id'])
            object.video_audio = cloud_audio['secure_url']
            object.save()

            # transcribe the audio file
            aai.settings.api_key = env.str(f"AAI_API_KEY")
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(object.video_audio)
            object.transcription = transcript.text
            object.save()

        return Response(serializer_data, status=status.HTTP_200_OK)
