from dataclasses import dataclass
from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel


class LLMConfig(ABC):
    provider: str
    model: str


    def __init__(self, env_config = {}):
        self.env_config = env_config


    @abstractmethod
    def init_chat_model(self) -> BaseChatModel:
        pass


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
            'image_url': {
                'url': f'data:image/png;base64,{self.image_data}'
            },
        }
