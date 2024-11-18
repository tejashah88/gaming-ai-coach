# Source inspired by https://github.com/notatallshaw/fall_guys_ping_estimate/blob/e95ce2f7410af578b84fda957c8740f3e5546eba/fgpe/overlay.py

import sys
import tkinter as tk
import signal

from numpy.typing import NDArray

from modules.overlay_ui.components.tk_screencap_image import TkScreencapImage


# Source: https://stackoverflow.com/a/66788780
def attach_exit_handling(root: tk.Tk) -> None:
    # Define common handler for exit handling
    def on_request_exit():
        root.destroy()
        sys.exit(0)

    # Set up a signal listener to listen to SIGINT
    signal.signal(signal.SIGINT, lambda sig, frame: on_request_exit())

    # Set up a handler on the root window to handle an exit request
    root.protocol('WM_DELETE_WINDOW', on_request_exit)

    # Setup a global keypress for Ctrl+C to be bound to an exit request
    root.bind_all('<Control-c>', lambda event: on_request_exit())


class SnapshotOverlay:
    OVERLAY_WIDTH = 400

    def __init__(self):
        # Initialize Tkinter window
        self.root = tk.Tk()

        # Set up screencap image display
        self.screencap_image = TkScreencapImage(self.root, self.OVERLAY_WIDTH)
        self.screencap_image.widget.pack(side='top', anchor='w', pady=(0, 10))

        # Set up bot response label
        self.response_text = tk.StringVar()
        self.response_text.set('Ready to coach!')
        self.lbl_response = tk.Label(
            self.root,
            textvariable=self.response_text,
            font=('Roboto Mono', 14, 'bold'),
            justify='left',
            wraplength=self.OVERLAY_WIDTH,
            background='white',
        )
        self.lbl_response.pack()

        # Set the window to frameless
        self.root.overrideredirect(True)

        # Shift the window 10 pixels towards bottom-right
        self.root.geometry('+10+10')

        # Lift the window on top of everything else
        self.root.lift()

        # Set the window to be on top of every other window
        self.root.wm_attributes('-topmost', True)

        # Set the background color of the window to transparent
        # HACK: This may cause specific pixels in-game to be transparent, may disable it later
        self.root.wm_attributes('-transparentcolor', self.root['bg'])

        # Attach responsive exit handling with Ctrl+C and SIGINT handling
        attach_exit_handling(self.root)


    def set_data(self, screencap_img: NDArray, response_text: str) -> None:
        self.screencap_image.set_image(screencap_img)
        self.response_text.set(response_text.strip())


    def update_ui(self) -> None:
        self.root.update()
        self.root.update_idletasks()


    def show_ui(self) -> None:
        self.root.deiconify()


    def hide_ui(self) -> None:
        self.root.withdraw()
