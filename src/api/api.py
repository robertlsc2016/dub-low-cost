from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from src.dubber.dub import dub
import traceback
from fastapi.staticfiles import StaticFiles

import shutil
import os

app = FastAPI()

app.mount(
    "/files",
    StaticFiles(directory="src/dubber/files/output"),
    name="files"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # obrigatório quando usa "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

VIDEO_PATH = "src/dubber/files/videos/video.mp4"

@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    try:
        with open(VIDEO_PATH, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        paths_result = await dub()

        return {
            "success": True,
            # "paths": paths_result[]
            "video": f"http://localhost:8000{paths_result['video_path']}"
        }

    except Exception as e:
        traceback.print_exc()

        return {
            "success": False,
            "error": str(e)
        }
