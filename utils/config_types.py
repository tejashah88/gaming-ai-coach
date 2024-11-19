from dataclasses import dataclass, field
from fancy_dataclass import ConfigDataclass

@dataclass
class ScreenshotConfig:
    # The GPU ID device index. 1st GPU = 0, 2nd GPU = 1, etc.
    GPU_IDX: int = 0

    # The display monitor ID device index. 1st monitor = 0, 2nd monitor = 1, etc.
    MONITOR_IDX: int = 0

    # Sets resolution mode for resizing images prior to sending to LLM model while preserving aspect ratio.
    # NOTE: These default are meant for OpenAI but work well for most other providers.
    #   If 'false', resize screenshots such that height is 768.
    #     See https://platform.openai.com/docs/guides/vision#calculating-costs for more info
    #   If 'true', resize screenshots such that width is 512.
    LOW_RESOLUTION_MODE: bool = False


@dataclass
class ChatbotConfig:
    # Select company provider for LLM chatbot model.
    MODEL_PROVIDER: str = 'openai'

    # Select LLM chat model name from company provider.
    MODEL_NAME: str = 'gpt-4o'

    # Keep at most 'n' back-and-forth interactions between human and bot. Set to 0 to always discard history.
    KEEP_BACK_FORTH_HISTORY: int = 0


@dataclass
class PromptsConfig:
    # The JSON file path for the list of prompts to load from.
    PROMPTS_LIST_PATH: str = 'prompts/shounic.json'

    # The key name of the specific prompt config from the aforementioned JSON file path.
    PROMPT_CONFIG_NAME: str = 'neutral'


@dataclass
class TextToSpeechOfflineAiConfig:
    # Glob path to list of example audio samples for use with voice cloning. Refer to https://pymotw.com/3/glob/ for examples.
    VOICE_SAMPLES_PATH: str = 'scripts/example-data/voice.wav'


@dataclass
class TextToSpeechOnlineAiConfig:
    # Internal voice model ID for ElevenLabs, can either be from pre-existing models or custom-made cloned models.
    ONLINE_VOICE_MODEL: str = 'example-voice-model'


@dataclass
class TextToSpeechConfig:
    # Can specify the following based on which TTS service you want. There is a fallback mode to use Window TTS
    # in case using the main TTS service fails for any reason.
    # - 'online-ai' for ElevenLabs
    # - 'offline-ai' for CoquiTTS (XTTS v2)
    # - 'windows' for Microsoft's default TTS
    MAIN_TTS_SERVICE: str = 'windows'

    # Offline AI module based on CoquiTTS
    offline_ai: TextToSpeechOfflineAiConfig = field(default_factory=TextToSpeechOfflineAiConfig)

    # Online AI module based on ElevenLabs
    online_ai: TextToSpeechOnlineAiConfig = field(default_factory=TextToSpeechOnlineAiConfig)


@dataclass
class CoachConfig(ConfigDataclass):
    screenshot: ScreenshotConfig
    chatbot: ChatbotConfig
    prompts: PromptsConfig
    text_to_speech: TextToSpeechConfig
