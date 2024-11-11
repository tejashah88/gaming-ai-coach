import json
import time
import os

from PIL import Image

from utils.file_io import join_normalized_path, ensure_folders


def get_epoch_seconds():
    return int(time.time())


class SessionLogger:
    def __init__(self, root_folder, settings_dict):
        self.root_folder = root_folder

        self.session_folder = join_normalized_path(self.root_folder, f'session-{get_epoch_seconds()}/')
        ensure_folders(self.session_folder)

        # Definitons for file paths
        self.settings_path = join_normalized_path(self.session_folder, 'settings.json')
        self.perf_timing_path = join_normalized_path(self.session_folder, 'timings.json')
        self.screenshots_folder = join_normalized_path(self.session_folder, 'screenshots/')
        self.bot_repsonses_folder = join_normalized_path(self.session_folder, 'repsonses/')

        ensure_folders(self.screenshots_folder)
        ensure_folders(self.bot_repsonses_folder)

        # Save settings to file
        with open(self.settings_path, 'w') as fp:
            json.dump(settings_dict, fp)

        self.current_instance_name: str | None = None


    def start_new_snapshot(self):
        self.current_snapshot_name = f'{get_epoch_seconds()}'


    def save_screencap(self, np_arr):
        if not self.current_snapshot_name:
            raise Exception(f'A new snapshot instance has not been instantiated')

        screenshot_path = join_normalized_path(self.screenshots_folder, f'{self.current_snapshot_name}.png')
        if not os.path.exists(screenshot_path):
            pil_image = Image.fromarray(np_arr)
            pil_image.save(screenshot_path, format='PNG')
        else:
            raise Exception(f'Screencap already exists for snapshot of {self.current_snapshot_name}')


    def save_chatbot_response(self, bot_response):
        if not self.current_snapshot_name:
            raise Exception(f'A new snapshot instance has not been instantiated')

        bot_response_path = join_normalized_path(self.bot_repsonses_folder, f'{self.current_snapshot_name}.txt')
        if not os.path.exists(bot_response_path):
            with open(bot_response_path, 'w', encoding='utf-8') as fp:
                fp.write(bot_response)
        else:
            raise Exception(f'Screencap already exists for snapshot of {self.current_snapshot_name}')
