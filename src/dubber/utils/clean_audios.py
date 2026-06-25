import shutil
from pathlib import Path

def clean_audios():
    print("=== apagando pasta audios para limpeza")
    p = Path("src/dubber/files/audios")

    if p.exists():
        shutil.rmtree(p)  # apaga tudo

    p.mkdir(parents=True, exist_ok=True)  # recria