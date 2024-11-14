from modules.text_to_speech.offline.windows_tts import WindowsTTS
from utils.file_io import join_normalized_path


if __name__ == '__main__':
    example_responses_path = join_normalized_path('scripts', 'example-data', 'response.txt')
    with open(example_responses_path, 'r') as fp:
        response_text = fp.read()

    tts_voice = WindowsTTS(
        voice_idx=0,
        rate=1.50,
        volume=1.00
    )

    tts_voice.speak(response_text)
