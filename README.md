# Gaming AI Coach

[![Watch the video](https://img.youtube.com/vi/CdrKLB4EhMk/maxresdefault.jpg)](https://youtu.be/CdrKLB4EhMk)

A recreation of shounic's experiment where an AI model tells him what to do in Team Fortress 2, but with some extra stuff.

If you're confused, watch his video about the original experiment: [TF2 but AI Makes EVERY Decision on What To Do
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
You can add new prompts by either editing the existing JSON file in `prompts/openai/gpt-4o/general-prompts.json` or making a new JSON file with the following format:
```json
{
    "normal-coach": {
        "system-prompt": "You are coaching a novice on what to do in a video game. You need to tell him exactly what to do and what's the best course of action in the given moment. The person you are coaching is playing right now, so keep instructions to one sentence.",
        "user-prompt": "This is a screenshot of the current situation. In one short sentence, please tell me exactly what I should do next? Deliver your repsonse concisely, neutrally and without bias."
    },
    "an-extra-coach": {
        "system-prompt": "...",
        "user-prompt": "..."
    },
    ...
}
```

If you decide to go with the latter option and make a new file entirely, PLEASE DO THE FOLLOWING:
1. Go to `main/model_configs.py`
2. Make a copy of the `OpenAIConfig` class and only change the `prompts_path` field to the relative path of the new custom prompts file. Here's an example of what that should look like:
```python
class OpenAIConfigCUSTOM(LLMConfig):
    provider        = 'openai'
    model           = 'gpt-4o'
    prompts_path    = 'prompts/openai/gpt-4o/custom-prompts.json'


    def init_chat_model(self):
        api_key = get_from_dict_or_env(self.env_config, 'openai_api_key', 'OPENAI_API_KEY')

        if api_key is None:
            raise Exception('The "OPENAI_API_KEY" must be defined in your environment file')

        return ChatOpenAI(
            api_key=SecretStr(api_key),
            model=self.model,
        )
```
3. Go to `main/gaming_coach.py` and find the following 2 lines.
```python
MODEL_CONFIG = OpenAIConfig()
PROMPT_CONFIG_NAME = 'sarcastic-shounic'
```
4. Change the `OpenAIConfig` to the name of your custom class and the prompt config name accordingly.
```python
MODEL_CONFIG = OpenAIConfigCUSTOM()
PROMPT_CONFIG_NAME = 'normal-coach'
```
5. Re-run the coach again with `python -m main.gaming_coach`

## Adding a new provider
This is similar to the previous section, except it'll require some knowledge of LangChain. The main tasks to complete are the following:
1. Check [this list of possible providers](https://python.langchain.com/docs/integrations/chat/#featured-providers) to verify that the desired model supports multi-modality.
2. Create a new `LLMConfig` similar to the above and name the new class appropriately.
3. Change the fields where appropriate (such as `provider`, `model` and `prompts_path`).
4. Change the implementation of `init_chat_model` to create a new instance of the LangChain-based chat model. This can be just about anything as long as it supports the [`langchain_core.language_models.chat_models.BaseChatModel`](https://python.langchain.com/api_reference/core/language_models/langchain_core.language_models.chat_models.BaseChatModel.html) interface.
   * If there are any changes to the environment variables loaded, make sure that they are added accordingly in your `.env` file.
5. Create a new prompts config file as according to the previous section, and change `prompts_path` accordingly.
6. Go to `main/gaming_coach.py` and find the following 2 lines.
```python
MODEL_CONFIG = OpenAIConfig()
PROMPT_CONFIG_NAME = 'sarcastic-shounic'
```
7. Change the `OpenAIConfig` to the name of your custom class
```python
MODEL_CONFIG = AnthropicAIConfig()
PROMPT_CONFIG_NAME = 'sarcastic-sonnet'
```
8. Re-run the coach again with `python -m main.gaming_coach`
