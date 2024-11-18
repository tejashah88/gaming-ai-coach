import tkinter as tk

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageTk, ImageOps

from utils import image_proc

class TkScreencapImage:
    def __init__(self, root, width):
        self.img_width = width

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Create a temporary blank image for the PhotoImage widget
        tmp_blank_image = Image.new(
            mode='RGB',
            size=(screen_width, screen_height),
            color='black',
        )

        processed_blank_image = self._post_process_image(
            np.array(tmp_blank_image)
        )

        self.img_screencap = ImageTk.PhotoImage(
            image=processed_blank_image
        )

        # Create a Label widget to display the image
        self.img_label = tk.Label(root, image=self.img_screencap) # type: ignore
        # NOTE: For some reason, setting the image attribute prevents a blank display...
        #   Source: https://stackoverflow.com/a/47138805
        self.img_label.image = self.img_screencap # type: ignore


    def _post_process_image(self, img_data) -> Image.Image:
        image_resized = Image.fromarray(
            image_proc.resize_image_min_length(img_data, width=self.img_width)
        )

        # Add a small white border around image
        bordered_image = ImageOps.expand(image_resized, border=8, fill='white')
        return bordered_image


    @property
    def widget(self) -> tk.Label:
        return self.img_label


    def set_image(self, img_data: NDArray) -> None:
        # Do some post processing on the image
        post_image = self._post_process_image(img_data)

        # Replace the image with a new one
        self.img_screencap.paste(post_image)
