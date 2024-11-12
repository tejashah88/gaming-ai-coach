from dataclasses import dataclass


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
