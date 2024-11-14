import io
import os

import soundfile as sf
import numpy as np
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs, DEFAULT_VOICE
from sounddevice import OutputStream

from modules.text_to_speech.base.base_tts import BaseTTS
from utils.audio_proc import time_stretch


class ElevenLabsTTS(BaseTTS):
    def __init__(
        self,
        voice: str,
        model: str = 'eleven_turbo_v2_5',
        voice_settings: VoiceSettings | None = None,
        rate: float = 1.0
    ):
        self.voice = voice
        self.model = model
        self.voice_settings = voice_settings if voice_settings is not None else DEFAULT_VOICE.settings
        self.speech_rate = rate
        self.output_format = 'pcm_24000'

        self.engine = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))


    def speak(self, text):
        audio_bytes_iter = self.engine.generate(
            text=text,
            voice=self.voice,
            voice_settings=self.voice_settings,
            model=self.model,
            output_format=self.output_format,
        )

        sample_rate = int(self.output_format.split('_')[1])
        audio_bytes = np.frombuffer(b''.join(audio_bytes_iter), dtype=np.int16)

        # NOTE: We only stretch/shrink the audio if it's more than a 1% difference
        if abs(self.speech_rate - 1.0) > 0.01:
            tmp_wav_buffer = io.BytesIO()
            sf.write(file=tmp_wav_buffer, data=audio_bytes, samplerate=sample_rate, format='wav')

            tmp_wav_buffer.seek(0)
            processed_audio_bytes = time_stretch(file=tmp_wav_buffer, rate=self.speech_rate)
        else:
            processed_audio_bytes = audio_bytes


        with OutputStream(samplerate=sample_rate, channels=1, dtype=np.int16) as stream:
            for chunk in processed_audio_bytes:
                stream.write(chunk)


    def cleanup(self):
        pass
