from modules.text_to_speech.base.base_tts import BaseTTS
from modules.text_to_speech.offline.windows_tts import WindowsTTS


class TextToSpeechService:
    def __init__(self, online_tts: BaseTTS | None=None, offline_tts: BaseTTS | None=None):
        self.online_tts_service = online_tts

        if offline_tts is not None:
            self.offline_tts_service = offline_tts
        else:
            self.offline_tts_service = WindowsTTS(
                voice_idx=0,
                rate=2.00,
                volume=1.00
            )


    def speak(self, text):
        if self.online_tts_service is not None:
            try:
                self.online_tts_service.speak(text)
            except Exception as ex:
                print('An error has occurred while trying to use the online TTS service. Switching to fallback TTS service...')
                print(ex)

                self.offline_tts_service.speak(text)
        else:
            self.offline_tts_service.speak(text)


    def cleanup(self):
        if self.online_tts_service is not None:
            self.online_tts_service.cleanup()

        self.offline_tts_service.cleanup()
