import os
import json
import asyncio
import subprocess
import time

import edge_tts
from pydub import AudioSegment
from typing import Literal



os.makedirs("src/files/audios", exist_ok=True)


# -----------------------------
# 1. GERAR ÁUDIO (EDGE-TTS)
# -----------------------------
async def gerar_audio_unico(job, segmentos):
    """
    Gera um único áudio utilizando Edge-TTS.
    """

    texto = "\n".join(
        seg["translated_text"].strip()
        for seg in segmentos
        if seg["translated_text"].strip()
    )

    arquivo_saida = f"src/files/audios/full_dub_audio-{job}.mp3"

    communicate = edge_tts.Communicate(
        text=texto,
        voice="pt-BR-AntonioNeural"
    )

    await communicate.save(arquivo_saida)

    return arquivo_saida


# -----------------------------
# 2. MONTAR ÁUDIO FINAL
# -----------------------------
async def montar_audio(now, job, audio_path):
    """
    Converte o MP3 gerado pelo Edge-TTS para WAV.
    """

    audio = AudioSegment.from_file(audio_path)

    output_audio = f"src/files/output/{now}/full_dub_audio-{job}.wav"

    audio.export(
        output_audio,
        format="wav"
    )

    return output_audio


# -----------------------------
# 3. GERAR VÍDEO FINAL
# -----------------------------
async def gerar_video_final(job, now):
    VIDEO_ORIGINAL = f"src/files/videos/video-{job}.mp4"

    comando = [
        "ffmpeg",
        "-y",
        "-i", VIDEO_ORIGINAL,
        "-i", f"src/files/output/{now}/full_dub_audio-{job}.wav",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-shortest",
        f"src/files/output/{now}/full_video_dub-{job}.mp4"
    ]

    subprocess.run(
        comando,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# -----------------------------
# 4. PIPELINE PRINCIPAL
# -----------------------------
async def dub_video_egde(
    now,
    job,
    model_name: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "base"
):
    start = time.time()

    print("=== INICIANDO PROCESSO DE DUBLAGEM ===")

    json_path = f"src/files/output/{now}/transcrition_{model_name}.json"

    with open(json_path, "r", encoding="utf-8") as f:
        segmentos = json.load(f)

    print("Gerando áudio com Edge-TTS...")
    audio_path = await gerar_audio_unico(job, segmentos)


    print("Montando áudio final...")
    await montar_audio(now, job, audio_path)

    print("Gerando vídeo...")
    await gerar_video_final(job, now)

    end = time.time()

    print(f"Dublagem finalizada | [{end - start:.4f}s]")
