from src.dubber.utils.extract_audio import extract_audio
from src.dubber.utils.paths_sctruct import paths_struct
from src.dubber.utils.clean_audios import clean_audios

from src.dubber.services.dubbers.piper_duber import dub_video;
from src.dubber.services.dubbers.edge_tts_duber import dub_video_egde
from src.dubber.services.transcribers.faster_whisper import transcribe
from src.dubber.services.transcribers.whisper import transcribe_whisper

from typing import Literal
from datetime import datetime
import time
from pathlib import Path


async def dub(
    job,
    model: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "tiny"
):
    start = time.time()

    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    model_name_whisper = model  # 👈 usa o que veio da API

    await extract_audio(job)

    Path(f"src/files/output/{now}").mkdir(parents=True, exist_ok=True)

    await transcribe(now, job, model_name_whisper)

    await dub_video_egde(now, job, model_name_whisper)

    clean_audios()

    end = time.time()
    print(
        f"Tempo total: {end - start:.4f} segundos - transcricao com modelo: {model_name_whisper}"
    )

    return {
        "video_path": f"files/{now}/full_video_dub-{job}.mp4",
        "audio_path": f"files/{now}/full_dub_audio-{job}.wav",
        "transcrition_path": f"files/{now}/transcrition_{model}.json"
    }