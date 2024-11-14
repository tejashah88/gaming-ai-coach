import glob
import io

import numpy as np
import torch
from TTS.api import TTS
import soundfile as sf
from sounddevice import OutputStream

from modules.text_to_speech.base.base_tts import BaseTTS
from utils.audio_proc import time_stretch


class CoquiTTS(BaseTTS):
    def __init__(
        self,
        voice_samples_path: str,
        model_name: str = 'tts_models/multilingual/multi-dataset/xtts_v2',
        rate: float = 1.0
    ):
        self.voice_samples = glob.glob(voice_samples_path)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.speech_rate = rate

        self.engine = TTS(
            model_name=model_name,
            progress_bar=True,
        ).to(device=self.device)


    def speak(self, text: str):
        # NOTE: The return type for this function is misleading as it returns a list of float32
        audio_bytes_list = self.engine.tts(
            text=text,
            speaker_wav=self.voice_samples, # type: ignore
            language='en',
            split_sentences=True,
        )

        sample_rate = int(self.engine.synthesizer.output_sample_rate) # type: ignore

        # NOTE: We only stretch/shrink the audio if it's more than a 1% difference
        if abs(self.speech_rate - 1.0) > 0.01:
            audio_buffer = np.array(audio_bytes_list, dtype=np.float32)
            tmp_wav_buffer = io.BytesIO()

            sf.write(file=tmp_wav_buffer, data=audio_buffer, samplerate=sample_rate, format='wav')

            tmp_wav_buffer.seek(0)
            processed_audio_bytes = time_stretch(file=tmp_wav_buffer, rate=self.speech_rate)
            buffer_dtype = np.int16
        else:
            processed_audio_bytes = audio_bytes_list
            buffer_dtype = np.float32


        with OutputStream(samplerate=sample_rate, channels=1, dtype=buffer_dtype) as stream:
            for chunk in processed_audio_bytes:
                stream.write(chunk)

    def cleanup(self):
        pass
