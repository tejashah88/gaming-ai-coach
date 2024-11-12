import pyttsx3

from modules.text_to_speech.base.base_tts import BaseTTS


class WindowsTTS(BaseTTS):
    def __init__(self, voice_idx=0, rate=2.00, volume=1.00):
        self.engine = pyttsx3.init()

        self.set_voice_settings(
            voice_idx=voice_idx,
            rate=rate,
            volume=volume,
        )


    def set_voice_settings(self, voice_idx=0, rate=2.00, volume=1.00):
        # Set TTS voice
        tts_voices = self.engine.getProperty('voices')

        if voice_idx >= 0 and voice_idx < len(tts_voices):
            self.engine.setProperty('voice', tts_voices[voice_idx].id)
        else:
            raise Exception(f'Invalid voice index specified. Number of existing TTS voices is {len(tts_voices)}')

        # Set TTS voice-specific settings
        self.engine.setProperty('rate', int(rate * 100))
        self.engine.setProperty('volume', volume)


    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


    def cleanup(self):
        self.engine.stop()
