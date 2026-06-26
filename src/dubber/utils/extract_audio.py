import subprocess

async def extract_audio(job):
    video_path = f"src/files/videos/video-{job}.mp4"
    audio_path = f"src/files/audios/full_trans_audio-{job}.wav"

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