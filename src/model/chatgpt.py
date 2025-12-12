from openai import OpenAI
import httpx
from datetime import datetime
from tinydb import TinyDB, Query
import os
import time
import base64
import uuid

os.environ['OPEN_API_KEY'] = ''

User = Query()
db = TinyDB('gtp.json')

role_user = 'user'
role_assi = 'assistant'

def is_number(val) :
    rev = False

    try:
        if int(val) or float(val):
            rev = True
    except:
        rev = False

    return rev


def insert_history(user_id, data) :
    data['user_id'] = user_id
    db.insert(data)


def call(user_id ,model, sentence, prompt):
    client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'), http_client=httpx.Client(verify=False))

    # client = OpenAI(base_url= 'http://3.39.219.244:9300',
    #                 api_key='no required', http_client=httpx.Client(verify=False))

    # client = OpenAI(base_url= 'http://172.21.68.103:8080',
    #                 api_key='no required', http_client=httpx.Client(verify=False))

    stt = datetime.now()

    if not model:
        model = 'gpt-4o-mini'
        #model = 'gpt-3.5-turbo'

    print('## 문장 ##')
    print(sentence + '\n')

    print('## 질문 ##')
    print(prompt   + '\n')

    message = []
    history = db.search(User.user_id == user_id)

    if len(history) == 0:
        question = {'role': 'system', 'content': 'you are my assistant.'}
        message.append(question)

        insert_history(user_id, question)
    else:
        message = [{'role': item['role'], 'content': item['content']} for item in history]

    question = {'role' : role_user, 'content': prompt}
    message.append(question)

    insert_history(user_id, question)

    response = client.chat.completions.create(
        model = model,
        messages = message[-10:] # 최신 질문을 10개만 전달 합니다.
    )
    # print('answer>> %s' %response)
    content = response.choices[0].message.content

    print('## 답변 ##')
    print(content + '\n')

    end = datetime.now()
    gap = end - stt
    print('시작>> %s'% stt)
    print('완료>> %s'% end)
    print('차이>> %s'% (gap.total_seconds()) + 'ms')

    return content


def speech_to_text(path) :
    text = ''

    client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'), http_client=httpx.Client(verify=False))

    with open(path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model = 'whisper-1',
            file  = audio_file
        )

    # print(transcription.text)
    text = transcription.text
    return text


def text_to_speech(text) :
    client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'), http_client=httpx.Client(verify=False))

    speech = client.audio.speech.create(
        model = 'gpt-4o-mini-tts',  # 초당 생성 빠른 TTS
        voice = 'alloy',  # 사용할 음성
        input = text
    )

    path = 'hello.wav'
    with open(path, 'wb') as f:
        f.write(speech.read())

def generate_image(user_id ,model, prompt) :
    # client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'), http_client=httpx.Client(verify=False))
    #
    # if not model:
    #     model = 'dall-e-3'
    #     # model = 'gpt-image-1'
    #
    # response = client.images.generate(
    #     model  = model,  # 또는 "dall-e-3"
    #     prompt = prompt,
    #     size   = "1024x1024",
    #     response_format="b64_json"
    # )
    #
    # image_base64 = response.data[0].b64_json
    # decode_bytes = base64.b64decode(image_base64)

    # file_id = uuid.uuid4()
    file_id = 'result'
    file_nm = str(file_id) + '.png'

    # with open(file_nm, "wb") as f:
    #     f.write(decode_bytes)

    return file_nm


async def upload(request) :
    body = await request.body()  # <-- raw bytes
    filename = f"{time.time()}.wav"

    # 파일 저장
    with open(filename, "wb") as f:
        f.write(body)

    return filename
