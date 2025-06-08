from RAUSHAN import *
from pyrogram import *
import speech_recognition as sr
from subprocess import getoutput as r
import time
from pyrogram import enums
import os
from pydub import AudioSegment

@RAUSHAN.on_message(filters.command('vtt', prefixes=HANDLER) & filters.user('me'))
async def voice_to_text(_, message):
    if not message.reply_to_message:
        return await message.reply('Please reply to an audio file to convert')
    
    os.makedirs("voice_convert", exist_ok=True)
    
    if message.reply_to_message.media == enums.MessageMediaType.VOICE:
        await message.reply_to_message.download(file_name="voice_convert/output.ogg")
    elif message.reply_to_message.audio:
        await message.reply_to_message.download(file_name="voice_convert/output.ogg")
    elif message.reply_to_message.document.file_name.endswith(('.mp3', '.oga', '.wav', '.m4a')):
        await message.reply_to_message.download(file_name="voice_convert/output.ogg")
    else:
        return await message.reply("Please reply to a valid audio file!")
    
    edit_message = await message.reply("Converting audio to text...")
    
    audio_file = "voice_convert/output.ogg"
    
    try:
        audio = AudioSegment.from_file(audio_file)
        audio.export("voice_convert/output.wav", format="wav")
        audio_file = "voice_convert/output.wav"
    except Exception as e:
        await edit_message.edit(f"Error converting file: {e}")
        return
    
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    
    retries = 3
    delay = 1
    for attempt in range(retries):
        try:
            text = recognizer.recognize_google(audio_data)
            await edit_message.edit(f"```Text output\nOutput:\n{text}```")
            break
        except sr.UnknownValueError:
            await edit_message.edit("I cannot understand the audio!")
            break
        except sr.RequestError as e:
            if attempt < retries - 1:
                await edit_message.edit(f"Error: {e}. Retrying, remaining {retries - attempt - 1} attempts...")
                time.sleep(delay)
            else:
                await message.reply(f"Failed to connect to Google Speech Recognition service after {retries} attempts.")
    
    await r("rm -rf voice_convert")
