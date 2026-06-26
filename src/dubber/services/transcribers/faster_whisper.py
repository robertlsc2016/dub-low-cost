from faster_whisper import WhisperModel
import json
from deep_translator import GoogleTranslator
from typing import Literal

import time


async def transcribe(
    now,
    job,
    model_name: Literal["tiny", "base", "small", "medium", "large"] = "base",
):
    audio_path= f"src/files/audios/full_trans_audio-{job}.wav"

    start = time.time()

    print(f"=== INICIANDO PROCESSO DE TRANSCRICAO: faster_whisper | modelo: {model_name}")

    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=True
    )

    translator = GoogleTranslator(source="en", target="pt")

    results = []

    for seg in segments:
        original = seg.text.strip()

        if not original:
            continue

        translated = translator.translate(original)

        results.append({
            "start": seg.start,
            "end": seg.end,
            "original_text": original,
            "translated_text": translated
        })

    with open(
        f"src/files/output/{now}/transcrition_{model_name}.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    end = time.time()

    print(f"TRANSCRICAO FINALIZADA - [{end - start:.4f}s]")