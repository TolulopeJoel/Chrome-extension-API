import os
import struct

import assemblyai as aai
from environs import Env

from .models import Video

env = Env()
env.read_env()


def append_video_chunk(session_id, video_chunk):
    """
    Add blobs returned from the frontend to a folder
    """
    # Ensure the session directory exists
    session_dir = os.path.join('recorded_videos', session_id)
    os.makedirs(session_dir, exist_ok=True)

    file_name = f"{session_id}_chunk_{len(os.listdir(session_dir))}.blob"
    file_path = os.path.join(session_dir, file_name)

    # Write the video data chunk to the file
    with open(file_path, 'wb') as video_file:
        video_file.write(video_chunk)
    
    # save path to database
    video = Video.objects.get(session_id=session_id)
    video.video_path = file_path
    video.save()


def join_video_chunks(session_id):
    """
    Combine binary data chunks in folder to a single output video file.

    Each binary chunk file is expected to have a 4-byte header specifying the size of the data chunk
    that follows. The function reads this header, extracts the binary data chunk, and appends it to
    the output file until all chunks are processed.
    """
    input_dir = f'recorded_videos/{session_id}'
    blob_files = [file for file in os.listdir(input_dir)]

    with open(f'recorded_videos/{session_id}/final_video.mp4', 'wb') as mp4_file:
        for blob_file in blob_files:
            blob_path = os.path.join(input_dir, blob_file)
            with open(blob_path, 'rb') as chunk_blob:
                chunk_size = struct.unpack('I', chunk_blob.read(4))[0]
                chunk_data = chunk_blob.read(chunk_size)
                mp4_file.write(chunk_data)


def transcribe_video(session_id, video_audio):
    aai.settings.api_key = env.str(f"AAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_audio)

    video = Video.objects.get(session_id=session_id)

    while True:
        if transcript.status == "completed":
            video.is_completed = True
            video.transcription = transcript.text
            video.save()
            return "completed"
        elif transcript.status == "processing" or transcript.status == "queued":
            video.is_completed = False
            video.transcription = "processing..."
            video.save()
            continue
        else:
            video.is_completed = False
            video.transcription = "No transcript available"
            video.save()
            return "failed"
