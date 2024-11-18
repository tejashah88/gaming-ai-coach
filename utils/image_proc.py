import io
import base64

import numpy as np
from PIL import Image

from numpy.typing import NDArray


def numpy_to_base64(np_arr: NDArray) -> str:
    pil_image = Image.fromarray(np_arr)

    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)

    encoded_img = base64.b64encode(buffer.read()).decode('utf-8')
    return encoded_img


def resize_image_min_length(img_data: NDArray, width: int = -1, height: int = -1) -> NDArray:
    pil_image = Image.fromarray(img_data)

    if width == -1 and height == -1:
        raise Exception('Resizing image by minimum length requires either the width or height to be specified')

    if width != -1 and height != -1:
        raise Exception('Resizing image by minimum length cannot have both width and height to be specified')

    if width != -1:
        # Calculate aspect ratio such that it's greater than 1
        aspect_ratio = pil_image.height / pil_image.width
        calculated_height = int(width * aspect_ratio)
        image_resized = pil_image.resize((width, calculated_height))
    else: # implied case: height != -1
        # Calculate aspect ratio such that it's greater than 1
        aspect_ratio = pil_image.width / pil_image.height
        calculated_width = int(height * aspect_ratio)
        image_resized = pil_image.resize((calculated_width, height))

    return np.array(image_resized)
