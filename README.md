# Gaming AI Coach

[![TF2 Demo](https://img.youtube.com/vi/CdrKLB4EhMk/maxresdefault.jpg)](https://youtu.be/CdrKLB4EhMk)

A recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff. If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do
](https://www.youtube.com/watch?v=Z2eduTNisYA)

This experiment takes a screenshot of your current gameplay, feeds it into a given LLM of your choice and gives you advice on how to proceed further. The fun part about it is that you can use this with **any game** and even **customize the prompts** to your liking. I've implemented shounic's original prompts, but it's very easy to add your own. You could for example make a coach that gives advice in a sarcastic or a dramatic manner. See the last 2 sections for more information.

## Table of Contents
* [NOTICE](#notice)
* [Features](#features)
* [Usage instructions](#usage-instructions)
* [How to set this up (on Windows)](#how-to-set-this-up-on-windows)
* [Adding your own prompts to an existing provider](#adding-your-own-prompts-to-an-existing-provider)
* [Adding a new provider](#adding-a-new-provider)

## NOTICE
This is very much a technical demo that I cobbled together within a few hours and as such is subject to odd bugs or annoyances. If you find any problems, please [make a GitHub issue](https://github.com/tejashah88/gaming-ai-coach/issues).

## Features
* Works with OpenAI's GPT-4o model out-of-the-box
* Shows a small overlay showing the taken screenshot and the model's response
* Easy to make variations for your prompt to save for later and share with others (via a JSON file)
* Support other model providers (like from Anthropic or Google) thanks to LangChain
  * See "[Supported providers and models](SUPPORTED_PROVIDERS_MODELS.md)" for more information


## Usage instructions
* `python -m main.gaming_coach` - Starts the application
* `Ctrl+C` - Exits the application

## How to set this up (on Windows)
1. Get an OpenAI key
2. Clone or fork this repo
3. Create a `.env` file and add the following contents, substituting `<<INSERT_API_KEY_HERE>>` with your copied API key
```yaml
OPENAI_API_KEY=<<INSERT_API_KEY_HERE>>
```
4. Follow the steps below to run the coach
```bash
# Setup virtual environment and dependencies
python -m venv env
env\Scripts\activate.bat
pip install -r requirements.txt

# Run the gaming coach
python -m main.gaming_coach
```

## Adding your own prompts
You can add new prompts by either editing the existing JSON file in `prompts/general-experiment.json` or making a new JSON file with the following format:
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
1. Go to `main/gaming_coach.py` and find the following 2 lines.
```python
PROMPTS_LIST_PATH = 'prompts/general-shounic.json'
PROMPT_CONFIG_NAME = 'sarcastic-shounic'
```
2. Change the `OpenAIConfig` to the name of your custom class and the prompt config name accordingly.
```python
PROMPTS_LIST_PATH = 'prompts/general-custom.json'
PROMPT_CONFIG_NAME = 'sarcastic-custom'
```
3. Re-run the coach again with `python -m main.gaming_coach`

## Adding a new provider
This is similar to the previous section, except it'll require some knowledge of LangChain. The main tasks to complete are the following:
1. Go to "[Supported providers and models](SUPPORTED_PROVIDERS_MODELS.md)" and double-check if your desired provider is supported. Remember that the models in question must support multimodal inputs.
2. Add the necessary environment variables to your `.env` file for the chosen model provider.
3. Go to `main/gaming_coach.py` and find the following 4 lines.
```python
MODEL_PROVIDER = 'openai'
MODEL_NAME = 'gpt-4o'
```
4. Change the `MODEL_PROVIDER` and `MODEL_NAME` accordingly
```python
MODEL_PROVIDER = 'anthropic'
MODEL_NAME = 'claude-3-5-sonnet-20240620'
```
5. Re-run the coach again with `python -m main.gaming_coach`
