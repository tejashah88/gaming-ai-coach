import glob
import os.path
import time
from dataclasses import dataclass, field

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from fancy_dataclass import ArgparseDataclass
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import make_chunks

from utils import file_io


SUPPORTED_EXTENSIONS = ['mp3', 'flv', 'ogg', 'wav', 'raw']
MAX_AUDIO_SAMPLE_SIZE = 10 * 1000 * 1000 # bytes


@dataclass
class PrepSamplesArgs(ArgparseDataclass, default_help=True):
    '''Preps a set of reference audio samples for voice cloning in ElevenLabs and Coqui TTS.'''

    voice_model_name: str = field(
        metadata={
            'args': '--name',
            'required': True,
            'help': 'The name of the voice model.'
        }
    )

    samples_glob_path: str = field(
        metadata={
            'args': '--samples',
            'required': True,
            'help': 'The glob path to the set of audio samples. Refer to https://pymotw.com/3/glob/ for examples.'
        }
    )

    upload_to_elevenlabs: bool = field(
        default=False,
        metadata={
            'args': '--upload-to-elevenlabs',
            'default': False,
            'action': 'store_true',
            'help': 'Should the split audio samples be uploaded to ElevenLabs via the API key specified?'
        }
    )


if __name__ == '__main__':
    # Fetch CLI arguments
    cli_args = PrepSamplesArgs.from_cli_args()
    VOICE_MODEL_NAME     = cli_args.voice_model_name
    SAMPLES_GLOB_PATH    = cli_args.samples_glob_path
    UPLOAD_TO_ELEVENLABS = cli_args.upload_to_elevenlabs

    COMBINED_OUTPUT_PATH = 'tools/output/combined'
    ELEVENLABS_OUTPUT_BASE_PATH = file_io.join_normalized_path('tools/output/elevenlabs', VOICE_MODEL_NAME)

    # Gather all audio files within folder via glob path
    # NOTE: Only WAV format has been tested
    all_found_audio_files = sum([
        glob.glob(file_io.join_normalized_path(SAMPLES_GLOB_PATH, '*.wav')),
        glob.glob(file_io.join_normalized_path(SAMPLES_GLOB_PATH, '*.mp3')),
        glob.glob(file_io.join_normalized_path(SAMPLES_GLOB_PATH, '*.flv')),
        glob.glob(file_io.join_normalized_path(SAMPLES_GLOB_PATH, '*.ogg')),
        glob.glob(file_io.join_normalized_path(SAMPLES_GLOB_PATH, '*.raw')),
    ], [])

    # Combine all audio samples into 1 file
    print(f'Combining {len(all_found_audio_files)} audio samples into 1 file...')
    combined_audio = AudioSegment.empty()
    for audio_file_path in tqdm(all_found_audio_files):
        # Combine current audio with new audio sample
        #   TODO: This functionality needs extensive documentation to better understand how audio samples
        #   of differing formats and internal parameters are merged together.
        file_ext = file_io.get_file_extension(audio_file_path)
        combined_audio += AudioSegment.from_file(audio_file_path, format=file_ext)
        # Add a small segment of silence to allow better separation of small audio samples
        combined_audio += AudioSegment.silent(duration=50)

    # Export the combined audio as a WAV file
    combined_audio.export(
        file_io.join_normalized_path(COMBINED_OUTPUT_PATH, f'{VOICE_MODEL_NAME}.wav'),
        format='wav'
    )

    # NOTE: ElevenLabs only allows uploading up to 25 audio samples of maximum of 10 MBs each. Therefore
    # we need to determine the bytes/second and generate audio sample chunks of the appropriate size.
    bytes_per_second = combined_audio.frame_rate * combined_audio.channels * combined_audio.sample_width
    combined_size_bytes = int(len(combined_audio) / 1000 * bytes_per_second) # NOTE: Length of combined audio is reported in milliseconds
    print(f'  Combined audio has {bytes_per_second} bytes per second, with total size of {combined_size_bytes} bytes')

    # Calculate maximum sample length in seconds per ElevenLabs requirements
    sample_length_sec = int(MAX_AUDIO_SAMPLE_SIZE / bytes_per_second)
    print(f'Splitting into chunks of {sample_length_sec} seconds...')

    # Split combined audio into audio sample chunks
    audio_segments = make_chunks(
        audio_segment=combined_audio,
        chunk_length=sample_length_sec * 1000
    )

    # Create the output folder for the split audio samples
    os.makedirs(ELEVENLABS_OUTPUT_BASE_PATH, exist_ok=True)

    # Save newly generated audio sample chunks to ElevenLabs folder
    print(f'Outputting audio segments to "{ELEVENLABS_OUTPUT_BASE_PATH}"...')
    for (i, segment) in enumerate(audio_segments):
        segment.export( # type: ignore
            file_io.join_normalized_path(ELEVENLABS_OUTPUT_BASE_PATH, f'output_{i+1}.wav'),
            format='wav'
        )


    if UPLOAD_TO_ELEVENLABS:
        # Load environment variables
        load_dotenv('.env')

        # Initialize ElevenLabs client with environment API key
        elevenlabs_client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))

        # Grab all generated audio sample paths and keep only first 25 (limit due to ElevenLabs)
        output_files = glob.glob(f'{ELEVENLABS_OUTPUT_BASE_PATH}/output_*.wav')
        files_to_upload = output_files[:25]
        print(f'Creating voice model "{VOICE_MODEL_NAME}" from {len(files_to_upload)} out of {len(output_files)} audio samples...')

        # Create voice clone model in ElevenLabs with given voice model name
        voice = elevenlabs_client.clone(
            name=VOICE_MODEL_NAME,
            description=f'Auto-generated voice model "{VOICE_MODEL_NAME}" from "prep_samples" tool as of epoch {int(time.time())}.',
            files=files_to_upload,
        )

        print(f'Custom voice model "{VOICE_MODEL_NAME}" from ElevenLabs is ready to use.')
