from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from src.dubber.dub import dub
from src.dubber.utils.paths_sctruct import paths_struct
import secrets;
import traceback
from fastapi.staticfiles import StaticFiles
import time

import shutil

import os
from dotenv import load_dotenv
load_dotenv()

url_ambient = os.getenv("URL_AMBIENT")


paths_struct()

app = FastAPI()

app.mount(
    "/files/",
    StaticFiles(directory="src/files/output"),
    name="files"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # obrigatório quando usa "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_video(
    video: UploadFile = File(...),
    model: str = Form("small")  # default small
):
    paths_struct()

    job = secrets.token_hex(2)
    VIDEO_PATH = f"src/files/videos/video-{job}.mp4"

    try:
        start = time.time()

        print("Modelo recebido:", model)
        print(f"modelo selecionado pelo usuario: {model}")
        print(f"job: {job}")

        with open(VIDEO_PATH, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # return
        # passa model pra sua pipeline
        paths_result = await dub(job, model=model)
        end = time.time()

        return {
            "success": True,
            "model": model,
            "video": f"{url_ambient}/{paths_result['video_path']}",
            "time": end - start
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e)
        }