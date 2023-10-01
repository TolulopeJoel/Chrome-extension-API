from django.db import models


class Video(models.Model):
    """
    A model to represent video files uploaded.

    This model stores information about uploaded files, the title of the file,
    and the file itself. It uses VideoMediaCloudinaryStorage to handle
    file uploads, making it possible to upload various types of video files.
    """
    title = models.CharField(max_length=100)

    video_file = models.FileField(upload_to='videos/')
    video_audio = models.URLField(blank=True, null=True)
    transcription = models.URLField(blank=True, null=True)

    upload_date = models.DateTimeField(auto_now_add=True)
