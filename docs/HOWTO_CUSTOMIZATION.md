# Customization

## Table of Contents
* [Adding your own prompts](#adding-your-own-prompts)
* [Changing to different model provider](#changing-to-different-model-provider)
* [Creating cloned voice model for TTS](#creating-cloned-voice-model-for-tts)

## Adding your own prompts
You can add new prompts by either editing the existing JSON file in `prompts/experiment.json` or making a new JSON file with the following format:
```json
{
    "normal-coach": {
        "system-prompt": "You are coaching a novice on what to do in a video game. You need to tell him exactly what to do and what's the best course of action in the given moment. The person you are coaching is playing right now, so keep instructions to one sentence.",
        "user-prompts": [
            "This is a screenshot of the current situation. In one short sentence, please tell me exactly what I should do next? Deliver your repsonse concisely, neutrally and without bias."
        ]
    },
    "custom-coach": {
        "system-prompt": "...",
        "user-prompts": [
            "..."
        ]
    },
    ...
}
```

1. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and change `PROMPTS_LIST_PATH` and `PROMPT_CONFIG_NAME` in the `prompts` section accordingly.
```toml
[prompts]
# The JSON file path for the list of prompts to load from.
PROMPTS_LIST_PATH = 'prompts/custom.json'

# The key name of the specific prompt config from the aforementioned JSON file path.
PROMPT_CONFIG_NAME = 'custom-coach'
```
2. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-prompts.toml
```

## Changing to different model provider
1. Go to "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" and double-check if your desired provider is supported. Remember that the models in question must support multimodal inputs.
2. Install the relevant LangChain packages from the aforementioned link.
3. Add the necessary environment variables to your `.env` file for the chosen model provider.
4. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and change `MODEL_PROVIDER` and `MODEL_NAME` in the `chatbot` section accordingly.
```toml
[chatbot]
# Select company provider for LLM chatbot model.
MODEL_PROVIDER = 'anthropic'

# Select LLM chat model name from company provider.
MODEL_NAME = 'claude-3-5-sonnet-20240620'
```
5. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-provider.toml
```

## Creating cloned voice model for TTS
1. Find a set of audio samples (in WAV format or converted to it) to use as the basis for your target voice to be cloned. Here's a few resources to start:
   * [/g/ Voice Sample Repository](https://rentry.org/Voice-Samples)
   * [The Sounds Resource](https://www.sounds-resource.com/)
   * [Aiartes - VoiceAI](https://web.archive.org/web/20241006171246/https://aiartes.com/voiceai)
2. Run the following command to generate 2 outputs: (1) A single WAV file with all audio samples combined and (2) a series of split audio samples for ElevenLabs, with each sample being no bigger than 10 MB.
   * *Glob path* refers to a normal path but with being able to use wildcard symboles to find matching files of similar paths.
   * Single asterisk (\*) allows matching similar file names and double asterisk (\*\*) allows matching similar sub-folders.
   * Refer to https://pymotw.com/3/glob/ for examples.
```bash
# Help command display
python -m tools.prep_samples --help
```
Help command display:
```bash
usage: prep_samples.py [-h] --name VOICE_MODEL_NAME --samples SAMPLES_GLOB_PATH [--upload-to-elevenlabs]

Preps a set of reference audio samples for voice cloning in ElevenLabs and Coqui TTS.

options:
  -h, --help            show this help message and exit
  --name VOICE_MODEL_NAME
                        The name of the voice model.
  --samples SAMPLES_GLOB_PATH
                        The glob path to the set of audio samples. Refer to https://pymotw.com/3/glob/ for examples.
  --upload-to-elevenlabs
                        Should the split audio samples be uploaded to ElevenLabs via the API key specified? (default: False)
```
Example usage:
```bash
# Use this command if you just want to generate the audio samples files
python -m tools.prep_samples --name example-voice-model --samples "path/to/voice_samples/*.wav"

# Add the '--upload-to-elevenlabs' if you want to directly create a cloned voice model via ElevenLabs' API
python -m tools.prep_samples --name squid-test --samples "path/to/voice_samples/*.wav" --upload-to-elevenlabs
```
3. Move the generated audio files from `tools/output` to an appropriate location.
4. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and change `MAIN_TTS_SERVICE`, `ONLINE_VOICE_MODEL` and `VOICE_SAMPLES_PATH` in the `text_to_speech` section accordingly.
```toml
[text_to_speech]
# Can specify the following based on which TTS service you want. There is a fallback mode to use Window TTS
# in case using the main TTS service fails for any reason.
# - 'online-ai' for ElevenLabs
# - 'offline-ai' for CoquiTTS (XTTS v2)
# - 'windows' for Microsoft's default TTS
MAIN_TTS_SERVICE = 'online-ai'

[text_to_speech.online_ai]
# Internal voice model ID for ElevenLabs, can either be from pre-existing models or custom-made cloned models.
ONLINE_VOICE_MODEL = 'example-voice-model'

[text_to_speech.offline_ai]
# Glob path to list of example audio samples for use with voice cloning. Refer to https://pymotw.com/3/glob/ for examples.
VOICE_SAMPLES_PATH = 'tools/output/combined/example-voice-model.wav'
```
5. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-voice.toml
```
