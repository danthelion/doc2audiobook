from typing import List

from google.cloud import texttospeech

from lib.logging import get_module_logger

logger = get_module_logger(__name__)


def text_to_mp3(client, voice, audio_config, text, file_dest):
    lines = text.splitlines()
    with open(file_dest, 'wb') as out:
        for (i, text_chunk) in enumerate(lines):
            # skip empty lines
            if len(text_chunk) > 0:
                logger.info(f'Synthesising input for chunk {i}, size: {len(text_chunk)}')
                input_text = texttospeech.types.SynthesisInput(text=text_chunk)
                logger.info(f'Synthesising speech for chunk {i}, size: {len(text_chunk)}')
                response = client.synthesize_speech(input_text, voice, audio_config)
                # this is fine because mp3s can be concatenated naively and still work
                out.write(response.audio_content)
                logger.info(f'Audio content written to file {file_dest}')


def list_voices(client) -> List[str]:
    """
    Lists the available voices.
    """

    return [voice.name for voice in client.list_voices().voices]
