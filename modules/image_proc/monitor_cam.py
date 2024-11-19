from contextlib import contextmanager
from typing import Any, Generator

import dxcam
from PIL import Image

from numpy.typing import NDArray


class MonitorCam:
    def __init__(self, device_idx: int = 0, output_idx: int = 0):
        self.camera = dxcam.create(device_idx=device_idx, output_idx=output_idx, output_color='BGR')


    def grab_screenshot(self) -> NDArray:
        frame = None

        while True:
            # NOTE: Sometimes this can return 'None' if it fails to get a screencap
            frame = self.camera.grab();
            if frame is not None:
                break

        return frame[:, :, ::-1];


    def preview_screenshot(self) -> None:
        frame = self.grab_screenshot()
        Image.fromarray(frame).show()


    # NOTE: See typing definition for generator: https://docs.python.org/3.10/library/typing.html#typing.Generator
    @contextmanager
    def screencap_session(self, *args: Any, **kwargs: Any) -> Generator[None, Any, None]:
        self.camera.start(*args, **kwargs)

        try:
            yield
        finally:
            self.camera.stop()


    def get_screencap_frame(self) -> NDArray:
        frame = None

        while True:
            # NOTE: Sometimes this can return 'None' if it failed to get a screencap for "some" reason
            frame = self.camera.get_latest_frame()
            if frame is not None:
                break

        return frame;
