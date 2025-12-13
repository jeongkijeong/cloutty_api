from typing import Optional

import uvicorn
# import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from src.model import bard
from src.model import chatgpt as chatGpt
from starlette.middleware.cors import CORSMiddleware
import os

app = FastAPI()


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    sentence: Optional[str] = None
    prompt: str
    model: Optional[str] = None


@app.get("/ai/bard")
def bard(prompt: str):
    response = bard.call(prompt)

    return response


@app.post("/ai/bard")
def bard(item: Item):
    prompt = item.prompt
    response = bard.call(prompt)

    return response

# @app.get("/ai/chatgpt")
# def chatgpt(prompt: str, model: Optional[str] = None,):
#     response = chatGpt.call(model, prompt)

#     return response

@app.post("/ai/chatgpt")
def chatgpt(item: Item):
    # print(item)
    prompt = item.prompt

    if not is_image_request(prompt):
        message = generate_answer(item) # 텍스트 처리.
        res_type = 1
    else:
        message = generate_images(item) # 이미지 처리.
        res_type = 2

    response = {'message' : message, 'type' : res_type}

    return response

def is_image_request(text):
    keywords = ["이미지", "그림", "그려줘", "사진", "image", "draw", "illustration"]
    return any(k in text.lower() for k in keywords)


@app.post("/ai/chatgpt/generate_image")
def generate_answer(item: Item):
    prompt = item.prompt
    response = chatGpt.generate_answer('jkj', None, prompt)

    return response


@app.post("/ai/chatgpt/generate_image")
def generate_images(item: Item):
    prompt = item.prompt
    response = chatGpt.generate_images('jkj', None, prompt)

    return response


# @app.post("/ai/chatgpt/generate_image")
# def generate_image(item: Item):
#     prompt = item.prompt
#     # model = item.model
#     response = chatGpt.generate_image('jkj', None, prompt)
#
#     return response


@app.post("/ai/chatgpt/stt")
async def stt(request : Request):
    filename = await chatGpt.upload(request)  # save file.
    response = chatGpt.speech_to_text(filename) # sound to text.
    print(response)

    return response


@app.post("/ai/chatgpt/tts")
def tts():
    response = chatGpt.text_to_speech('안녕하세요 반값습니다.')
    return response

IMAGE_DIR = Path('D:\\source\\workspace_pycharm\\cloutty_api\\images')

@app.get("/images/{image_name}")
async def image(image_name: str):
    image_path = IMAGE_DIR / image_name
    # current_dir = os.getcwd()
    # print(current_dir)
    # print(image_path)

    if image_path.exists():
        return FileResponse(image_path)
    return {"error": "Image not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
