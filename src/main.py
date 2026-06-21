from utils.extract_audio import extract_audio
from utils.paths_sctruct import paths_struct
from utils.clean_audios import clean_audios

from services.dubbers.piper_duber import dub_video;
from services.dubbers.edge_tts_duber import dub_video_egde

from services.transcribers.faster_whisper import transcribe


from services.transcribers.whisper import transcribe_whisper

from typing import Literal
from datetime import datetime
import time


def main():
    start = time.time()

    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    model_name_whisper: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "small"
    extract_audio()

    paths_struct(now)
    transcribe(now, model_name_whisper)
    
    # transcribe_whisper(now, model_name_whisper)
    
    # dub_video(now, model_name_whisper)
    dub_video_egde(now, model_name_whisper)


    clean_audios()

    end = time.time()
    print(f"Tempo total: {end - start:.4f} segundos - transcricao com modelo: {model_name_whisper}")

if __name__ == "__main__":
    main()