import os
import json
import subprocess
from pydub import AudioSegment
from typing import Literal
import time


VIDEO_ORIGINAL = "src/files/videos/video.mp4"

os.makedirs("src/files/audios", exist_ok=True)


# -----------------------------
# 1. GERAR ÁUDIO (PIPELINE OTIMIZADO)
# -----------------------------
def gerar_audio_unico(segmentos, model_path):
    """
    🚀 OTIMIZAÇÃO PRINCIPAL:
    - elimina subprocess por frase
    - gera um único áudio contínuo
    """

    texto = " ".join(
        seg["translated_text"].strip()
        for seg in segmentos
        if seg["translated_text"].strip()
    )

    arquivo_saida = "src/files/audios/full.wav"

    subprocess.run(
        [
            "piper",
            "--model", model_path,
            "--output_file", arquivo_saida,
            "--texto", texto
        ],
        # input=texto.encode("utf-8"),
        check=True
    )

    return arquivo_saida


# -----------------------------
# 2. MONTAR ÁUDIO FINAL (SIMPLIFICADO)
# -----------------------------
def montar_audio(now, segmentos, audio_path):
    """
    🔥 versão mais leve:
    - usa apenas 1 arquivo de áudio
    - evita N overlays pesados
    """

    audio = AudioSegment.from_wav(audio_path)

    audio.export(
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

    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# -----------------------------
# 4. PIPELINE PRINCIPAL
# -----------------------------
def dub_video(
    now,
    model_name: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "base"
):
    start = time.time()

    print("=== INICIANDO PROCESSO DE DUBLAGEM")

    json_path = f"src/files/output/{now}/transcrition_{model_name}.json"

    with open(json_path, "r", encoding="utf-8") as f:
        segmentos = json.load(f)

    model_path = "src/files/piper/models/pt_BR-jeff-medium.onnx"

    print("Gerando áudio com Piper (modo otimizado)...")
    audio_path = gerar_audio_unico(segmentos, model_path)

    print("Montando áudio final...")
    montar_audio(now, segmentos, audio_path)

    print("Gerando vídeo...")
    gerar_video_final(now)

    end = time.time()

    print(f"Dublagem finalizada | [{end - start:.4f}s]")