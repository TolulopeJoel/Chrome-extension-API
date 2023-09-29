from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from django.db import models


class Video(models.Model):
    """
    A model to represent video files uploaded.

    This model stores information about uploaded files, the title of the file,
    and the file itself. It uses VideoMediaCloudinaryStorage to handle
    file uploads, making it possible to upload various types of video files.
    """
    title = models.CharField(max_length=100)

    # The choice of ImageField for 'video_file' is random because VideoMediaCloudinaryStorage
    # allows uploading video file types, not just images.
    video_file = models.ImageField(
        upload_to='videos/',
        storage=VideoMediaCloudinaryStorage()
    )
    upload_date = models.DateTimeField(auto_now_add=True)
