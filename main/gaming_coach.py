import time

from dotenv import load_dotenv
import numpy as np

from services.monitor_cam import MonitorCam
from services.chatbot.llm_chatbot import LLMChatbot, UserTextMessage, UserImageMessage
from services.session_logger import SessionLogger
from services.tts_voice import TTSVoice
from ui.snapshot_overlay import SnapshotOverlay

from utils.perf_timer import PerfTimer
from utils.image import numpy_to_base64

from main.model_configs import OpenAIConfig

# Start a virtual camera to start taking screenshots of the game
monitor = MonitorCam(
    device_idx=0,
    output_idx=0,
)

# Start a Text-to-speech service based on the Windows API
tts_coach = TTSVoice(
    voice_idx=0,
    rate=2.00,
    volume=1.00
)


# Start the performance timer
perf_timer = PerfTimer(
    default_precision=3
)

# Load environment variables
load_dotenv('.env')

# Load LLM Config and related settings
MODEL_CONFIG = OpenAIConfig()
PROMPT_CONFIG_NAME = 'sarcastic-shounic'

# Load list of prompts and fetch system and user prompts with given config name
PROMPTS_LIST = MODEL_CONFIG.load_prompts()
current_prompt_config = PROMPTS_LIST[PROMPT_CONFIG_NAME]

# Initialize the LLM model interface
chatbot = LLMChatbot(
    chat_model=MODEL_CONFIG.init_chat_model(),
    system_message=current_prompt_config['system-prompt'],
)

# Initialize the session logger for debugging purposes
sesh_logger = SessionLogger(
    root_folder='gameplay-sessions',
    settings_dict={
        'version': 0.1,
        'model': {
            'provider': MODEL_CONFIG.provider,
            'model': MODEL_CONFIG.model,
            'api_params': chatbot.chat_model._default_params,
        },
        'prompt': {
            'config_name': PROMPT_CONFIG_NAME,
            'config': current_prompt_config,
        }
    }
)


# Create the snapshot overlay to display the screenshot and bot response
snap_overlay = SnapshotOverlay()
# snap_overlay.prevent_freezing()


print(f'Starting coach with configuration "{PROMPT_CONFIG_NAME}"...')
tts_coach.speak('Ready to coach!')
try:
    while True:
        # Start a new snapshot in the session
        sesh_logger.start_new_snapshot()
        perf_timer.reset()

        # Make sure to hide the overlay before taking a screenshot
        snap_overlay.hide_ui()

        # NOTE: We add a small amount of delay to prevent the previous screenshot from being captured in the next one
        time.sleep(0.200)

        # Grab a screencap of the current gameplay
        frame = monitor.grab_screenshot()
        perf_timer.print_elapsed_time_and_reset('Screencap capture')

        # Save screencap to a file for later viewing
        sesh_logger.save_screencap(frame)
        perf_timer.print_elapsed_time_and_reset('Screencap to file')

        # Convert the screencap to Base64
        b64_img = numpy_to_base64(frame)
        perf_timer.print_elapsed_time_and_reset('Screencap to base64')

        # Ask the chatbot to process the image with the given prompts
        bot_response = chatbot.send_message([
            UserTextMessage(text=current_prompt_config['user-prompt']),
            UserImageMessage(image_data=b64_img)
        ])

        # Save the bot's response to a file
        sesh_logger.save_chatbot_response(bot_response)
        perf_timer.print_elapsed_time_and_reset('AI Gameplay Analysis')

        # Set the snapshot data and show the snapshot overlay
        snap_overlay.set_data(
            screencap_img=np.array(frame),
            response_text=bot_response,
        )
        snap_overlay.show_ui()
        snap_overlay.update_ui()

        # Speak the bot response via Text-to-Speech
        tts_coach.speak(bot_response)
        perf_timer.print_elapsed_time_and_reset('TTS Voice transcription')
        print()
except KeyboardInterrupt:
    print('Exiting due to user request...')

    # Close the snapshot overlay
    snap_overlay.root.destroy()

    # Stop the TTS engine
    tts_coach.engine.stop()
