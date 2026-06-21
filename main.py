from src.services.extract_audio import extract_audio
from src.services.paths_sctruct import paths_struct
from src.services.clean_audios import clean_audios
from src.services.dub import dub_video;
from src.services.transcribe import transcribe

from typing import Literal
from datetime import datetime
import time


def main():
    start = time.time()

    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    model_name_whisper: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "medium"
    extract_audio()

    paths_struct(now)
    transcribe(now, model_name_whisper)

    dub_video(now, model_name_whisper)
    # clean_audios()

    end = time.time()
    print(f"Tempo total: {end - start:.4f} segundos - transcricao com modelo: {model_name_whisper}")

if __name__ == "__main__":
    main()