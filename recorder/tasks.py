import os
import shutil
import struct

import assemblyai as aai
from environs import Env
from moviepy.editor import VideoFileClip

env = Env()
env.read_env()


def append_video_chunk(session_id, video_chunk):
    # Ensure the session directory exists
    session_dir = os.path.join('recorded_videos', session_id)
    os.makedirs(session_dir, exist_ok=True)

    # Move the video_chunk to the session directory
    chunk_destination = os.path.join(
        session_dir, os.path.basename(video_chunk)
    )
    shutil.move(video_chunk, chunk_destination)


def join_blob_chunks(session_id):
    """
    Combine binary data chunks into a single output file.

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


def convert_video_to_audio(session_id, video_path):
    # Ensure the session directory exists
    session_dir = os.path.join('recorded_videos', session_id)
    os.makedirs(session_dir, exist_ok=True)

    video = VideoFileClip(video_path)
    audio = video.audio

    audio_path = os.path.join(f'{session_dir}/audio', 'record-audio.mp3')
    audio.write_audiofile(audio_path, codec='mp3')

    return audio_path


def transcribe_video(video_audio):
    aai.settings.api_key = env.str(f"AAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(video_audio)

    return transcript
