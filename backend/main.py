from typing import Dict, List, Type, Union
from typing_extensions import TypedDict
from PIL import Image
from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from fastapi.datastructures import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import io
import time

app = FastAPI()

HOST = "http://localhost:8000"

FILES_DIR = HOST + "/files/"


class ImgItemModel(BaseModel):
    name: str
    y1: int
    y2: int


ImgItem = Union[str, ImgItemModel]


def get_file_url(filename: str) -> str:
    return f"{HOST}/files/?filename={filename}"


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_file_path(filename: str):
    return os.path.join("files", filename)


def get_files_list():
    return os.listdir("files")


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/files/")
async def get_img(filename: str):
    # FINISHED: 压缩加速加载！
    return FileResponse(get_file_path(filename))


@app.get("/files/list")
async def get_imgs_lsit():
    return {
        "files": get_files_list()
    }


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), compress: bool = True):
    MAX_WIDTH = 640
    img = Image.open(io.BytesIO(file.file.read()))

    img.save(get_file_path("raw_" + file.filename))
    if compress:
        filename = "medium_" + file.filename
        w, h = img.size
        compress_ratio = 1 if w < MAX_WIDTH else w / MAX_WIDTH
        w = int(w / compress_ratio)
        h = int(h / compress_ratio)
        img = img.resize((w, h))
        img.save(get_file_path("medium_" + file.filename))
    else:
        filename = "raw_" + file.filename
    return {"filename": filename, "url": get_file_url(filename)}


@app.post("/merge_imgs/")
async def create_merged_img(img_items: List[ImgItem]):
    print({"img_items": img_items})
    assert img_items.__len__() > 0
    final_width = 0
    final_height = 0
    imgs = []
    for img_item in img_items:
        # img_item是BaseModel，是类的形式，所以要用属性取值法，不能用字典取值法
        img_name = img_item if isinstance(img_item, str) else img_item.name
        img = Image.open(get_file_path(img_name))
        if not isinstance(img_item, str):
            y1 = img_item.y1
            y2 = img_item.y2
            w, h = img.size
            img = img.crop((0, h / 100 * y1, w, h / 100 * y2))
        if final_width == 0:
            final_width = img.size[0]
        else:
            assert final_width == img.size[0]
        imgs.append({"img": img, "y": final_height})
        final_height += img.size[1]
    final_img = Image.new("RGBA", (final_width, final_height), (250, 250, 250))
    for img_info in imgs:
        final_img.paste(img_info["img"], (0, img_info["y"]))
    final_img_rand_name = f"{time.time()}.png"
    final_img.save(get_file_path(final_img_rand_name))
    return {
        "filename": final_img_rand_name,
        "url": get_file_url(final_img_rand_name)
    }
