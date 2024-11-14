import io
from typing import BinaryIO
from audiostretchy.stretch import AudioStretch
import numpy as np

audio_stretch = AudioStretch()

def time_stretch(path: str | None = None, file: BinaryIO | None = None, rate: float = 1):
    if path is None and file is None:
        raise Exception('Stretching audio requires either the "path" or "file" to be specified')

    if path is not None and file is not None:
        raise Exception('Stretching audio cannot have both "path" and "file" to be specified')

    audio_stretcher = AudioStretch()
    audio_stretcher.open(path=path, file=file, format='wav')
    audio_stretcher.stretch(ratio=1 / rate)

    return np.array(audio_stretcher.samples)
