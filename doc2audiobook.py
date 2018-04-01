import argparse
from pathlib import Path

import textract
from google.cloud import texttospeech

from lib.logging import get_module_logger
from lib.tts_utils import list_voices, text_to_mp3, collect_input_files

logger = get_module_logger(__name__)


def parse_arguments():
    """
    Parse command line arguments.

    :return:
    """
    parser = argparse.ArgumentParser(description='Synthesise text from various documents into high fidelity speech.')
    parser.add_argument('-list-voices', help='List available voices.', action='store_true')
    parser.add_argument('--voice', type=str, help='Voice to use for synthesis. Use -list-voices to see options.')

    return parser.parse_args()


def process_input_files(input_directory_path: Path,
                        output_directory_path: Path,
                        client: texttospeech.TextToSpeechClient,
                        voice: texttospeech.types.VoiceSelectionParams,
                        audio_config: texttospeech.types.AudioConfig
                        ) -> None:
    """
    Process every file inside `input_directory_path` and save results in `output_directory_path`.

    :param input_directory_path: Full path to the input directory.
    :param output_directory_path: Full path to the output directory.
    :param client: TextToSpeechClient instance.
    :param voice: VoiceSelectionParams instance.
    :param audio_config: AudioConfig instance.
    :return: None
    """
    input_files = collect_input_files(input_directory_path=input_directory_path)

    for input_file in input_files:
        logger.info(f'Processing input file `{input_file}`')
        output_file = output_directory_path / (input_file.stem + '.mp3')
        logger.info(f'Target output file is: `{output_file}`')

        text_to_translate = textract.process(str(input_file))

        text_to_mp3(
            client=client,
            voice=voice,
            audio_config=audio_config,
            text=text_to_translate,
            output_file_path=output_file
        )

        logger.info(f'Processing done for input file `{input_file}`')


def main():
    client = texttospeech.TextToSpeechClient()
    available_voices = list_voices(client=client)

    args = parse_arguments()
    if args.list_voices:
        print(f'Available voices\n{available_voices}\n')
        return

    use_voice = args.voice
    if use_voice not in available_voices:
        exit('Invalid voice! Use -list-voices to see all available options.')

    use_language = '-'.join(use_voice.split('-')[0:2])

    logger.info(f'Using voice `{use_voice}` in language `{use_language}`')

    voice = texttospeech.types.VoiceSelectionParams(language_code=use_language, name=use_voice)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    process_input_files(
        input_directory_path=Path('/data/input'), output_directory_path=Path('/data/output'),
        client=client, voice=voice, audio_config=audio_config
    )

    logger.info('Done!')
    logger.info('Failures have been saved next to their respective output files.')


if __name__ == '__main__':
    main()
