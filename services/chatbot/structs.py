from dataclasses import dataclass
from abc import ABC, abstractmethod
import json

from langchain_core.language_models.chat_models import BaseChatModel


class LLMConfig(ABC):
    provider: str
    model: str
    prompts_path: str


    def __init__(self, env_config = {}):
        self.env_config = env_config


    @abstractmethod
    def init_chat_model(self) -> BaseChatModel:
        pass


    def load_prompts(self):
        prompt_configs = None

        with open(self.prompts_path, 'r') as fp:
            prompt_configs = json.load(fp)

        return prompt_configs


@dataclass
class UserTextMessage:
    text: str
    type: str = 'text'

    def as_msg_entry(self):
        return {
            'type': self.type,
            'text': self.text,
        }


@dataclass
class UserImageMessage:
    image_data: str
    type: str = 'image_url'


    def as_msg_entry(self):
        return {
            'type': self.type,
            'image_url': {'url': f'data:image/png;base64,{self.image_data}'},
        }
