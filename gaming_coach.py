import time
import json

from dotenv import load_dotenv
import numpy as np

from langchain.chat_models import init_chat_model
from elevenlabs.types import VoiceSettings

from modules.image_proc.monitor_cam import MonitorCam
from modules.ai_chatbot.llm_chatbot import LLMChatbot
from modules.ai_chatbot.messages import UserTextMessage, UserImageMessage
from modules.text_to_speech.offline.coqui_ai_tts import CoquiTTS
from modules.text_to_speech.offline.windows_tts import WindowsTTS
from modules.text_to_speech.online.elevenlabs_tts import ElevenLabsTTS
from modules.overlay_ui.snapshot_overlay import SnapshotOverlay

from modules.text_to_speech.tts_service import TextToSpeechService
from utils.perf_timer import PerfTimer
from utils.image_proc import numpy_to_base64, resize_image_min_length


# Load environment variables
load_dotenv('.env')


# Screenshot capture options
GPU_IDX = 0
MONITOR_IDX = 0

# Coaching AI options
MODEL_PROVIDER = 'openai'
MODEL_NAME = 'gpt-4o'
PROMPTS_LIST_PATH = 'prompts/general-shounic.json'
PROMPT_CONFIG_NAME = 'sarcastic-shounic'

# TTS general options
MAIN_TTS_SERVICE = 'offline-ai'

# TTS-specific settings
TTS_COQUI_VOICE_SAMPLES_PATH = r'C:\Users\Tejas\Downloads\Squidward Tentacles\*.wav'
TTS_ELEVENLABS_VOICE_MODEL = 'squidward-tentacles'
# TTS_ELEVENLABS_VOICE_MODEL = 'spongebob'


# Start a virtual camera to start taking screenshots of the game
monitor = MonitorCam(
    device_idx=GPU_IDX,
    output_idx=MONITOR_IDX,
)

# Start a Text-to-speech service based on either ElevenLabs or the Windows API
match MAIN_TTS_SERVICE:
    case 'online-ai':
        main_tts = ElevenLabsTTS(
            voice=TTS_ELEVENLABS_VOICE_MODEL,
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=False,
            ),
            rate=1.0,
        )
    case 'offline-ai':
        main_tts = CoquiTTS(
            voice_samples_path=TTS_COQUI_VOICE_SAMPLES_PATH,
            rate=1.25,
        )
    case _:
        main_tts = None


tts_service = TextToSpeechService(
    main_tts=main_tts,
    fallback_tts=WindowsTTS(
        voice_idx=0,
        rate=1.50,
        volume=1.00
    )
)

# Start the performance timer
perf_timer = PerfTimer(
    default_precision=3
)

# Load list of prompts and fetch system and user prompts with given config name
with open(PROMPTS_LIST_PATH, 'r') as fp:
    PROMPTS_LIST = json.load(fp)

current_prompt_config = PROMPTS_LIST[PROMPT_CONFIG_NAME]

# Initialize the LLM model interface
chatbot = LLMChatbot(
    chat_model=init_chat_model(
        model_provider=MODEL_PROVIDER,
        model=MODEL_NAME,
    ),
    system_message=current_prompt_config['system-prompt'],
)

CHATBOT_SETTINGS = {
    'model': {
        'provider': MODEL_PROVIDER,
        'name': MODEL_NAME,
        'params': chatbot.chat_model._identifying_params,
    },
    'prompt': {
        'list_path': PROMPTS_LIST_PATH,
        'config_name': PROMPT_CONFIG_NAME,
        'config': current_prompt_config,
    }
}

print(json.dumps(CHATBOT_SETTINGS, indent=2))

# Create the snapshot overlay to display the screenshot and bot response
snap_overlay = SnapshotOverlay()
# snap_overlay.prevent_freezing()
snap_overlay.hide_ui()

print(f'Starting coach with configuration "{PROMPT_CONFIG_NAME}"...')
tts_service.speak('Ready to coach!')
try:
    while True:
        # Start a new snapshot in the session
        perf_timer.reset()

        # Make sure to hide the overlay before taking a screenshot
        snap_overlay.hide_ui()
        # NOTE: We add a small amount of delay to prevent the previous screenshot from being captured in the next one
        time.sleep(0.200)

        # Grab a screencap of the current gameplay
        frame = monitor.grab_screenshot()
        perf_timer.print_elapsed_time_and_reset('Screencap capture')

        # Reduce the smallest side length to 768 (otherwise OpenAI would do it anyways) and convert the screencap to base 64
        # - See https://platform.openai.com/docs/guides/vision#calculating-costs for mode info
        resized_frame = resize_image_min_length(frame, height=768)
        b64_img = numpy_to_base64(resized_frame)
        perf_timer.print_elapsed_time_and_reset('Screencap to base 64')

        # Ask the chatbot to process the image with the given prompts
        # TODO: Sometimes this can take a very long time to respond (if at all), not sure why...
        bot_response = chatbot.send_message([
            *[UserTextMessage(text=prompt_text) for prompt_text in current_prompt_config['user-prompts']],
            UserImageMessage(image_data=b64_img),
        ])

        # Save the bot's response to a file
        perf_timer.print_elapsed_time_and_reset('AI Gameplay Analysis')

        # Set the snapshot data and show the snapshot overlay
        snap_overlay.set_data(
            screencap_img=np.array(frame),
            response_text=bot_response.content, # type: ignore
        )
        snap_overlay.show_ui()
        snap_overlay.update_ui()

        # Speak the bot response via Text-to-Speech
        tts_service.speak(bot_response.content) # type: ignore
        perf_timer.print_elapsed_time_and_reset('TTS Voice transcription')
        print()
except KeyboardInterrupt:
    print('Exiting due to user request...')

    # Close the snapshot overlay
    snap_overlay.root.destroy()

    # Stop the TTS engine (if applicable)
    tts_service.cleanup()
