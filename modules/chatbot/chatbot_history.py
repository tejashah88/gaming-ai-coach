import json

from langchain_core.chat_history import InMemoryChatMessageHistory

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage


class ChatbotHistory:
    def __init__(self):
        self.store: dict[str, BaseChatMessageHistory] = {}


    def set_messages(self, session_id: str, messages: list[BaseMessage]) -> None:
        sesh_history = self.get_session_history(session_id)
        sesh_history.clear()
        sesh_history.add_messages(messages)


    def get_messages(self, session_id: str) -> list[BaseMessage]:
        sesh_history = self.get_session_history(session_id)
        return sesh_history.messages


    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]


    def dump_session_history(self, session_id: str, file_path: str) -> None:
        sesh_history = self.get_session_history(session_id)

        with open(file_path, 'w') as fp:
            json.dump([message.model_dump() for message in sesh_history.messages], fp, indent=2)
