from django.db import models


class Video(models.Model):
    """
    A model to represent video files uploaded.

    This model stores information about uploaded files, the title of the file,
    and the file itself. It uses VideoMediaCloudinaryStorage to handle
    file uploads, making it possible to upload various types of video files.
    """
    session_id = models.CharField(max_length=225)
    is_completed = models.BooleanField(default=False)
    video_path = models.CharField(max_length=225, blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)

    upload_date = models.DateTimeField(auto_now_add=True)
