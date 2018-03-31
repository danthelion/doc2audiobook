from pathlib import Path

import textract
from google.cloud import texttospeech

from lib.logging import get_module_logger
from lib.tts_utils import list_voices, text_to_mp3

logger = get_module_logger(__name__)

client = texttospeech.TextToSpeechClient()

available_voices = list_voices(client=client)

logger.info(available_voices)

# use_voice = input('Which voice to use?')
use_voice = 'en-US-Wavenet-F'
use_language = '-'.join(use_voice.split('-')[0:2])

logger.info(f'Using voice {use_voice} in language {use_language}')

voice = texttospeech.types.VoiceSelectionParams(language_code=use_language, name=use_voice)
audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

input_path = list(Path('/data/input').glob('**/*'))[0]
logger.info(f'Processing file {input_path}')

text_to_translate = textract.process(input_path)

text_to_mp3(
    client=client,
    voice=voice,
    audio_config=audio_config,
    text=text_to_translate,
    file_dest=f'/data/output/output.mp3'
)
