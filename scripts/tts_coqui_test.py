from modules.text_to_speech.offline.coqui_ai_tts import CoquiTTS
from utils.file_io import join_normalized_path


if __name__ == '__main__':
    example_responses_path = join_normalized_path('scripts', 'example-data', 'response.txt')
    with open(example_responses_path, 'r') as fp:
        response_text = fp.read()

    tts = CoquiTTS(
        voice_samples_path='scripts/example-data/squidward.wav',
        rate=1.25,
    )

    tts.speak(response_text)
