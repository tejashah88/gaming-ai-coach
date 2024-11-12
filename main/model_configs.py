from pydantic import SecretStr
from langchain_core.utils.env import get_from_dict_or_env

from langchain_openai import ChatOpenAI

from modules.ai_chatbot.structs import LLMConfig


class OpenAIConfig(LLMConfig):
    provider        = 'openai'
    model           = 'gpt-4o'


    def init_chat_model(self):
        api_key = get_from_dict_or_env(self.env_config, 'openai_api_key', 'OPENAI_API_KEY')

        if api_key is None:
            raise Exception('The "OPENAI_API_KEY" must be defined in your environment file')

        return ChatOpenAI(
            api_key=SecretStr(api_key),
            model=self.model,
        )
