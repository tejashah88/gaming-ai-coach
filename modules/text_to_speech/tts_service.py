import traceback

from modules.text_to_speech.base.base_tts import BaseTTS
from modules.text_to_speech.offline.windows_tts import WindowsTTS


class TextToSpeechService:
    def __init__(
        self,
        main_tts: BaseTTS | None=None,
        fallback_tts: BaseTTS | None=None,
    ):
        self.main_tts_service = main_tts

        if fallback_tts is not None:
            self.fallback_tts_service = fallback_tts
        else:
            self.fallback_tts_service = WindowsTTS(
                voice_idx=0,
                rate=1.0,
                volume=1.00,
            )


    def speak(self, text: str) -> None:
        if self.main_tts_service is not None:
            try:
                self.main_tts_service.speak(text)
            except Exception as ex:
                print('An error has occurred while trying to use the main TTS service. Switching to fallback TTS service...')
                print(traceback.format_exc())

                self.fallback_tts_service.speak(text)
        else:
            self.fallback_tts_service.speak(text)


    def cleanup(self) -> None:
        if self.main_tts_service is not None:
            self.main_tts_service.cleanup()

        self.fallback_tts_service.cleanup()
