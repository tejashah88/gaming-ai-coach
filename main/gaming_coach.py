import json
import time

from dotenv import load_dotenv
import numpy as np

from modules.image_proc.monitor_cam import MonitorCam
from modules.ai_chatbot.llm_chatbot import LLMChatbot
from modules.ai_chatbot.structs import UserTextMessage, UserImageMessage
from modules.text_to_speech.offline.windows_tts import WindowsTTS
from ui.snapshot_overlay import SnapshotOverlay

from utils.perf_timer import PerfTimer
from utils.image_proc import numpy_to_base64, resize_image_min_length

from main.model_configs import OpenAIConfig

# Start a virtual camera to start taking screenshots of the game
monitor = MonitorCam(
    device_idx=0,
    output_idx=0,
)

# Start a Text-to-speech service based on the Windows API
tts_service = WindowsTTS(
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
with open('prompts/general-shounic.json', 'r') as fp:
    PROMPTS_LIST = json.load(fp)

current_prompt_config = PROMPTS_LIST[PROMPT_CONFIG_NAME]

# Initialize the LLM model interface
chatbot = LLMChatbot(
    chat_model=MODEL_CONFIG.init_chat_model(),
    system_message=current_prompt_config['system-prompt'],
)

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


# Create the snapshot overlay to display the screenshot and bot response
snap_overlay = SnapshotOverlay()
# snap_overlay.prevent_freezing()


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

        # Reduze the smallest side length to 768 (otherwise OpenAI would do it anyways) and convert the screencap to base 64
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
            response_text=bot_response,
        )
        snap_overlay.show_ui()
        snap_overlay.update_ui()

        # Speak the bot response via Text-to-Speech
        tts_service.speak(bot_response)
        perf_timer.print_elapsed_time_and_reset('TTS Voice transcription')
        print()
except KeyboardInterrupt:
    print('Exiting due to user request...')

    # Close the snapshot overlay
    snap_overlay.root.destroy()

    # Stop the TTS engine
    tts_service.engine.stop()
