# Gaming AI Coach

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Setup instructions](#setup-instructions)
* [Usage instructions](#usage-instructions)
* [Adding your own prompts](#adding-your-own-prompts)
* [Changing to a different provider](#changing-to-a-different-provider)

### Video: Playing TF2 Demo w/ Squidward as my coach
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

## Quick Setup instructions
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
    "an-extra-coach": {
        "system-prompt": "...",
        "user-prompts": [
            "..."
        ]
    },
    ...
}
```

If you decide to go with the latter option, please do the following:
1. Go to `gaming_coach.py`, find the following 2 lines and change them accordingly.
```python
PROMPTS_LIST_PATH = 'prompts/general-custom.json'
PROMPT_CONFIG_NAME = 'sarcastic-custom'
```
2. Re-run the coach again with `python -m gaming_coach --config configs/default.ini`

### Changing to a different provider
1. Go to "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" and double-check if your desired provider is supported. Remember that the models in question must support multimodal inputs.
2. Add the necessary environment variables to your `.env` file for the chosen model provider.
3. Go to `gaming_coach.py` and find the following 2 lines.
```python
MODEL_PROVIDER = 'openai'
MODEL_NAME = 'gpt-4o'
```
1. Change the `MODEL_PROVIDER` and `MODEL_NAME` accordingly
```python
MODEL_PROVIDER = 'anthropic'
MODEL_NAME = 'claude-3-5-sonnet-20240620'
```
1. Re-run the coach again with `python -m gaming_coach --config configs/default.ini`
