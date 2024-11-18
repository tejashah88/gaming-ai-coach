import time
import json

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

from modules.ai_coach import AICoach
from modules.image_proc.monitor_cam import MonitorCam
from modules.chatbot.llm_chatbot import LLMChatbot
from modules.chatbot.messages import HumanTextMessage, HumanImageMessage

from modules.text_to_speech.offline.windows_tts import WindowsTTS
from modules.overlay_ui.snapshot_overlay import SnapshotOverlay

from utils.perf_timer import PerfTimer
from utils import image_proc


# Load environment variables
load_dotenv('.env')


# Screenshot capture options
GPU_IDX = 0
MONITOR_IDX = 0
LOW_RESOLUTION_MODE = False

# Coaching AI options
MODEL_PROVIDER = 'openai'
MODEL_NAME = 'gpt-4o'
# PROMPTS_LIST_PATH = 'prompts/general-shounic.json'
# PROMPT_CONFIG_NAME = 'sarcastic-shounic'
PROMPTS_LIST_PATH = 'prompts/general-experiment.json'
PROMPT_CONFIG_NAME = 'sassy-roaster'

KEEP_BACK_FORTH_HISTORY=3

# TTS general options
MAIN_TTS_SERVICE = 'online-ai'

# TTS-specific settings
TTS_COQUI_VOICE_SAMPLES_PATH = r'C:\Users\Tejas\Downloads\Squidward Tentacles\*.wav'
TTS_ELEVENLABS_VOICE_MODEL = 'squidward-tentacles'
# TTS_ELEVENLABS_VOICE_MODEL = 'spongebob'


# Start a Text-to-speech service based on either ElevenLabs or the Windows API
match MAIN_TTS_SERVICE:
    case 'online-ai':
        from modules.text_to_speech.online.elevenlabs_tts import ElevenLabsTTS
        from elevenlabs.types import VoiceSettings

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
        from modules.text_to_speech.offline.coqui_ai_tts import CoquiTTS

        main_tts = CoquiTTS(
            voice_samples_path=TTS_COQUI_VOICE_SAMPLES_PATH,
            rate=1.25,
        )
    case _:
        main_tts = None

# Start the performance timer
perf_timer = PerfTimer(
    default_precision=3
)

coach = AICoach(
    # Start a virtual camera to start taking screenshots of the game
    monitor_cam = MonitorCam(
        device_idx=GPU_IDX,
        output_idx=MONITOR_IDX,
    ),
    # Initialize the LLM model interface
    chatbot = LLMChatbot(
        chat_model=init_chat_model(
            model_provider=MODEL_PROVIDER,
            model=MODEL_NAME,
        ),
        keep_back_forth_cycles=KEEP_BACK_FORTH_HISTORY,
    ),
    # Setup TTS services
    main_tts=main_tts,
    fallback_tts=WindowsTTS(
        voice_idx=0,
        rate=1.5,
        volume=1.00
    )
)

# Load list of prompts and fetch system and user prompts with given config name
with open(PROMPTS_LIST_PATH, 'r') as fp:
    PROMPTS_LIST = json.load(fp)

current_prompt_config = PROMPTS_LIST[PROMPT_CONFIG_NAME]

coach.setup_prompts(
    system_prompt=current_prompt_config['system-prompt'],
    input_prompts=[
        *[HumanTextMessage(message) for message in current_prompt_config['user-prompts']],
        HumanImageMessage('{image_input}')
    ],
)

# Create the snapshot overlay to display the screenshot and bot response
snap_overlay = SnapshotOverlay()
snap_overlay.hide_ui()
# snap_overlay.prevent_freezing()

print(f'Starting coach with following configuration...')
CHATBOT_SETTINGS = {
    'model': {
        'provider': MODEL_PROVIDER,
        'name': MODEL_NAME,
        'params': coach.fetch_chatbot_params(),
    },
    'prompt': {
        'list_path': PROMPTS_LIST_PATH,
        'config_name': PROMPT_CONFIG_NAME,
        'config': current_prompt_config,
    }
}

print()
print(json.dumps(CHATBOT_SETTINGS, indent=2))

coach.speak_text('Ready to coach!')
try:
    while True:
        # Start a new snapshot in the session
        perf_timer.reset()

        # Make sure to hide the overlay before taking a screenshot
        snap_overlay.hide_ui()
        # NOTE: We add a small amount of delay to prevent the previous screenshot from being captured in the next one
        time.sleep(0.200)

        # Grab a screencap of the current gameplay
        monitor_frame = coach.capture_monitor_screenshot()
        perf_timer.print_elapsed_time_and_reset('Desktop capture from GPU')

        if not LOW_RESOLUTION_MODE:
            # Reduce the smallest side length to 768 (otherwise OpenAI would do it anyways) and convert the screencap to base 64
            # - See https://platform.openai.com/docs/guides/vision#calculating-costs for mode info
            resize_kwargs = {'height': 768}
        else:
            resize_kwargs = {'width': 512}

        resized_frame = image_proc.resize_image_min_length(monitor_frame, **resize_kwargs)
        monitor_frame_b64 = image_proc.numpy_to_base64(resized_frame)
        perf_timer.print_elapsed_time_and_reset('Convert screencap to base 64')

        # Ask the chatbot to process the image with the given prompts
        bot_response = coach.ask_chatbot(image_input=monitor_frame_b64)
        perf_timer.print_elapsed_time_and_reset('AI Gameplay Analysis')

        # Set the snapshot data and show the snapshot overlay
        snap_overlay.set_data(
            screencap_img=resized_frame,
            response_text=bot_response.content, # type: ignore
        )
        print(bot_response.response_metadata)
        snap_overlay.show_ui()
        snap_overlay.update_ui()

        # Speak the bot response via Text-to-Speech
        coach.speak_text(bot_response.content) # type: ignore
        perf_timer.print_elapsed_time_and_reset('TTS Voice transcription')
        print()
except KeyboardInterrupt:
    print('Exiting due to user request...')

    # Close the snapshot overlay
    snap_overlay.root.destroy()

    # Stop the coach and cleanup associated resources
    coach.cleanup()
