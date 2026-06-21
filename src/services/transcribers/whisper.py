import whisper
import json
from deep_translator import GoogleTranslator
from typing import Literal


def transcribe_whisper(now, model_name: Literal["tiny", "base", "small", "medium", "large", "turbo"] = "base"):
    print(f"=== INICIANDO PROCESSO DE TRANSCRICAO | whisper | modelo: {model_name}")

    model = whisper.load_model(model_name)

    result = model.transcribe("src/files/videos/video.mp4")

    segments = []

    for segment in result["segments"]:
        original = segment["text"]

        translated = GoogleTranslator(
            source='en',
            target='pt'
        ).translate(original)

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "original_text": original,
            "translated_text": translated
        })

    with open(f"src/files/output/{now}/transcrition_{model_name}.json", "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=4)

        