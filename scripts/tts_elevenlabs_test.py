from modules.text_to_speech.online.elevenlabs_tts import ElevenLabsTTS
from utils.file_io import join_normalized_path

from dotenv import load_dotenv
load_dotenv('.env')

if __name__ == '__main__':
    example_responses_path = join_normalized_path('scripts', 'example-data', 'response.txt')
    with open(example_responses_path, 'r') as fp:
        response_text = fp.read()

    tts = ElevenLabsTTS(
        voice='squidward-tentacles',
        rate=1.0
    )

    tts.speak(response_text)
