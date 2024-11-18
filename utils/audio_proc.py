import io

from audiostretchy.stretch import AudioStretch
import numpy as np
import soundfile as sf

from typing import BinaryIO
from numpy.typing import NDArray


def arr_to_wav_bytes(audio_data: NDArray, sample_rate: int) -> BinaryIO:
    tmp_wav_buffer = io.BytesIO()
    sf.write(file=tmp_wav_buffer, data=audio_data, samplerate=sample_rate, format='wav')

    tmp_wav_buffer.seek(0)
    return tmp_wav_buffer


def time_stretch(path: str | None = None, file: BinaryIO | None = None, rate: float = 1) -> NDArray:
    if path is None and file is None:
        raise Exception('Stretching audio requires either the "path" or "file" to be specified')

    if path is not None and file is not None:
        raise Exception('Stretching audio cannot have both "path" and "file" to be specified')

    audio_stretcher = AudioStretch()
    audio_stretcher.open(path=path, file=file, format='wav')
    audio_stretcher.stretch(ratio=1 / rate)

    return np.array(audio_stretcher.samples)
