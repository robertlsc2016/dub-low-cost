from pathlib import Path




def paths_struct(now):
    print("=== INICIANDO A CRIACAO E CHECAGEM DE ESTRUTURA DE PASTAS")
    paths = [
    "src/files/audios",
    "src/files/piper/models",
    # "files/transcriptions",
    "src/files/videos",
    "src/files/output"
]
    
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    Path(f"src/files/output/{now}").mkdir(parents=True, exist_ok=True)

    print("Estrutura de pastas criada/verificada com sucesso.")