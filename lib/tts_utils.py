from typing import List
from pathlib import Path

from google.cloud import texttospeech

from lib.logging import get_module_logger

logger = get_module_logger(__name__)


def collect_input_files(input_directory_path: Path):
    """
    Grab every file inside the input directory.

    :param input_directory_path: Full path to the input directory.
    :return:
    """
    return input_directory_path.glob('**/*')


def text_to_mp3(client: texttospeech.TextToSpeechClient,
                voice: texttospeech.types.VoiceSelectionParams,
                audio_config: texttospeech.types.AudioConfig,
                text: str,
                output_file_path: Path) -> None:
    """
    Convert a string into voice and save it in an .mp3 file.

    :param client:
    :param voice:
    :param audio_config:
    :param text:
    :param output_file_path:
    :return:
    """
    lines = text.splitlines()

    logger.info(f'Consuming {len(lines)} lines ...')

    with open(output_file_path, 'wb') as out:
        for (i, text_chunk) in enumerate(lines):
            # skip empty lines
            if len(text_chunk) > 0:
                logger.info(f'Synthesising input for chunk {i}, size: {len(text_chunk)}')
                input_text = texttospeech.types.SynthesisInput(text=text_chunk)
                logger.info(f'Synthesising speech for chunk {i}, size: {len(text_chunk)}')
                response = client.synthesize_speech(input_text, voice, audio_config)
                # this is fine because mp3s can be concatenated naively and still work
                logger.info(f'Writing Audio content to {output_file_path} ...')
                out.write(response.audio_content)
                logger.info(f'Audio content written to {output_file_path}!')


def list_voices(client) -> List[str]:
    """
    Lists the available voices.
    """

    return [voice.name for voice in client.list_voices().voices]
