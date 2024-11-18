import pyttsx3

from modules.text_to_speech.base.base_tts import BaseTTS


class WindowsTTS(BaseTTS):
    def __init__(
        self,
        voice_idx: int = 0,
        rate: float = 1.0,
        volume: float = 1.00,
    ):
        self.engine = pyttsx3.init()

        # Set TTS voice
        tts_voices = self.engine.getProperty('voices')

        if voice_idx >= 0 and voice_idx < len(tts_voices):
            self.engine.setProperty('voice', tts_voices[voice_idx].id)
        else:
            raise Exception(f'Invalid voice index specified. Number of existing TTS voices is {len(tts_voices)}')

        # Set TTS-specific settings
        self.engine.setProperty('rate', int(rate * 100))
        self.engine.setProperty('volume', volume)


    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()


    def cleanup(self) -> None:
        self.engine.stop()
