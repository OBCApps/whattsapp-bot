
import openai
import random
import os
import requests
from moviepy.editor import AudioFileClip
def to_audio_text(audio_file):
    audio_data = audio_file['MediaUrl0']


    transcription=""

    nombre_file=random.randint(1, int(1e9))

    while(1):
        if os.path.exists(str(nombre_file)+".webm")==0: break
        nombre_file=random.randint(1, int(1e9))

    nombre_file=str(nombre_file)+".webm"

    with open(nombre_file, "wb") as buffer: 
        response = requests.get(audio_data)
        buffer.write(response.content)

    clip = AudioFileClip(nombre_file)

    nombre_file_mp3=nombre_file[0:-5]+".mp3"

    clip.write_audiofile(nombre_file_mp3, codec="mp3")

    transcription=transcribe_audio(nombre_file_mp3)

    os.remove(nombre_file)
    os.remove(nombre_file_mp3)

    print(transcription)

    return transcription