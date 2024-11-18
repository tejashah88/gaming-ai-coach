import glob
import os.path
import tempfile

from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.utils import make_chunks
from elevenlabs.client import ElevenLabs

from utils.file_io import join_normalized_path

SUPPORTED_EXTENSIONS = ['mp3', 'flv', 'ogg', 'wav', 'raw']
MAX_AUDIO_SAMPLE_SIZE = 10 * 1000 * 1000 # 10 MB

# Load environment variables
load_dotenv('.env')

voice_model_name = input('Name of voice model: ')
samples_path = input('Folder path with audio samples: ')

# Gather all audio files within folder
all_found_audio_files = sum([
    glob.glob(join_normalized_path(samples_path, '*.wav')),
    glob.glob(join_normalized_path(samples_path, '*.mp3')),
    glob.glob(join_normalized_path(samples_path, '*.flv')),
    glob.glob(join_normalized_path(samples_path, '*.ogg')),
    glob.glob(join_normalized_path(samples_path, '*.raw')),
], [])

print(f'  Combining {len(all_found_audio_files)} audio samples into 1 file...')
combined_audio = AudioSegment.empty()
for audio_file_path in all_found_audio_files:
    file_ext = os.path.splitext(audio_file_path)[1][1:].strip().lower()
    combined_audio += AudioSegment.from_file(audio_file_path, format=file_ext)

combined_audio.export(f'audio_tools/output/combined/{voice_model_name}.wav', format='wav')

# NOTE: Elevenlabs only allows uploading up to 25 audio samples of maximum of 10 MBs each. Therefore
# we need to determine the bytes/second and generate audio sample chunks of the appropriate size.
bytes_per_second = combined_audio.frame_rate * combined_audio.channels * combined_audio.sample_width
# NOTE: Length of combined audio is reported in milliseconds
combined_size = len(combined_audio) / 1000 * bytes_per_second
print(f'  Combined audio has {bytes_per_second} bytes per second, with total size of {combined_size} bytes')

sample_length_sec = int(MAX_AUDIO_SAMPLE_SIZE / bytes_per_second)
print(f'  Splitting into chunks of {sample_length_sec} seconds...')
audio_segments = make_chunks(combined_audio, chunk_length=sample_length_sec * 1000)

# with tempfile.TemporaryDirectory() as temp_dir_name:
print(f'  Outputting audio segments to "audio_tools/output/split"...')
for (i, segment) in enumerate(audio_segments):
    segment.export(f'audio_tools/output/split/output_{i+1}.wav', format='wav') # type: ignore

elevenlabs_client = ElevenLabs(api_key=os.getenv('ELEVEN_API_KEY'))

# NOTE: Elevenlabs only allows uploading up to 25 audio samples
output_files = glob.glob(f'audio_tools/output/split/output_*.wav')
files_to_upload = output_files[:25]
print(f'  Creating voice model "{voice_model_name}" from {len(files_to_upload)} out of {len(output_files)} audio samples...')

voice = elevenlabs_client.clone(
    name=voice_model_name,
    description='',
    files=files_to_upload,
)

print(f'  Success! Your voice model "{voice_model_name}" is ready to use')
