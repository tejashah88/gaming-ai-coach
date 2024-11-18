from modules.image_proc.monitor_cam import MonitorCam
from modules.chatbot.llm_chatbot import LLMChatbot
from modules.chatbot.messages import HumanTextMessage, HumanImageMessage

from modules.text_to_speech.base.base_tts import BaseTTS
from modules.text_to_speech.tts_service import TextToSpeechService

from numpy.typing import NDArray


class AICoach:
    def __init__(
        self,
        monitor_cam: MonitorCam,
        chatbot: LLMChatbot,
        main_tts: BaseTTS | None,
        fallback_tts: BaseTTS | None
    ):
        self.monitor = monitor_cam
        self.chatbot = chatbot

        # Start a Text-to-speech service based on either ElevenLabs or the Windows API
        self.tts_service = TextToSpeechService(
            main_tts=main_tts,
            fallback_tts=fallback_tts
        )

        self.prompts_setup: bool = False


    def setup_prompts(self, system_prompt: str, input_prompts: list[HumanTextMessage | HumanImageMessage]):
        self.chatbot.setup_prompt_template(
            system_message=system_prompt,
            human_messages=input_prompts,
        )

        self.prompts_setup = True


    def capture_monitor_screenshot(self) -> NDArray:
        frame = self.monitor.grab_screenshot()
        return frame


    def ask_chatbot(self, **kwargs):
        if not self.prompts_setup:
            raise Exception(f'Chatbot prompts are not setup with {self.__class__.__name__}.{self.setup_prompts.__name__}()')

        bot_response = self.chatbot.send_message(prompt_vars=kwargs)
        return bot_response


    def fetch_chatbot_params(self):
        return self.chatbot.chat_model._identifying_params


    def speak_text(self, text: str):
        self.tts_service.speak(text)


    def cleanup(self):
        # Stop the TTS engine (if applicable)
        self.tts_service.cleanup()
