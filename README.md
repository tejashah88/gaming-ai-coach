# Gaming AI Coach
An AI-powered backseat coach to fix your skill issue and/or ruin your day :). Powered by OpenAI's GPT-4o and ElevenLabs' TTS services out-of-the-box.


## Table of Contents
* [:warning: AI Safety Disclaimer :warning:](#warning-ai-safety-disclaimer-warning)
* [Introduction](#thought_balloon-introduction-thought_balloon)
* [Features](#star2-features-star2)
* [Quick Setup](#building_construction-quick-setup-building_construction)
* [Usage instructions](#computer-usage-instructions-computer)
  * [Starting the application](#red_car-starting-the-application-red_car)
  * [Exiting the application](#stop_sign-exiting-the-application-stop_sign)
* [Customization](#gear-customization-gear)
  * [Adding your own prompts](#memo-adding-your-own-prompts-memo)
  * [Changing to different model provider](#robot-changing-to-different-model-provider-robot)
  * [Creating cloned voice model for Text-to-Speech](#loudspeaker-creating-cloned-voice-model-for-text-to-speech-loudspeaker)


### Video: Playing TF2 w/ Squidward as my coach (click the thumbnail below!)
[![TF2 Demo w/ Squidward](https://img.youtube.com/vi/MKgUtl2PALw/maxresdefault.jpg)](https://youtu.be/MKgUtl2PALw)


## :warning: AI Safety Disclaimer :warning:
This should really go without saying but as this is a powerful piece of AI technology, it MUST be used responsibly! There is real potential for real harm to be done if misused, especially with the voice cloning technology.

This project serves as an educational/entertainment tool for personal, non-commercial use. By using this project, you inherently agree to use it for its intended purpose and without harming anyone. The original developer does not hold any responsibility for the use of this project for unintended and potentially harmful use cases.

\- Tejas Shah ([@tejashah88](https://github.com/tejashah88)) - Original Developer


## :thought_balloon: Introduction :thought_balloon:
This project is a recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff. If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do](https://www.youtube.com/watch?v=Z2eduTNisYA).

This experiment takes a screenshot of your current gameplay, feeds it into a given Large Language Model (LLM) like ChatGPT 4o and yells advice to you on how to proceed further with either the default Windows TTS or a custom TTS service such as from ElevenLabs or Coqui TTS.

The fun part about it is that you can use this with **any game**, using **any cloned voice model** and even **customize the prompts** to your liking. I've implemented shounic's original prompts, but it's very easy to add your own. You could for example make a coach that gives advice in a sarcastic or a dramatic manner. See the last 2 sections for more information.

This project is deemed to be mostly finished so no new features will likely be implemented, but if you find any problems, please [make a GitHub issue](https://github.com/tejashah88/gaming-ai-coach/issues).


## :star2: Features :star2:
* Works with **OpenAI's GPT-4o** model out-of-the-box (other models and providers supported, like from Anthropic or Google).
  * See "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" for more information
* Supports **ElevenLabs' TTS**, and Coqui TTS (local-first AI-based) and Windows' TTS (as a fallback)
  * Can specify your own instantly cloned voice models
* Shows a small overlay showing the taken screenshot and the model's response
* Easy to customize and experiment with different prompts (via prompts JSON file and config file)
  * [Adding your own prompts](#adding-your-own-prompts)
  * [Changing to different model provider](#changing-to-different-model-provider)
  * [Creating cloned voice model for TTS](#creating-cloned-voice-model-for-tts)


## :building_construction: Quick Setup :building_construction:
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

## :computer: Usage instructions :computer:
### :red_car: Starting the application :red_car:
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


### :stop_sign: Exiting the application :stop_sign:
The key binding to use is **`Ctrl+C`** as long as you're focused (i.e. last clicked) on either the terminal running the command or on the screenshot overlay.

It can take some time for the current action to stop before the application can shutdown, so please be patient for a few seconds. If it doesn't do anything after that, spamming **`Ctrl+C`** can help, or killing the Python process in Task Manager.

**Known bug**: There's a rare bug where sometimes fetching the response from the LLM will hang without reason. Spamming **`Ctrl+C`** or killing the task from Task manager eventually works.


## :gear: Customization :gear:
Arguably the coolest part of this project is the ability to choose whatever LLM model, coaching prompts, and even coaching voices that you want. I encourage you to try out different models like Anthropic's Claude 3.5 Sonnet or Meta's open-weights Llama 3.2, or perhaps try making your own prompts to fit your ideal coaching personality, or even trying out different voice models like Jack Sparrow or Squidward.

However, this customization comes with heavy premise of responsible and ethical AI usage of this project. If you haven't read it already, **read the [AI Safety Disclaimer](#warning-ai-safety-disclaimer-warning)** and understand that any misuse of this project beyond educational/entertainment purposes is NOT allowed by the original developer.


### :memo: Adding your own prompts :memo:
Adding your own prompts is very easy! The main idea is that you need a system prompt to tell the LLM what it should be doing in the first place (i.e. being a gaming coach) and additional user prompts to add more instructions like what to do when it receives a screenshot of your gameplay.

Here's an example of a system and accompanying user prompt(s) for the sarcastic coach as featured in the above demo:

#### System Prompt
```
You are coaching a novice on what to do in a video game. You need to tell him exactly what to do
and what's the best course of action in the given moment. The person you are coaching is playing
right now, so keep instructions to one sentence. be short and precise with your responses. Make
mention of landmarks if necessary, that can help the player understand your direction in as much
clarity as possible.
```

#### User Prompt(s)
```
This is a screenshot of the current situation. In one short sentence, please tell me exactly what
I should do next? Deliver your response in a sarcastic way. Make sure to still give advice though.
```

If you want to learn how to add your own custom prompts, click the following tutorial link below:
* Tutorial for: [Adding your own prompts](docs/HOWTO_CUSTOMIZATION.md#adding-your-own-prompts)


### :robot: Changing to different model provider :robot:
While OpenAI's GPT-4o model performs fairly well for 95% of use cases of this project, it's easy to change it to any multimodal LLM model out in the market, whether it's proprietary or open-source/open-weights! Check out the "[Supported providers and models](docs/SUPPORTED_PROVIDERS_MODELS.md)" section for the list of supported model providers. Note that this list is non-exhaustive and none of the other providers have been tested as of November 2024.

If you want to learn how to change to using a different model provider, click the following tutorial link below:
* Tutorial for: [Changing to different model provider](docs/HOWTO_CUSTOMIZATION.md#changing-to-different-model-provider)


### :loudspeaker: Creating cloned voice model for Text-to-Speech :loudspeaker:
Hearing from Microsoft Sam giving you coaching advice can become monotonous really quick, but it doesn't have to be. Thanks to the ability of voice cloning, it's possible to have your favorite fictional and/or realistic characters be your coach.

Note that this requires either a paid ElevenLabs account (about $5/month for 30 minutes of generated audio) or a CUDA-enabled GPU to run the local-first AI-powered TTS services (you can run with a CPU but it's painfully slow). This also requires downloading a set of clean audio samples of the voice to be cloned for the best experience.

Here's a few starting resources for making your own voice clones. Use them responsibly!
  * [/g/ Voice Sample Repository](https://rentry.org/Voice-Samples)
  * [The Sounds Resource](https://www.sounds-resource.com/)
  * [Aiartes - VoiceAI](https://web.archive.org/web/20241006171246/https://aiartes.com/voiceai)

If you want to learn how to create your own cloned voice models, click the following tutorial link below:
* Tutorial for: [Creating your own cloned voice models](docs/HOWTO_CUSTOMIZATION.md#creating-cloned-voice-model-for-tts)
