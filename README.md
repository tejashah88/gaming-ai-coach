# Gaming AI Coach

[![Watch the video](https://img.youtube.com/vi/CdrKLB4EhMk/maxresdefault.jpg)](https://youtu.be/CdrKLB4EhMk)

A recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff. If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do
](https://www.youtube.com/watch?v=Z2eduTNisYA)

This experiment takes a screenshot of your current gameplay, feeds it into a given LLM of your choice and gives you advice on how to proceed further. The fun part about it is that you can use this with **any game** and even **customize the prompts** to your liking. I've implemented shounic's original prompts, but it's very easy to add your own. You could for example make a coach that gives advice in a sarcastic or a dramatic manner. See the last 2 sections for more information.

## NOTICE
This is very much a technical demo that I cobbled together within a few hours and as such is subject to odd bugs or annoyances. If you find any problems, please [make a GitHub issue](https://github.com/tejashah88/gaming-ai-coach/issues).

## Features
- Works with OpenAI's GPT-4o model out-of-the-box
- Shows a small overlay showing the taken screenshot and the model's response
- Easy to make variations for your prompt to save for later and share with others (via a JSON file)
- Can support other model providers (like from Anthropic or Google) thanks to the LangChain API
  - See [this list of possible providers](https://python.langchain.com/docs/integrations/chat/#featured-providers) for more information. Note that the providers must support the "Multimodal" feature.

## Supported models and providers
The list of models has the baseline assumption that they support multimodal inputs. By default, the OpenAI LangChain package is installed but you can add provider-specific packages by doing `pip install langchain-{provider}`, substituting  `{provider}` with your desired one.

Here's the full list of providers as supported by LangChain: https://python.langchain.com/docs/integrations/chat/#featured-providers

### Only supports own models
* OpenAI
  * Provider info: https://platform.openai.com/docs/models
  * Supported models
    * GPT-4o
    * GPT-4o mini
  * LangChain package to install: `langchain-openai`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/openai/
* Anthropic
  * Provider info: https://docs.anthropic.com/en/docs/about-claude/models
  * Supported models
    * Claude 3.5 Sonnet
    * Claude 3 Opus
    * Claude 3 Sonnet
    * Claude 3 Haiku
  * LangChain package to install: `langchain-anthropic`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/anthropic/
* Google Generative AI
  * Provider info: https://ai.google.dev/gemini-api/docs/models/gemini
  * Supported models
    * Gemini 1.5 Flash
    * Gemini 1.5 Flash-8B
    * Gemini 1.5 Pro
  * LangChain package to install: `langchain-google-genai`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/google_generative_ai/

### Allows custom models
* AWS Bedrock
  * Provider info: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
  * Supported models:
    * Full list: https://docs.aws.amazon.com/bedrock/latest/userguide/models-features.html
  * LangChain package to install: `langchain-aws`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/bedrock/
* Google Vertex AI
  * Provider info: https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/overview
  * Supported models:
    * Gemini 1.5 Flash
    * Gemini 1.5 Flash-8B
    * Gemini 1.5 Pro
    * More in "Model Garden": https://console.cloud.google.com/vertex-ai/model-garden
  * LangChain package to install: `langchain-google-vertexai`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/
* Together AI
  * Provider info: https://docs.together.ai/docs/vision-overview
  * Supported models:
    * Llama 3.2 Vision 11B
    * Llama 3.2 Vision 90B
    * "Serverless" list: https://docs.together.ai/docs/serverless-models
    * "Dedicated" list: https://docs.together.ai/docs/dedicated-models
  * LangChain package to install: `langchain-together`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/together/
* HuggingFace
  * Provider info: https://huggingface.co/models
  * Supported models:
    * Llama 3.2 Vision 11B
    * Llama 3.2 Vision 90B
    * Full list: https://huggingface.co/models
  * LangChain package to install: `langchain-huggingface`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/huggingface/
* Ollama
  * Provider info: https://github.com/ollama/ollama
  * Supported models:
    * Llama 3.2 Vision 11B
    * Llama 3.2 Vision 90B
    * Full list: https://github.com/ollama/ollama#model-library
  * LangChain package to install: `langchain-ollama`
  * LangChain documentation: https://python.langchain.com/docs/integrations/chat/ollama/


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

## Adding your own prompts to an existing provider
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
1. Check [this list of possible providers](https://python.langchain.com/docs/integrations/chat/#featured-providers) to verify that the desired model supports multi-modality.
2. Add the necessary environment variables to your `.env` file for the chosen model provider.
3. Create a new prompts config file as according to the previous section, and change `prompts_path` accordingly.
4. Go to `main/gaming_coach.py` and find the following 4 lines.
```python
MODEL_PROVIDER = 'openai'
MODEL_NAME = 'gpt-4o'
```
5. Change the `MODEL_PROVIDER` and `MODEL_NAME` accordingly
```python
MODEL_PROVIDER = 'anthropic'
MODEL_NAME = 'claude-3-5-sonnet-20240620'
```
6. Re-run the coach again with `python -m main.gaming_coach`
