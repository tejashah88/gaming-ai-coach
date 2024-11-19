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
* [Known Issues](#known-issues)

### Video: Playing TF2 w/ Squidward as my coach (click the thumbnail below!)
[![TF2 Demo w/ Squidward](https://img.youtube.com/vi/MKgUtl2PALw/maxresdefault.jpg)](https://youtu.be/MKgUtl2PALw)

## Introduction

This project is a recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff. If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do](https://www.youtube.com/watch?v=Z2eduTNisYA).

This experiment takes a screenshot of your current gameplay, feeds it into a given Large Language Model (LLM) like ChatGPT 4o and yells advice to you on how to proceed further with either the default Windows TTS or a custom TTS service such as from ElevenLabs or Coqui AI.

The fun part about it is that you can use this with **any game**, using **any cloned voice model** and even **customize the prompts** to your liking. I've implemented shounic's original prompts, but it's very easy to add your own. You could for example make a coach that gives advice in a sarcastic or a dramatic manner. See the last 2 sections for more information.

This project is deemed to be mostly finished so no new features will likely be implemented, but if you find any problems, please [make a GitHub issue](https://github.com/tejashah88/gaming-ai-coach/issues).

## Features
* Works with **OpenAI's GPT-4o** model out-of-the-box (other models and providers supported, like from Anthropic or Google).
  * See "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" for more information
* Supports **Elevenlabs' Text-to-speech** service, CoquiTTS (local-first AI-based) or Windows' TTS (as a fallback)
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
5. Create a copy of [`configs/example.ini`](configs/example.ini) in the same folder and refer to the comments to change it to your preferences.
6. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom.ini
```

## Usage instructions
* `python -m gaming_coach --config path/to/config.ini` - Starts the application
* `Ctrl+C` - Exits the application

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

1. Create a copy of [`configs/example.ini`](configs/example.ini) in the same folder and change `PROMPTS_LIST_PATH` and `PROMPT_CONFIG_NAME` in the `prompts` section accordingly.
```ini
[prompts]
# The JSON file path for the list of prompts to load from.
PROMPTS_LIST_PATH = prompts/custom.json

# The key name of the specific prompt config from the aforementioned JSON file path.
PROMPT_CONFIG_NAME = custom-coach
```
2. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-prompts.ini
```

### Changing to different model provider
1. Go to "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" and double-check if your desired provider is supported. Remember that the models in question must support multimodal inputs.
2. Add the necessary environment variables to your `.env` file for the chosen model provider.
3. Create a copy of [`configs/example.ini`](configs/example.ini) in the same folder and change `MODEL_PROVIDER` and `MODEL_NAME` in the `chatbot` section accordingly.
```ini
[chatbot]
# Select company provider for LLM chatbot model.
MODEL_PROVIDER = anthropic

# Select LLM chat model name from company provider.
MODEL_NAME = claude-3-5-sonnet-20240620
```
2. Run the gaming coach, making sure to specify your new config path.
```bash
python -m gaming_coach --config configs/custom-provider.ini
```

### Creating cloned voice model for TTS
1. Find a set of voice samples (in WAV format or converted to it) to use as the basis for your voice cloning.
2. Run `python -m tools/prep_samples.py`

## Known Issues
- Config validation is mostly non-existent, and requires decent Python experience to understand the codebase. Comments within example configuation files should suffice but are not exhaustive.
- Only OpenAI's GPT-4o model has been tested, unsure about how nicely other model providers play with this program
- There's a rare bug where sometimes fetching the response from the LLM will hang without reason. Spamming `Ctrl+C` eventually works.
- Code documentation is sparse at best, needs more comments for explaining function inputs/outputs and complex parts of code.
