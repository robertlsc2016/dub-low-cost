from faster_whisper import WhisperModel
import json
from deep_translator import GoogleTranslator
from typing import Literal

audio_path="src/files/audios/full_audio.wav"


def transcribe(
    now,
    model_name: Literal["tiny", "base", "small", "medium", "large"] = "base"
):

    print("=== INICIANDO PROCESSO DE TRANSCRICAO")

    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(audio_path)

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

    print("TRANSCRICAO FINALIZADA")