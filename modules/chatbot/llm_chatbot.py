import os
import time

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import trim_messages

from modules.chatbot.chatbot_history import ChatbotHistory
from modules.chatbot.messages import HumanTextMessage, HumanImageMessage

from typing import Any
from langchain_core.messages import BaseMessage


class LLMChatbot:
    def __init__(self, chat_model: BaseChatModel, keep_back_forth_cycles: int = 0):
        self.chat_model: BaseChatModel = chat_model

        self.current_session_id: str = self.generate_session_id()
        self.keep_back_forth_cycles: int = keep_back_forth_cycles
        self.history: ChatbotHistory = ChatbotHistory()


    def generate_session_id(self) -> str:
        epoch_sec = int(time.time())
        random_salt = os.urandom(8).hex()
        return f'thread-{epoch_sec}-{random_salt}'


    def setup_prompt_template(
        self,
        system_message: str,
        human_messages: list[HumanTextMessage | HumanImageMessage]
    ) -> None:
        self.prompt_template = ChatPromptTemplate.from_messages([
            ('system', system_message),
            ('placeholder', '{__history}'),
            ('human', [message.to_dict() for message in human_messages]),
        ])


    def send_message(
        self,
        prompt_vars: dict[str, Any] = {},
        configurable_settings: dict[str, Any] = {},
    ) -> BaseMessage:
        if self.keep_back_forth_cycles == 0:
            self.current_session_id = self.generate_session_id()

        chat_history = self.history.get_messages(self.current_session_id)
        input_messages = self.prompt_template.format_messages(**{
            **prompt_vars,
            '__history': chat_history,
        })

        # Preserve only the last 'n' messages, while keeping the system prompt and starting with a human message
        # Formula for keeping last 'n' messages: c + b * n
        # - c = 2 (system prompt and initial user prompt)
        # - b = 2 (bot response + next user response)
        # - n (number of back-and-forth user & bot exchanges)
        input_trimmed_messages = trim_messages(
            input_messages,
            strategy='last',
            token_counter=len,
            max_tokens=(2 + self.keep_back_forth_cycles * 2),
            include_system=True,
            start_on='human',
        )

        print(f'Number of input messages: {len(input_trimmed_messages)}')

        bot_response = self.chat_model.invoke(
            input_trimmed_messages,
            config={'configurable': configurable_settings}
        )

        new_chat_history = input_trimmed_messages + [bot_response]

        self.history.set_messages(self.current_session_id, new_chat_history)

        return bot_response
