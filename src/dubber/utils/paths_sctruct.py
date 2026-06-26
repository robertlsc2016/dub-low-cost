from pathlib import Path

async def paths_struct():
    print("=== INICIANDO A CRIACAO E CHECAGEM DE ESTRUTURA DE PASTAS")
    paths = [
    "src/dubber/files/audios",
    "src/dubber/files/piper/models",
    # "files/transcriptions",
    "src/dubber/files/videos",
    "src/dubber/files/output"
]
    
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    # Path(f"src/dubber/files/output/{now}").mkdir(parents=True, exist_ok=True)

    print("Estrutura de pastas criada/verificada com sucesso.")