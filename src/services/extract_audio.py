import subprocess

video_path = "src/files/videos/video.mp4"
audio_path = "src/files/audios/full_audio.wav"


def extract_audio():
    print("EXTRAINDO AUDIO...");

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",  # remove vídeo
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ])