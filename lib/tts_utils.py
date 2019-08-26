import json
import traceback
from pathlib import Path
from typing import List, Generator

from google.cloud import texttospeech

from lib.logging import get_module_logger

logger = get_module_logger(__name__)


def collect_input_files(input_directory_path: Path) -> Generator[Path, None, None]:
    """
    Grab every file inside the input directory.

    :param input_directory_path: Full path to the input directory.
    :return: List of full path of every file inside the input folder.
    """
    return input_directory_path.glob('**/*')


def text_to_mp3(client: texttospeech.TextToSpeechClient,
                voice: texttospeech.types.VoiceSelectionParams,
                audio_config: texttospeech.types.AudioConfig,
                text: str,
                output_file_path: Path) -> None:
    """
    Convert a string into voice and save it in an .mp3 file.

    :param client: TextToSpeechClient instance.
    :param voice: VoiceSelectionParams instance.
    :param audio_config: AudioConfig instance.
    :param text: String to synthesise.
    :param output_file_path: Full path to the output .mp3 file.
    :return: None
    """
    lines = text.splitlines()

    logger.info(f'Synthesising {len(lines)} lines ...')

    output_file_log = output_file_path.parent / (output_file_path.stem + '_log.json')

    with output_file_path.open(mode='wb') as output_file:
        for (i, text_chunk) in enumerate(lines):
            # skip empty lines
            if len(text_chunk) > 0:
                input_text = texttospeech.types.SynthesisInput(text=text_chunk)
                try:
                    logger.info(f'Synthesising speech for chunk `{i}`, size: `{len(text_chunk)}`')
                    response = client.synthesize_speech(input_text, voice, audio_config)
                except Exception as e:
                    # If a line could not be synthesised properly, return it along with the error message
                    # It is possible that textract could not extract the text properly.
                    logger.error(f'Speech synthesising failed! Chunk text: `{input_text}`\nError: {e}\n')
                    _error_log = {
                        'chunk_number': i,
                        'chunk_length': len(text_chunk),
                        'chunk_text': str(text_chunk),
                        'Error message': traceback.format_exc()
                    }
                    with open(f'{output_file_log}', 'w') as log_out:
                        json.dump(_error_log, log_out)
                    continue
                output_file.write(response.audio_content)
                logger.info(f'Audio content written to `{output_file_path}`!')

        logger.info(f'Output saved to `{output_file_path}`')
        logger.info(f'logs at `{output_file_log}`')


def list_voices(client) -> List[str]:
    """
    Lists the available voices.
    """

    return [voice.name for voice in client.list_voices().voices]
