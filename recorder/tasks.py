import os

def append_video_chunk(session_id, video_chunk):
    # Ensure the session directory exists
    session_dir = os.path.join('recorded_videos', session_id)
    os.makedirs(session_dir, exist_ok=True)

    # Save the received video data chunk to a file
    with open(os.path.join(session_dir, 'record.webm'), 'ab') as video_file:
        video_file.write(video_chunk)


def conver_video_to_audio(video):
    pass


def transcribe_video(video_audio):
    pass
