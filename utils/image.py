import io
import base64

from PIL import Image

def numpy_to_base64(np_arr):
    pil_image = Image.fromarray(np_arr)

    buffer = io.BytesIO()
    pil_image.save(buffer, format='PNG')
    buffer.seek(0)

    encoded_img = base64.b64encode(buffer.read()).decode('utf-8')
    return encoded_img
