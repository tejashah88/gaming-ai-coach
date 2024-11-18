from dataclasses import dataclass
from typing import Any


@dataclass
class HumanTextMessage:
    data: str
    type: str = 'text'

    def to_dict(self) -> dict[str, str]:
        return {
            'type': self.type,
            'text': self.data,
        }


@dataclass
class HumanImageMessage:
    data: str
    type: str = 'image_url'


    def to_dict(self) -> dict[str, str | dict[str, str]]:
        return {
            'type': self.type,
            'image_url': {
                'url': f'data:image/png;base64,{self.data}'
            }
        }
