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


async def dub():
    start = time.time()

    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    model_name_whisper: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "tiny"
    await extract_audio()

    # await paths_struct(now)
    Path(f"src/files/output/{now}").mkdir(parents=True, exist_ok=True)

    await transcribe(now, model_name_whisper)
    
    # transcribe_whisper(now, model_name_whisper)
    
    # dub_video(now, model_name_whisper)
    await dub_video_egde(now, model_name_whisper)


    clean_audios()

    end = time.time()
    print(f"Tempo total: {end - start:.4f} segundos - transcricao com modelo: {model_name_whisper}")

    
    return {
        "video_path": f"files//{now}/full_video_dub.mp4",
        "audio_path": f"files//{now}/full_dub.wav",
        "transcrition_path": f"files//{now}/transcrition_small.json"
    }


# if __name__ == "__main__":
#     dub()