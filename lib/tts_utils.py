import sys

from typing import List
from google.cloud import texttospeech


def text_to_mp3(client, voice, audio_config, text, file_dest):
    lines = text.splitlines()
    with open(file_dest, 'wb') as out:
        for (i, text_chunk) in enumerate(lines):
            # skip empty lines
            if len(text_chunk) > 0:
                input_text = texttospeech.types.SynthesisInput(text=text_chunk)
                response = client.synthesize_speech(input_text, voice, audio_config)
                # this is fine because mp3s can be concatenated naively and still work
                out.write(response.audio_content)
                # print progress
                ticks = min(48, round(i / len(lines) * 48))
                bar = "=" * ticks + "." * (48 - ticks)
                sys.stdout.write("\r" + "[" + bar + "]")
                sys.stdout.flush()
    print()


def list_voices(client) -> List[str]:
    """
    Lists the available voices.
    """

    return [voice.name for voice in client.list_voices().voices]
