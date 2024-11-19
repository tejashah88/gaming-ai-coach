# Gaming AI Coach

An AI-powered backseat coach to fix your skill issue and/or ruin your day :). Powered by OpenAI's GPT-4o and ElevenLabs' TTS services out-of-the-box.

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Quick Setup](#quick-setup)
* [Usage instructions](#usage-instructions)
* [Customization](#customization)
  * [Adding your own prompts](#adding-your-own-prompts)
  * [Changing to different model provider](#changing-to-different-model-provider)
  * [Creating cloned voice model for TTS](#creating-cloned-voice-model-for-tts)
* [Known Caveats](#known-caveats)

### Video: Playing TF2 w/ Squidward as my coach (click the thumbnail below!)
[![TF2 Demo w/ Squidward](https://img.youtube.com/vi/MKgUtl2PALw/maxresdefault.jpg)](https://youtu.be/MKgUtl2PALw)

## Introduction

This project is a recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff. If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do](https://www.youtube.com/watch?v=Z2eduTNisYA).

This experiment takes a screenshot of your current gameplay, feeds it into a given Large Language Model (LLM) like ChatGPT 4o and yells advice to you on how to proceed further with either the default Windows TTS or a custom TTS service such as from ElevenLabs or Coqui TTS.

The fun part about it is that you can use this with **any game**, using **any cloned voice model** and even **customize the prompts** to your liking. I've implemented shounic's original prompts, but it's very easy to add your own. You could for example make a coach that gives advice in a sarcastic or a dramatic manner. See the last 2 sections for more information.

This project is deemed to be mostly finished so no new features will likely be implemented, but if you find any problems, please [make a GitHub issue](https://github.com/tejashah88/gaming-ai-coach/issues).

## Features
* Works with **OpenAI's GPT-4o** model out-of-the-box (other models and providers supported, like from Anthropic or Google).
  * See "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" for more information
* Supports **ElevenLabs' Text-to-speech** service, CoquiTTS (local-first AI-based) or Windows' TTS (as a fallback)
  * Can specify your own instantly cloned voice models
* Shows a small overlay showing the taken screenshot and the model's response
* Easy to customize and experiment with different prompts (via prompts JSON file and config file)

## Quick Setup
1. Clone or fork this repo
2. Get an OpenAI API key (and/or an ElevenLabs API key)
3. Create a `.env` file and add the following contents, substituting `<<INSERT_API_KEY_HERE>>` with your copied API key
```yaml
OPENAI_API_KEY=<<INSERT_API_KEY_HERE>>
ELEVEN_API_KEY=<<INSERT_API_KEY_HERE>> # Optional
```
4. Setup virtual environment with installed dependencies, choosing between either command based on if you have a CUDA-enabled GPU.
```bash
# If you DO NOT have a CUDA-enabled GPU
call setup-env-cpu.bat

# If you DO have a CUDA-enabled GPU. This requires a minimum of CUDA 12.4 to be installed
call setup-env-gpu.bat
```
5. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and refer to the comments to change it to your preferences.
6. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom.toml
```

## Usage instructions

### Starting the application
```bash
python -m gaming_coach --config path/to/config.toml
```
Help command display:
```bash
usage: gaming_coach.py [-h] --config CONFIG_PATH

The main coaching program.

options:
  -h, --help            show this help message and exit
  --config CONFIG_PATH  The path to the config file (ends in .toml)
```

### Exiting the application
The key binding to use is **`Ctrl+C`** as long as you're focused (i.e. last clicked) on either the terminal running the command or on the screenshot overlay.

It can take some time for the current action to stop before the application can shutdown, so please be patient for a few seconds. If it doesn't do anything after that, spamming **`Ctrl+C`** can help, or killing the Python process in Task Manager.

**Known bug**: There's a rare bug where sometimes fetching the response from the LLM will hang without reason. Spamming **`Ctrl+C`** or killing the task from Task manager eventually works.

## Customization

### Adding your own prompts
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
PROMPTS_LIST_PATH = prompts/custom.json

# The key name of the specific prompt config from the aforementioned JSON file path.
PROMPT_CONFIG_NAME = custom-coach
```
2. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-prompts.toml
```

### Changing to different model provider
1. Go to "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" and double-check if your desired provider is supported. Remember that the models in question must support multimodal inputs.
2. Add the necessary environment variables to your `.env` file for the chosen model provider.
3. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and change `MODEL_PROVIDER` and `MODEL_NAME` in the `chatbot` section accordingly.
```toml
[chatbot]
# Select company provider for LLM chatbot model.
MODEL_PROVIDER = anthropic

# Select LLM chat model name from company provider.
MODEL_NAME = claude-3-5-sonnet-20240620
```
4. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-provider.toml
```

### Creating cloned voice model for TTS
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
3. Create a copy of [`configs/example.toml`](configs/example.toml) in the same folder and change `MAIN_TTS_SERVICE`, `ONLINE_VOICE_MODEL` and `VOICE_SAMPLES_PATH` in the `text_to_speech` section accordingly.
```toml
[text_to_speech]
# Can specify the following based on which TTS service you want. There is a fallback mode to use Window TTS
# in case using the main TTS service fails for any reason.
# - 'online-ai' for ElevenLabs
# - 'offline-ai' for CoquiTTS (XTTS v2)
# - 'windows' for Microsoft's default TTS
MAIN_TTS_SERVICE = online-ai

[text_to_speech.online_ai]
# Internal voice model ID for ElevenLabs, can either be from pre-existing models or custom-made cloned models.
ONLINE_VOICE_MODEL = example-voice-model

[text_to_speech.offline_ai]
# Glob path to list of example audio samples for use with voice cloning. Refer to https://pymotw.com/3/glob/ for examples.
VOICE_SAMPLES_PATH = tools/output/combined/example-voice-model.wav
```
4. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-voice.toml
```
