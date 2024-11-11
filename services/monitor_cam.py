from contextlib import contextmanager

import dxcam
from PIL import Image


class MonitorCam:
    def __init__(self, device_idx: int = 0, output_idx: int = 0):
        self.camera = dxcam.create(device_idx=device_idx, output_idx=output_idx)


    def grab_screenshot(self):
        return self.camera.grab();


    def preview_screenshot(self):
        frame = self.grab_screenshot()
        Image.fromarray(frame).show() # type: ignore


    def get_screencap_frame(self):
        return self.camera.get_latest_frame()


    @contextmanager
    def screencap_session(self, *args, **kwargs):
        self.camera.start(*args, **kwargs)

        try:
            yield
        finally:
            self.camera.stop()

