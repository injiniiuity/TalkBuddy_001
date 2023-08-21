import openai
import winsound
from elevenlabslib import *
from pydub import AudioSegment
from pydub.playback import play
import io
from io import BytesIO
import os
import config
import requests
from PIL import Image
import json
from subprocess import call
from elevenlabs import clone, generate, play, set_api_key

openai.api_key = config.OPENAI_API_KEY
api_key = config.ELEVENLABS_API_KEY
from elevenlabslib import ElevenLabsUser
user = ElevenLabsUser(api_key)
set_api_key(api_key)

messages = ["You are an advisor. Please respond to all input in 50 words or less."]

global voice1
voice1 = "Rachel"
image1 = None

#기본 목소리 설정
def adam():
  global voice1
  voice1 = "Adam"

def antoni():
  global voice1
  voice1 = "Antoni"

def rachel():
  global voice1
  voice1 = "Rachel"


#목소리 생성
def clone_voice(userMp3):
  voice = clone(
    name="Voice Name",
    description="An old American male voice with a slight hoarseness in his throat. Perfect for news.",
    files=[userMp3],
    )
  global  voice1
  voice1 = "Voice Name"
  
  
 
        
#이미지 생성
url = "https://stablediffusionapi.com/api/v3/text2img"
def get_image(prompt):
  payload = {
    "key": config.DREAM_BOOTH_KEY,
    "prompt": prompt,
    "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), anime",
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": 0,"safety_checker": "0","enhance_prompt": "yes","guidance_scale": 7.5}
  headers = {}
  response = requests.request("POST", url, headers=headers, data=payload)
  url1 = str(json.loads(response.text)['output'][0])
  r = requests.get(url1)
  i = Image.open(BytesIO(r.content))
  return i

  
    
#음성, 사진 합성
def vd_generate(video, audio):
        #if video is None or audio is None or "wav2lip" is None:
        #    return

        smooth = "--nosmooth" if 0 else ""
        pads = str(0) + " " + str(10) + " " + str(0) + " " + str(0)
        call(["run.cmd", "checkpoints/wav2lip.pth", video, audio, pads, str(2), smooth])
        return "results/result_voice.mp4"

#음성 및 영상 생성
def transcribe(audio):
    global messages

    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append(f"\nUser: {transcript['text']}")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages[-1],
        max_tokens=80,
        n=1,
        stop=None,
        temperature=0.5
    )

    system_message = response["choices"][0]["text"]
    messages.append(f"{system_message}")
    
    voice = user.get_voices_by_name(voice1)[0]
    audio = voice.generate_audio_v2(system_message)

    audio = AudioSegment.from_file(io.BytesIO(audio[0]), format="mp3")
    audio.export("./input/output.wav", format="wav")
    video1 = vd_generate("./input/pic.png","./input/output.wav")
    chat_transcript = "\n".join(messages)
    return (video1, chat_transcript)
  
  

#input 이미지 저장
def image_save(image):
    image1=image
    image1.save('./input/pic.png','png')

  