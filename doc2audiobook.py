import textract
from google.cloud import texttospeech

from lib.tts_utils import list_voices, text_to_mp3

client = texttospeech.TextToSpeechClient()

available_voices = list_voices(client=client)

print(available_voices)

# use_voice = input('Which voice to use?')
use_voice = 'en-US-Wavenet-F'
use_language = '-'.join(use_voice.split('-')[0:2])

print(f'Using voice {use_voice} in language {use_language}')

voice = texttospeech.types.VoiceSelectionParams(language_code=use_language, name=use_voice)
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

input_path = '/data/bgnet_A4.pdf'
text_to_translate = textract.process(input_path)

text_to_mp3(
    client=client,
    voice=voice,
    audio_config=audio_config,
    text=text_to_translate,
    file_dest='/data/out.mp3'
)
