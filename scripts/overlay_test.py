from PIL import Image
import numpy as np

from ui.snapshot_overlay import SnapshotOverlay
from utils.file_io import join_normalized_path


if __name__ == '__main__':
    # File path definitions
    example_screenshot_path = join_normalized_path('scripts', 'example-data', 'screencap.png')
    example_responses_path = join_normalized_path('scripts', 'example-data', 'response.txt')

    # Load example data
    with open(example_responses_path, 'r') as fp:
        response_text = fp.read()

    with open(example_screenshot_path, 'rb') as fp:
        screencap_image = np.array(Image.open(fp))

    # Create screen overlay with example data
    overlay_test = SnapshotOverlay()
    overlay_test.set_data(
        screencap_img=screencap_image,
        response_text=response_text,
    )

    # Show the overlay
    overlay_test.show_ui()
    overlay_test.root.mainloop()
