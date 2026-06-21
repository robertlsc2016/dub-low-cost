import os
import json
import subprocess
from pydub import AudioSegment
from typing import Literal

VIDEO_ORIGINAL = "src/files/videos/video.mp4"
JSON_TRANSCRICAO = "src/transcrition_base.json"

os.makedirs("src/files/audios", exist_ok=True)


# -----------------------------
# 1. GERAR ÁUDIOS (PIPER)
# -----------------------------
def gerar_audios(segmentos, model_path="src/files/piper/models/pt_BR-jeff-medium.onnx"):
    for i, seg in enumerate(segmentos):

        texto = seg["translated_text"].strip()

        if not texto:
            continue

        arquivo_saida = f"src/files/audios/{i}.wav"

        subprocess.run(
            [
                "piper",
                "--model", model_path,
                "--output_file", arquivo_saida,
                 texto,
            ],
            check=True
        )


# -----------------------------
# 2. MONTAR ÁUDIO FINAL
# -----------------------------
def montar_audio(now, segmentos):
    duracao_total = int(segmentos[-1]["end"] * 1000)

    audio_final = AudioSegment.silent(duration=duracao_total)

    for i, seg in enumerate(segmentos):

        arquivo_audio = f"src/files/audios/{i}.wav"

        if not os.path.exists(arquivo_audio):
            continue

        fala = AudioSegment.from_wav(arquivo_audio)

        inicio = int(seg["start"] * 1000)

        audio_final = audio_final.overlay(
            fala,
            position=inicio
        )

    audio_final.export(
        f"src/files/output/{now}/full_dub.wav",
        format="wav"
    )


# -----------------------------
# 3. GERAR VÍDEO FINAL
# -----------------------------
def gerar_video_final(now):
    comando = [
        "ffmpeg",
        "-y",
        "-i", VIDEO_ORIGINAL,
        "-i", f"src/files/output/{now}/full_dub.wav",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-shortest",
        f"src/files/output/{now}/full_video_dub.mp4"
    ]

    subprocess.run(comando)


# -----------------------------
# 4. PIPELINE PRINCIPAL
# -----------------------------
def dub_video(now, model_name: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "base"):
    print("=== INICIANDO PROCESSO DE DUBLAGEM")

    JSON_TRANSCRICAO = f"transcrition_{model_name}.json"

    with open(f"src/files/output/{now}/{JSON_TRANSCRICAO}", "r", encoding="utf-8") as f:
        segmentos = json.load(f)

    print("Gerando falas com Piper...")
    gerar_audios(segmentos)

    print("Montando áudio final...")
    montar_audio(now, segmentos)

    print("Gerando vídeo...")
    gerar_video_final(now)

    print("Concluído!")
    print("Arquivo: full_video_dub.mp4")
