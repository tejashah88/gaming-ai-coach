import tkinter as tk

from numpy.typing import NDArray
from PIL import Image, ImageTk, ImageOps

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

        processed_blank_image = self._post_process_image(tmp_blank_image)

        self.img_screencap = ImageTk.PhotoImage(
            image=processed_blank_image
        )

        # Create a Label widget to display the image
        self.img_label = tk.Label(root, image=self.img_screencap)
        # NOTE: For some reason, setting the image attribute prevents a blank display...
        #   Source: https://stackoverflow.com/a/47138805
        self.img_label.image = self.img_screencap


    def _post_process_image(self, pil_image):
        # Resize image to have width of 500px and respecting aspect ratio
        img_ratio = pil_image.height / pil_image.width
        target_width = self.img_width
        calculated_height = int(target_width * img_ratio)
        image_resized = pil_image.resize((target_width, calculated_height))

        # Add a small white border around image
        bordered_image = ImageOps.expand(image_resized, border=8, fill='white')
        return bordered_image


    @property
    def widget(self):
        return self.img_label


    def set_image(self, img_data: NDArray):
        # Open image from filepath
        image = Image.fromarray(img_data)

        # Do some post processing on the image
        post_image = self._post_process_image(image)

        # Replace the image with a new one
        self.img_screencap.paste(post_image)
