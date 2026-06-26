import subprocess
import os

video_path = "src/files/videos/video.mp4"
audio_path = "src/files/audios/full_audio.wav"

async def extract_audio():
    print("EXTRAINDO AUDIO...")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            audio_path
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        # creationflags=subprocess.CREATE_NO_WINDOW  # 👈 importante no Windows
    )