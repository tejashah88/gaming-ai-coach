import os

import pyaudio
from elevenlabs.client import ElevenLabs


class ElevenLabsTTS:
    def __init__(self, voice, model='eleven_turbo_v2_5'):
        self.client = ElevenLabs(
            api_key=os.getenv('ELEVEN_API_KEY'),
        )

        self.voice = voice
        self.model = model
        self.output_format = 'pcm_24000'


    def _stream_audio_to_output(self, audio_iterator):
        sample_rate = int(self.output_format.split('_')[1])

        py_audio_inst = pyaudio.PyAudio()
        stream = py_audio_inst.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, output=True)

        for chunk in audio_iterator:
            if chunk:
                stream.write(chunk)

        stream.stop_stream()
        stream.close()
        py_audio_inst.terminate()


    def speak(self, text):
        audio_stream = self.client.generate(
            text=text,
            voice=self.voice,
            model=self.model,
            output_format=self.output_format,
            stream=True
        )

        self._stream_audio_to_output(audio_stream)
